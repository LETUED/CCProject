import pytest
from click.testing import CliRunner
from ci_cd_tool.config.config_manager import ConfigurationManager

@pytest.fixture
def cli_runner():
    return CliRunner()

@pytest.fixture
def config_manager():
    return ConfigurationManager() 