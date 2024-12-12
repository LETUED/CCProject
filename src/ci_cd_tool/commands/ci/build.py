from typing import Optional
import click
from ..base import BaseCommand
from ...core.exceptions import error_handler
from ...services.ci_service import CIService, CIConfig
from ...config.config_manager import ConfigManager

class BuildCommand(BaseCommand):
    """빌드 명령어"""
    
    def execute(self, stage: str, env: Optional[str] = None) -> bool:
        try:
            self.info(f"빌드 시작: {stage}")
            
            config = CIConfig(
                stage=stage,
                provider='local',
                config_path='.cc/config.yml',
                environment=env
            )
            
            ci_service = self.container.ci_service()
            return ci_service.build(config)
                
        except Exception as e:
            self.error(f"빌드 실패: {str(e)}")
            return False

@click.command()
@click.argument('stage')
@click.option('--env', help='환경 지정 (예: dev, staging, prod)')
@error_handler()
def build(stage: str, env: Optional[str] = None):
    """빌드 실행"""
    command = BuildCommand()
    return command.execute(stage, env)

__all__ = ['build'] 