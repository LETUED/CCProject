import pytest
from unittest.mock import Mock, patch
from ci_cd_tool.commands.cd.deploy import DeployCommand

@pytest.fixture
def deploy_command():
    return DeployCommand()

@pytest.fixture
def mock_deploy_service():
    with patch('ci_cd_tool.core.container.Container.deploy_service') as mock:
        service = Mock()
        mock.return_value = service
        yield service

def test_deploy_success(deploy_command, mock_deploy_service):
    # 배포 성공 시나리오
    mock_deploy_service.deploy.return_value = True
    
    result = deploy_command.execute(
        env="prod",
        version="1.0.0"
    )
    
    assert result is True
    mock_deploy_service.deploy.assert_called_once_with("prod", "1.0.0")

def test_deploy_failure(deploy_command, mock_deploy_service):
    # 배포 실패 시나리오
    mock_deploy_service.deploy.return_value = False
    
    result = deploy_command.execute(
        env="prod",
        version="1.0.0"
    )
    
    assert result is False

def test_deploy_exception(deploy_command, mock_deploy_service):
    # 예외 발생 시나리오
    mock_deploy_service.deploy.side_effect = Exception("배포 오류")
    
    result = deploy_command.execute(
        env="prod",
        version="1.0.0"
    )
    
    assert result is False 