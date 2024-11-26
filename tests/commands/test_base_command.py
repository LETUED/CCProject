import pytest
from unittest.mock import Mock, patch
from rich.console import Console
from ci_cd_tool.commands.base import BaseCommand
from ci_cd_tool.core.container import Container

class TestBaseCommand(BaseCommand):
    def execute(self, *args, **kwargs) -> bool:
        return True

@pytest.fixture
def base_command():
    return TestBaseCommand()

def test_base_command_initialization():
    command = TestBaseCommand()
    assert isinstance(command.console, Console)
    assert isinstance(command.container, Container)
    assert command.logger is not None

def test_message_outputs(base_command, caplog):
    # 메시지 출력 테스트
    base_command.info("정보 메시지")
    assert "정보 메시지" in caplog.text
    
    base_command.success("성공 메시지")
    assert "성공 메시지" in caplog.text
    
    base_command.warning("경고 메시지")
    assert "경고 메시지" in caplog.text
    
    base_command.error("에러 메시지")
    assert "에러 메시지" in caplog.text 