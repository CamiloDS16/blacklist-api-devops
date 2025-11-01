import pytest
import os

os.environ['TESTING'] = 'True'

@pytest.fixture(scope='session', autouse=True)
def setup_test_environment():
    pass

