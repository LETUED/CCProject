import pytest
from unittest.mock import Mock, patch
from ci_cd_tool.commands.test.run import TestRunCommand
from ci_cd_tool.services.test_service import TestConfig

@pytest.fixture
def test_command():
    return TestRunCommand()

@pytest.fixture
def mock_test_service():
    with patch('ci_cd_tool.core.container.Container.test_service') as mock:
        service = Mock()
        mock.return_value = service
        yield service

def test_execute_success(test_command, mock_test_service):
    # 테스트 성공 시나리오
    mock_test_service.run_tests.return_value = True
    
    result = test_command.execute(
        module="auth",
        env="dev",
        report=True
    )
    
    assert result is True
    mock_test_service.run_tests.assert_called_once()
    called_config = mock_test_service.run_tests.call_args[0][0]
    assert isinstance(called_config, TestConfig)
    assert called_config.test_dir == "unittest/auth"
    assert called_config.env == "dev"
    assert called_config.report is True

def test_execute_failure(test_command, mock_test_service):
    # 테스트 실패 시나리오
    mock_test_service.run_tests.return_value = False
    
    result = test_command.execute(
        module=None,
        env=None,
        report=False
    )
    
    assert result is False
    mock_test_service.run_tests.assert_called_once()
    called_config = mock_test_service.run_tests.call_args[0][0]
    assert called_config.test_dir == "unittest"
    assert called_config.env is None
    assert called_config.report is False

def test_execute_exception(test_command, mock_test_service):
    # 예외 발생 시나리오
    mock_test_service.run_tests.side_effect = Exception("테스트 실행 오류")
    
    result = test_command.execute(
        module="auth",
        env="dev",
        report=True
    )
    
    assert result is False 