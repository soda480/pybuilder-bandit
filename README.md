# pybuilder-bandit
[![GitHub Workflow Status](https://github.com/soda480/pybuilder-bandit/workflows/build/badge.svg)](https://github.com/soda480/pybuilder-bandit/actions)
[![coverage](https://img.shields.io/badge/coverage-100%25-brightgreen)](https://pybuilder.io/)
[![complexity](https://img.shields.io/badge/complexity-A-brightgreen)](https://radon.readthedocs.io/en/latest/api.html#module-radon.complexity)
[![PyPI version](https://badge.fury.io/py/pybuilder-bandit.svg)](https://badge.fury.io/py/pybuilder-bandit)
[![python](https://img.shields.io/badge/python-3.7%20%7C%203.8%20%7C%203.9%20%7C%203.10-teal)](https://www.python.org/downloads/)

A pybuilder plugin that analyzes your project for common security issues using `bandit`. Bandit is a security linter for Python code, for more information refer to the [bandit pypi page](https://pypi.org/project/bandit/).

To add this plugin into your pybuilder project, add the following line near the top of your build.py:
```python
use_plugin('pypi:pybuilder_bandit')
```

**NOTE** if you are using Pybuilder version `v0.11.x`, then specify the following version of the plugin:
```python
use_plugin('pypi:pybuilder_bandit', '~=0.1.3')
```

### Pybuilder bandit properties

The pybuilder task `pyb bandit` will use bandit to scan your project to find common security issues, verbose mode will display to the screen any issues found. The following plugin properties are available to further configure the scan.

Name | Type | Default Value | Description
-- | -- | -- | --
bandit_break_build | bool | False | Fail build if scan detects any issues
bandit_confidence_level | str | LOW | Report only issues of a given confidence level or higher: LOW, MEDIUM, HIGH
bandit_severity_level | str | LOW | report only issues of a given severity level or higher: LOW, MEDIUM, HIGH
bandit_skip_ids | str | None | comma-separated list of test IDs to skip
bandit_include_testsources | bool | False | include scanning of project test sources
bandit_include_scripts | bool | False | include scanning of project scripts

The plugin properties are set using `project.set_property`, the following is an example of how to set the properties:

```Python
project.set_property('bandit_break_build', True)
project.set_property('bandit_confidence_level', 'LOW')
project.set_property('bandit_severity_level', 'MEDIUM')
project.set_property('bandit_skip_ids', 'B110,B315')
project.set_property('bandit_include_testsources', True)
project.set_property('bandit_include_scripts', True)
```

### Development

Clone the repository and ensure the latest version of Docker is installed on your development server.

Build the Docker image:
```sh
docker image build \
-t pybbandit:latest .
```

Run the Docker container:
```sh
docker container run \
--rm \
-it \
-v $PWD:/code \
pybbandit:latest \
bash
```

Execute the build:
```sh
pyb -X
```
