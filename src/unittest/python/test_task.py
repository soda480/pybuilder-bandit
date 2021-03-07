#   -*- coding: utf-8 -*-
import unittest
from mock import patch
from mock import call
from mock import Mock

from pybuilder_bandit.task import init_bandit
from pybuilder_bandit.task import bandit
from pybuilder_bandit.task import get_command
from pybuilder_bandit.task import set_verbose_property
from pybuilder_bandit.task import translate_confidence_level
from pybuilder_bandit.task import translate_severity_level
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

    @patch('pybuilder_bandit.task.set_verbose_property')
    @patch('pybuilder_bandit.task.get_command')
    @patch('pybuilder_bandit.task.process_result')
    def test__bandit_Should_CallExpected_When_VerifyResultFalse(self, process_result_patch, get_command_patch, *patches):
        command_mock = Mock()
        get_command_patch.return_value = command_mock
        project_mock = Mock()
        logger_mock = Mock()
        bandit(project_mock, logger_mock, Mock())
        process_result_patch.assert_called_once_with(project_mock, command_mock.run_on_production_source_files.return_value, logger_mock)

    @patch('pybuilder_bandit.task.translate_severity_level')
    @patch('pybuilder_bandit.task.translate_confidence_level')
    @patch('pybuilder_bandit.task.ExternalCommandBuilder')
    def test__get_command_Should_CallAndReturnExpected_When_Skip(self, external_command_builder_patch, *patches):
        command_mock = Mock()
        external_command_builder_patch.return_value = command_mock
        project_mock = Mock()
        project_mock.get_property.return_value = 'id1,id2,id3'
        reactor_mock = Mock()
        result = get_command(project_mock, reactor_mock)
        external_command_builder_patch.assert_called_once_with('bandit', project_mock, reactor_mock)
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
        reactor_mock = Mock()
        result = get_command(project_mock, reactor_mock)
        external_command_builder_patch.assert_called_once_with('bandit', project_mock, reactor_mock)
        self.assertEqual(result, external_command_builder_patch.return_value)
        self.assertFalse(call('--skip') in command_mock.use_argument.mock_calls)

    def test__set_verbose_property_Should_CallExpected_When_Called(self, *patches):
        project_mock = Mock()
        set_verbose_property(project_mock)
        project_mock.set_property.assert_called_once_with('bandit_verbose_output', project_mock.get_property.return_value)

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

    def test__process_result_Should_RaiseBuildFailedException_When_FailBuildAndReportLines(self, *patches):
        project_mock = Mock()
        project_mock.get_property.return_value = True
        result_mock = Mock()
        result_mock.report_lines = ['--line1--']
        with self.assertRaises(BuildFailedException):
            process_result(project_mock, result_mock, Mock())

    def test__process_result_Should_LogWarn_When_NoFailBuildAndReportLines(self, *patches):
        project_mock = Mock()
        project_mock.get_property.return_value = False
        result_mock = Mock()
        result_mock.report_lines = ['--line1--']
        logger_mock = Mock()
        process_result(project_mock, result_mock, logger_mock)
        logger_mock.warn.assert_called()

    def test__process_result_Should_LogInfo_When_FailBuildAndNoReportLines(self, *patches):
        project_mock = Mock()
        project_mock.get_property.return_value = True
        result_mock = Mock()
        result_mock.report_lines = []
        logger_mock = Mock()
        process_result(project_mock, result_mock, logger_mock)
        logger_mock.info.assert_called()
