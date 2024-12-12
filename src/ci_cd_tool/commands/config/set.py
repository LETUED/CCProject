import click
from typing import Optional
from ..base import BaseCommand
from ...config.config_manager import ConfigManager
from ...core.exceptions import error_handler

class SetCommand(BaseCommand):
    """설정 값 저장 명령어"""
    
    def execute(self, key: str, value: str) -> bool:
        try:
            self.info(f"설정 저장: {key}={value}")
            
            config = self.container.config()
            config.set_value(key, value)
            
            self.success(f"설정이 저장되었습니다: {key}={value}")
            return True
                
        except Exception as e:
            self.error(f"설정 저장 실패: {str(e)}")
            return False

@click.command()
@click.argument('key')
@click.argument('value')
@error_handler()
def set_command(key: str, value: str):
    """설정 값 저장"""
    command = SetCommand()
    return command.execute(key, value)

__all__ = ['set_command'] 