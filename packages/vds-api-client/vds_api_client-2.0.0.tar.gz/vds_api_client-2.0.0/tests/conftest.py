
from __future__ import print_function, absolute_import, division

import os
import pytest
import shutil
import time
from click.testing import CliRunner


@pytest.fixture
def save_dir():
    """
    Get the same savedir back for all tests
    """
    directory = os.path.join(os.environ.get('TEMP', os.environ.get('TMP', '/tmp')), 'api_testdata')
    try:
        os.mkdir(directory)
    except OSError:
        pass
    return directory


@pytest.fixture
def empty_save_dir():
    """
    Get the same savedir back for all tests, but empty after initialization
    """
    directory = os.path.join(os.environ.get('TEMP', os.environ.get('TMP', '/tmp')), 'api_testdata')
    if os.path.exists(directory):
        shutil.rmtree(directory, ignore_errors=True)
    t1 = time.time()
    while time.time() - t1 < 1:
        try:
            os.mkdir(directory)
        except OSError:
            time.sleep(0.01)
    if not os.path.exists(directory):
        raise OSError('empty_save_dir not created')
    return directory


@pytest.fixture
def credentials():
    """
    Get the credentials stored in the environent variables `$VDS_USER` and `$VDS_PASS`
    """
    creds = {'user': os.environ.get('VDS_USER'), 'pw': os.environ.get('VDS_PASS')}
    return creds


@pytest.fixture
def example_config_v1():
    """
    Get the configuration for Aa en Maas downloads
    """
    filename = os.path.join('tests', 'config_files', 'example_config_v1.vds')
    return filename


@pytest.fixture
def example_config_v2():
    """
    Get the configuration for Aa en Maas downloads
    """
    filename = os.path.join('tests', 'config_files', 'example_config_v2.vds')
    return filename


@pytest.fixture
def runner():
    """
    Get the cli runner
    """
    return CliRunner()

# EOF
