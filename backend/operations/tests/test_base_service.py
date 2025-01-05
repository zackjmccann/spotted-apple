import os
import pytest
from app.services import base_service


@pytest.fixture
def base_service_abc():
    return base_service

def test_base_service(base_service_abc):
    test_value = base_service_abc._get_environment_variable('TEST_VALUE', 'int')
    assert test_value == int(os.environ['TEST_VALUE'])
