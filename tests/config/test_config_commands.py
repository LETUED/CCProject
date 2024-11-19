import pytest
from ci_cd_tool.commands import config_group

@pytest.fixture
def config_manager():
    from ci_cd_tool.config.config_manager import ConfigurationManager
    return ConfigurationManager()

def test_config_init_command(cli_runner):
    # Given/When
    result = cli_runner.invoke(config_group, ['init'])
    
    # Then
    assert result.exit_code == 0
    assert "설정 초기화" in result.output

def test_config_show_command(cli_runner):
    # Given/When
    result = cli_runner.invoke(config_group, ['show'])
    
    # Then
    assert result.exit_code == 0
    assert "현재 설정" in result.output 