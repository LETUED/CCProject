import pytest
from ci_cd_tool.commands.cd_commands import cd_group

def test_cd_deploy_command(cli_runner):
    # Given/When
    result = cli_runner.invoke(cd_group, ['deploy', '--env', 'staging', '--version', '1.0.0'])
    
    # Then
    assert result.exit_code == 0
    assert "배포가 시작되었습니다" in result.output

def test_cd_rollback_command(cli_runner):
    # Given/When
    result = cli_runner.invoke(cd_group, ['rollback', '--version', '0.9.0'])
    
    # Then
    assert result.exit_code == 0
    assert "롤백이 시작되었습니다" in result.output