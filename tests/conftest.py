import pytest
from click.testing import CliRunner

@pytest.fixture
def cli_runner():
    """CLI 테스트를 위한 fixture"""
    return CliRunner() 