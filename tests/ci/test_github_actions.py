import pytest
from ci_cd_tool.commands.ci import ci_group

def test_ci_test_command(cli_runner):
    """GitHub Actions 테스트 명령어"""
    result = cli_runner.invoke(ci_group, [
        'test', 
        '--env', 'staging'
    ])
    
    assert result.exit_code == 0
    assert "테스트 실행 중" in result.output 