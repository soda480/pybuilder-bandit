[![GitHub Workflow Status](https://github.com/soda480/pybuilder-bandit/workflows/build/badge.svg)](https://github.com/soda480/pybuilder-bandit/actions)
[![Code Coverage](https://codecov.io/gh/soda480/pybuilder-bandit/branch/main/graph/badge.svg)](https://codecov.io/gh/soda480/pybuilder-bandit)
[![Code Grade](https://www.code-inspector.com/project/19887/status/svg)](https://frontend.code-inspector.com/project/19887/dashboard)
[![PyPI version](https://badge.fury.io/py/pybuilder-bandit.svg)](https://badge.fury.io/py/pybuilder-bandit)

# pybuilder-bandit #

A pybuilder plugin that executes the `bandit` security linter on your project. Bandit is a tool designed to find common security issues in Python code, for more information refer to the [bandit pypi page](https://pypi.org/project/bandit/).

To add this plugin into your pybuilder project, add the following line at the top of your build.py:
```python
use_plugin('pypi:pybuilder_bandit', '~=0.1.0')
```

**NOTE** version `v0.1.x` of this plugin will only work with version `v0.11.x` of Pybuilder.

### Pybuilder bandit properties ###

The pybuilder task `pyb bandit` will use bandit to scan your project to find common security issues, verbose mode will display to the screen any issues found. The following plugin properties are available to further configure the scan.

Name | Type | Default Value | Description
-- | -- | -- | --
bandit_fail_build | bool | False | Fail build if scan detects any issues
bandit_confidence_level | str | LOW | Report only issues of a given confidence level or higher: LOW, MEDIUM, HIGH
bandit_severity_level | str | LOW | report only issues of a given severity level or higher: LOW, MEDIUM, HIGH
bandit_skip_ids | str | None | comma-separated list of test IDs to skip

The plugin properties are set using `project.set_property`, the following is an example of how to set the properties:

```Python
project.set_property('bandit_fail_build', True)
project.set_property('bandit_confidence_level', 'LOW')
project.set_property('bandit_severity_level', 'MEDIUM')
project.set_property('bandit_skip_ids', 'B110,B315')
```

### Development ###

Clone the repository and ensure the latest version of Docker is installed on your development server.

Build the Docker image:
```sh
docker image build \
-t \
pybbandit:latest .
```

Run the Docker container:
```sh
docker container run \
--rm \
-it \
-v $PWD:/pybuilder-bandit \
pybbandit:latest \
/bin/sh
```

Execute the build:
```sh
pyb -X
```