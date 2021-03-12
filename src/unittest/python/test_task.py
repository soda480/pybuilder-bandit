#   -*- coding: utf-8 -*-
import unittest
from mock import patch
from mock import call
from mock import Mock
from mock import mock_open

from pybuilder_bandit.task import init_bandit
from pybuilder_bandit.task import bandit
from pybuilder_bandit.task import get_command
from pybuilder_bandit.task import translate_confidence_level
from pybuilder_bandit.task import translate_severity_level
from pybuilder_bandit.task import read_data
from pybuilder_bandit.task import get_summary_lines
from pybuilder_bandit.task import process_result

from pybuilder.errors import BuildFailedException


class TestTask(unittest.TestCase):

    def setUp(self):
        """
        """
        pass

    def tearDown(self):
        """
        """
        pass

    def test__init_bandit_Should_CallExpected_When_Called(self, *patches):
        project_mock = Mock()
        init_bandit(project_mock)
        self.assertTrue(call('bandit_break_build', False) in project_mock.set_property_if_unset.mock_calls)
        self.assertTrue(call('bandit_confidence_level', 'LOW') in project_mock.set_property_if_unset.mock_calls)
        self.assertTrue(call('bandit_severity_level', 'LOW') in project_mock.set_property_if_unset.mock_calls)
        self.assertTrue(call('bandit_skip_ids', None) in project_mock.set_property_if_unset.mock_calls)

    @patch('pybuilder_bandit.task.get_command')
    @patch('pybuilder_bandit.task.process_result')
    def test__bandit_Should_CallExpected_When_VerifyResultFalse(self, process_result_patch, get_command_patch, *patches):
        command_mock = Mock()
        get_command_patch.return_value = command_mock
        project_mock = Mock()
        project_mock.get_property.side_effect = [True, None]
        logger_mock = Mock()
        bandit(project_mock, logger_mock)
        process_result_patch.assert_called_once_with(project_mock, command_mock.run_on_production_source_files.return_value, logger_mock, project_mock.expand_path.return_value)
        command_mock.run_on_production_source_files.assert_called_once_with(logger_mock, include_dirs_only=True, include_test_sources=True, include_scripts=False)

    @patch('pybuilder_bandit.task.translate_severity_level')
    @patch('pybuilder_bandit.task.translate_confidence_level')
    @patch('pybuilder_bandit.task.ExternalCommandBuilder')
    def test__get_command_Should_CallAndReturnExpected_When_Skip(self, external_command_builder_patch, *patches):
        command_mock = Mock()
        external_command_builder_patch.return_value = command_mock
        project_mock = Mock()
        project_mock.get_property.return_value = 'id1,id2,id3'
        result = get_command(project_mock, '--output-filename--')
        external_command_builder_patch.assert_called_once_with('bandit', project_mock)
        self.assertEqual(result, external_command_builder_patch.return_value)
        self.assertTrue(call('--skip') in command_mock.use_argument.mock_calls)
        self.assertTrue(call('id1,id2,id3') in command_mock.use_argument.mock_calls)

    @patch('pybuilder_bandit.task.translate_severity_level')
    @patch('pybuilder_bandit.task.translate_confidence_level')
    @patch('pybuilder_bandit.task.ExternalCommandBuilder')
    def test__get_command_Should_CallAndReturnExpected_When_NoSkip(self, external_command_builder_patch, *patches):
        command_mock = Mock()
        external_command_builder_patch.return_value = command_mock
        project_mock = Mock()
        project_mock.get_property.return_value = None
        result = get_command(project_mock, '--output-filename--')
        external_command_builder_patch.assert_called_once_with('bandit', project_mock)
        self.assertEqual(result, external_command_builder_patch.return_value)
        self.assertFalse(call('--skip') in command_mock.use_argument.mock_calls)

    def test__translate_confidence_level_Should_ReturnExpected_When_Low(self, *patches):
        result = translate_confidence_level('LOW')
        self.assertEqual(result, '-i')

    def test__translate_confidence_level_Should_ReturnExpected_When_Medium(self, *patches):
        result = translate_confidence_level('MEDIUM')
        self.assertEqual(result, '-ii')

    def test__translate_confidence_level_Should_ReturnExpected_When_High(self, *patches):
        result = translate_confidence_level('HIGH')
        self.assertEqual(result, '-iii')

    def test__translate_confidence_level_Should_RaisValueError_When_Invalid(self, *patches):
        with self.assertRaises(ValueError):
            translate_confidence_level('BAD')

    def test__translate_severity_level_Should_ReturnExpected_When_Low(self, *patches):
        result = translate_severity_level('LOW')
        self.assertEqual(result, '-l')

    def test__translate_severity_level_Should_ReturnExpected_When_Medium(self, *patches):
        result = translate_severity_level('MEDIUM')
        self.assertEqual(result, '-ll')

    def test__translate_severity_level_Should_ReturnExpected_When_High(self, *patches):
        result = translate_severity_level('HIGH')
        self.assertEqual(result, '-lll')

    def test__translate_severity_level_Should_RaisValueError_When_Invalid(self, *patches):
        with self.assertRaises(ValueError):
            translate_severity_level('BAD')

    @patch('builtins.open')
    @patch('pybuilder_bandit.task.json')
    def test__read_data_Should_ReturnExpected_When_Called(self, json_patch, open_patch, *patches):
        open_patch.return_value.__enter__.return_value = mock_open()
        result = read_data('--filename--')
        self.assertEqual(result, json_patch.load.return_value)

    def test__get_summary_lines_ReturnExepcted_When_Called(self, *patches):
        data = {
            "errors": [],
            "metrics": {
                "_totals": {
                    "CONFIDENCE.HIGH": 1.0,
                    "CONFIDENCE.LOW": 0.0,
                    "CONFIDENCE.MEDIUM": 1.0,
                    "CONFIDENCE.UNDEFINED": 0.0,
                    "SEVERITY.HIGH": 0.0,
                    "SEVERITY.LOW": 1.0,
                    "SEVERITY.MEDIUM": 1.0,
                    "SEVERITY.UNDEFINED": 0.0,
                    "loc": 238,
                    "nosec": 0
                }
            },
            "results": ['--1--', '--2--']
        }
        result = get_summary_lines(data)
        expected_result = [
            'Test results:\n',
            '    Number of issues identified: 2\n',
            'Code scanned:\n',
            '    Total lines of code: 238\n',
            '    Total lines skipped (#nosec): 0\n',
            'Run metrics:\n',
            '    Total issues (by severity):\n',
            '        Undefined: 0.0\n',
            '        Low: 1.0\n',
            '        Medium: 1.0\n',
            '        High: 0.0\n',
            '    Total issues (by confidence):\n',
            '        Undefined: 0.0\n',
            '        Low: 0.0\n',
            '        Medium: 1.0\n',
            '        High: 1.0\n']
        self.assertEqual(result, expected_result)

    def test__process_result_Should_RaiseBuildFailedException_When_FailBuildAndNonZeroExitCode(self, *patches):
        project_mock = Mock()
        project_mock.get_property.side_effect = [False, True]
        result_mock = Mock()
        result_mock.exit_code = 1
        with self.assertRaises(BuildFailedException):
            process_result(project_mock, result_mock, Mock(), '--output-filename--')

    def test__process_result_Should_LogWarn_When_NoFailBuildAndNonZeroExitCode(self, *patches):
        project_mock = Mock()
        project_mock.get_property.side_effect = [False, False]
        result_mock = Mock()
        result_mock.exit_code = 1
        logger_mock = Mock()
        process_result(project_mock, result_mock, logger_mock, '--output-filename--')
        logger_mock.warn.assert_called()

    def test__process_result_Should_LogInfo_When_FailBuildAndZeroExitCode(self, *patches):
        project_mock = Mock()
        project_mock.get_property.side_effect = [False]
        result_mock = Mock()
        result_mock.exit_code = 0
        logger_mock = Mock()
        process_result(project_mock, result_mock, logger_mock, '--output-filename--')
        logger_mock.info.assert_called()

    @patch('pybuilder_bandit.task.read_data')
    @patch('pybuilder_bandit.task.get_summary_lines')
    @patch('pybuilder_bandit.task.log_report')
    def test__process_result_Should_LogReport_When_Verbose(self, log_report_patch, get_summary_lines_patch, *patches):
        project_mock = Mock()
        project_mock.get_property.side_effect = [True]
        result_mock = Mock()
        result_mock.exit_code = 0
        logger_mock = Mock()
        process_result(project_mock, result_mock, logger_mock, '--output-filename--')
        log_report_patch.assert_called_once_with(logger_mock, 'bandit', get_summary_lines_patch.return_value)
