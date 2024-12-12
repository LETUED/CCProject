import click
from ..base import BaseCommand
from ...core.exceptions import error_handler
from ...config.manager import ConfigManager

class GetCommand(BaseCommand):
    """설정 값 조회 명령어"""
    
    def execute(self, key: str) -> bool:
        try:
            config_manager = ConfigManager()
            value = config_manager.get_value(key)
            
            if value is None:
                self.error(f"설정 키를 찾을 수 없습니다: {key}")
                return False
                
            self.info(f"{key} = {value}")
            return True
                
        except Exception as e:
            self.error(f"설정 값 조회 중 오류 발생: {str(e)}")
            return False

@click.command(name='get')
@click.argument('key')
@error_handler()
def get_command(key: str):
    """설정 값 조회"""
    command = GetCommand()
    return command.execute(key)

__all__ = ['get_command'] 