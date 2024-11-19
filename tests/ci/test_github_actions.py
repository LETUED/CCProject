import pytest
from ci_cd_tool.commands.ci_commands import ci_group
from ci_cd_tool.core.exceptions import CLIError

def test_ci_test_command(cli_runner):
    # Given/When
    result = cli_runner.invoke(ci_group, ['test', '--env', 'staging', '--fast'])
    
    # Then
    assert result.exit_code == 0
    assert "테스트 실행 중" in result.output

def test_ci_build_command(cli_runner):
    # Given/When
    result = cli_runner.invoke(ci_group, ['build'])
    
    # Then
    assert result.exit_code == 0
    assert "빌드를 시작합니다" in result.output 