import click
from ..base import BaseCommand
from ...core.exceptions import error_handler
from ...config.config_manager import ConfigurationManager

class SetCommand(BaseCommand):
    def execute(self, key: str, value: str) -> bool:
        try:
            self.info(f"설정 값 변경: {key} = {value}")
            config_manager = ConfigurationManager()
            
            # key가 점(.)으로 구분된 경우 중첩된 설정으로 처리
            keys = key.split('.')
            config = config_manager.load() or {}
            
            # 중첩된 딕셔너리 생성
            current = config
            for k in keys[:-1]:
                current = current.setdefault(k, {})
            current[keys[-1]] = value
            
            if config_manager.save(config):
                self.success(f"설정이 변경되었습니다: {key} = {value}")
                return True
            return False
            
        except Exception as e:
            self.error(f"설정 변경 실패: {str(e)}")
            return False

@click.command(name='set')
@click.argument('key')
@click.argument('value')
@error_handler()
def set(key: str, value: str):
    """설정 값 변경"""
    command = SetCommand()
    return command.execute(key, value) 