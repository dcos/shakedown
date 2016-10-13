# Shakedown [![Build Status](http://jenkins.mesosphere.com/service/jenkins/buildStatus/icon?job=public-shakedown-master)](http://jenkins.mesosphere.com/service/jenkins/job/public-shakedown-master/)

DC/OS test harness.


## Overview

*A shakedown is a period of testing or a trial journey undergone by a ship, aircraft or other craft and its crew before being declared operational.
    — https://en.wikipedia.org/wiki/Shakedown_(testing)*


## Installation

Shakedown requires Python 3.4+.

### Installing from PyPI

The recommended Shakedown installation method is via the PyPI Python Package Index repository at [https://pypi.python.org/pypi/dcos-shakedown](https://pypi.python.org/pypi/dcos-shakedown).  To install the latest version and all required modules:

`pip install dcos-shakedown`

### Bleeding edge

To pull and install from our `master` branch on GitHub:

```
git clone github.com:mesosphere/shakedown.git
cd shakedown
pip install -e .
```

### Setting up a new Shakedown virtual environment

If you'd like to isolate your Shakedown Python environment, you can do so using the [virtualenv](https://pypi.python.org/pypi/virtualenv) tool.  To create a new virtual environment in `$HOME/shakedown`:

```
pip install virtualenv
virtualenv $HOME/shakedown
source $HOME/shakedown/bin/activate
pip install dcos-shakedown
```

This virtual environment can then be activated in new terminal sessions with:

`source $HOME/shakedown/bin/activate`


## Usage

`shakedown --dcos-url=http://dcos.example.com [options] [path_to_tests]`

- `--dcos-url` is required.
- tests within the current working directory will be auto-discovered unless specified.
- arguments can be stored in a `~/.shakedown` [TOML](https://github.com/toml-lang/toml) file (command-line takes precedence)
- `shakedown --help` is your friend.


## Helper methods

`shakedown` is a testing tool as well as a library.  Many helper functions are available via `from shakedown import *` in your tests.  See the [API documentation](API.md) for more information.


## License

Shakedown is licensed under the Apache License, Version 2.0.  For additional information, see the [LICENSE](LICENSE) file included at the root of this repository.


## Reporting Issues

Please report issues and submit feature requests for Shakedown by [creating an issue in the DC/OS JIRA with the "shakedown" component](https://dcosjira.atlassian.net/secure/CreateIssueDetails!init.jspa?pid=10001&issuetype=10003&components=10700).

## Contributing

See the [CONTRIBUTING](CONTRIBUTING.md) file in the root of this repository.
