import pytest
from ci_cd_tool.commands.ci import ci_group
from ci_cd_tool.ci.github_actions import GitHubActionsCI
from unittest.mock import patch, MagicMock

def test_ci_test_command(cli_runner):
    """GitHub Actions 테스트 명령어"""
    result = cli_runner.invoke(ci_group, [
        'test', 
        '--env', 'staging'
    ])
    
    assert result.exit_code == 0
    assert "테스트 실행 중" in result.output

@pytest.fixture
def github_actions():
    config = {
        'config_path': '.github/workflows/ci.yml',
        'environment': 'staging'
    }
    return GitHubActionsCI(config)

def test_create_pipeline(github_actions, tmp_path):
    """파이프라인 생성 테스트"""
    with patch('os.path.exists') as mock_exists:
        mock_exists.return_value = False
        
        assert github_actions.create_pipeline() == True
        assert "GitHub Actions workflow 생성" in github_actions.console.file.getvalue()

def test_run_tests_success(github_actions):
    """테스트 실행 성공 케이스"""
    with patch('unittest.TestLoader') as mock_loader:
        mock_suite = MagicMock()
        mock_result = MagicMock()
        mock_result.wasSuccessful.return_value = True
        mock_suite.run.return_value = mock_result
        mock_loader.return_value.discover.return_value = mock_suite
        
        test_config = {'test_dir': 'tests'}
        assert github_actions.run_tests(test_config) == True

def test_run_tests_failure(github_actions):
    """테스트 실행 실패 케이스"""
    with patch('unittest.TestLoader') as mock_loader:
        mock_suite = MagicMock()
        mock_result = MagicMock()
        mock_result.wasSuccessful.return_value = False
        mock_result.failures = [1]
        mock_result.errors = [1]
        mock_suite.run.return_value = mock_result
        mock_loader.return_value.discover.return_value = mock_suite
        
        test_config = {'test_dir': 'tests'}
        assert github_actions.run_tests(test_config) == False

def test_get_status(github_actions):
    """상태 조회 테스트"""
    status = github_actions.get_status()
    assert status == "success"