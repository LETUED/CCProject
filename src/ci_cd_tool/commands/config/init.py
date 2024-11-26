import click
from ..base import BaseCommand
from ...core.exceptions import error_handler
from ...config.manager import ConfigManager

class InitCommand(BaseCommand):
    def execute(self) -> bool:
        try:
            self.info("기본 설정 초기화 중...")
            config_manager = ConfigManager()
            
            # 기본 설정 생성 및 저장
            default_config = config_manager.get_default_config()
            if config_manager.save(default_config):
                self.success("기본 설정이 초기화되었습니다")
                return True
            else:
                self.error("설정 저장 중 오류가 발생했습니다")
                return False
                
        except Exception as e:
            self.error(f"설정 초기화 실패: {str(e)}")
            return False

@click.command()
@error_handler()
def init():
    """기본 설정 초기화"""
    command = InitCommand()
    return command.execute() 