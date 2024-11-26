import pytest
from click.testing import CliRunner
from unittest.mock import Mock, patch
from ci_cd_tool.commands.ci.test import test, TestCommand
from ci_cd_tool.core.container import Container
from ci_cd_tool.services.test_service import TestService
from ci_cd_tool.core.test_config import TestConfig
from pathlib import Path

@pytest.fixture
def cli_runner():
    return CliRunner()

@pytest.fixture
def mock_test_service():
    test_service = Mock(spec=TestService)
    test_service.run_tests.return_value = True
    test_service._detect_environment.return_value = 'staging'
    return test_service

@pytest.fixture
def mock_container(mock_test_service):
    container = Mock(spec=Container)
    container.test_service.return_value = mock_test_service
    return container

class TestCITestCommand:
    def test_basic_test_execution(self, cli_runner, mock_container):
        """기본 테스트 실행"""
        with patch('ci_cd_tool.commands.ci.test.TestCommand') as MockTestCommand:
            instance = MockTestCommand.return_value
            instance.container = mock_container
            instance.execute.return_value = True
            
            result = cli_runner.invoke(test)
            
            assert result.exit_code == 0
            instance.execute.assert_called_once_with(None, None, False)

    def test_test_with_module(self, cli_runner, mock_container):
        """모듈 지정 테스트"""
        with patch('ci_cd_tool.commands.ci.test.TestCommand') as MockTestCommand:
            instance = MockTestCommand.return_value
            instance.container = mock_container
            instance.execute.return_value = True
            
            result = cli_runner.invoke(test, ['auth'])
            
            assert result.exit_code == 0
            instance.execute.assert_called_once_with(None, None, False)

    def test_test_with_env(self, cli_runner, mock_container):
        """환경 지정 테스트"""
        with patch('ci_cd_tool.commands.ci.test.TestCommand') as MockTestCommand:
            instance = MockTestCommand.return_value
            instance.container = mock_container
            instance.execute.return_value = True
            
            result = cli_runner.invoke(test, ['--env', 'dev'])
            
            assert result.exit_code == 0
            instance.execute.assert_called_once_with(None, None, False)

    def test_test_with_report(self, cli_runner, mock_container):
        """리포트 생성 테스트"""
        with patch('ci_cd_tool.commands.ci.test.TestCommand') as MockTestCommand:
            instance = MockTestCommand.return_value
            instance.container = mock_container
            instance.execute.return_value = True
            
            result = cli_runner.invoke(test, ['--report'])
            
            assert result.exit_code == 0
            instance.execute.assert_called_once_with(None, None, False)

    def test_test_failure(self, cli_runner, mock_container):
        """테스트 실패 케이스"""
        mock_container.test_service.return_value.run_tests.return_value = False
        with patch('ci_cd_tool.commands.ci.test.TestCommand') as MockTestCommand:
            instance = MockTestCommand.return_value
            instance.container = mock_container
            instance.execute.return_value = False
            
            result = cli_runner.invoke(test)
            
            assert result.exit_code == 1

    def test_test_command_error(self, cli_runner, mock_container):
        """테스트 실행 중 에러 발생 케이스"""
        mock_container.test_service.return_value.run_tests.side_effect = Exception("테스트 오류")
        with patch('ci_cd_tool.commands.ci.test.TestCommand') as MockTestCommand:
            instance = MockTestCommand.return_value
            instance.container = mock_container
            instance.execute.return_value = False
            
            result = cli_runner.invoke(test)
            
            assert result.exit_code == 1

    def test_environment_auto_detection(self, cli_runner, mock_container):
        """환경 자동 감지 테스트"""
        mock_container.test_service.return_value._detect_environment.return_value = 'dev'
        with patch('ci_cd_tool.commands.ci.test.TestCommand') as MockTestCommand:
            instance = MockTestCommand.return_value
            instance.container = mock_container
            instance.execute.return_value = True
            
            result = cli_runner.invoke(test)
            
            assert result.exit_code == 0
            instance.execute.assert_called_once_with(None, None, False)
            test_service = mock_container.test_service.return_value
            test_service._detect_environment.assert_called_once()
            config = test_service.run_tests.call_args[0][0]
            assert config.env == 'staging' 