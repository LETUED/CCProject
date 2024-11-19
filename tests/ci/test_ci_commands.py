import pytest
from click.testing import CliRunner
from ci_cd_tool.commands import ci_group

def test_ci_test_command(cli_runner):
    result = cli_runner.invoke(ci_group, ['test', '--env', 'staging'])
    assert result.exit_code == 0
    assert "테스트 실행 중" in result.output
    assert "환경: staging" in result.output

def test_ci_test_with_fast_option(cli_runner):
    result = cli_runner.invoke(ci_group, ['test', '--fast'])
    assert result.exit_code == 0
    assert "테스트 실행 중" in result.output
    assert "빠른 테스트 모드" in result.output 