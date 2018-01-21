# -*- coding: utf-8 -*-
#
# Copyright © Spyder Project Contributors
# Licensed under the terms of the MIT License
#

"""
File for running tests programmatically.
"""

# Standard library imports
import os
import os.path as osp
import shutil

# Third party imports
import qtpy  # to ensure that Qt4 uses API v2
import pytest


# To activate/deactivate certain things for pytest's only
os.environ['SPYDER_PYTEST'] = 'True'

# Tests expect English as the interface language
os.environ['LANG'] = 'en'

# To run our slow tests only in our CIs
run_slow = False
if os.environ.get('CI', None) is not None:
    run_slow = True


def main():
    """
    Run pytest tests.
    """
    # Remove temp conf_dir before starting the tests
    from spyder.config.base import get_conf_path
    conf_dir = get_conf_path()
    if osp.isdir(conf_dir):
        shutil.rmtree(conf_dir)

    pytest_args = ['spyder',
                   'spyder_profiler',
                   '-x',
                   '-vv',
                   '-rw',
                   '--durations=10',
                   '--cov=spyder',
                   '--cov=spyder_profiler',
                   '--cov-report=term-missing']

    if run_slow:
        pytest_args.append('--run-slow')

    errno = pytest.main(pytest_args)

    # sys.exit doesn't work here because some things could be running
    # in the background (e.g. closing the main window) when this point
    # is reached. And if that's the case, sys.exit does't stop the
    # script (as you would expected).
    if errno != 0:
        raise SystemExit(errno)


if __name__ == '__main__':
    main()
