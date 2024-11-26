from typing import Optional
import click
from ..base import BaseCommand
from ...core.exceptions import error_handler
from ...services.ci_service import CIService, CIConfig
from ...config.config_manager import ConfigurationManager

class BuildCommand(BaseCommand):
    """CI 파이프라인의 빌드 단계 실행"""
    
    def execute(self, env: Optional[str] = None) -> bool:
        try:
            self.info("CI 파이프라인 빌드 단계 시작")
            
            ci_service = CIService(self.console)
            config_manager = ConfigurationManager()
            settings = config_manager.load()
            
            provider = settings.get('ci', {}).get('provider', 'github')
            
            config = CIConfig(
                stage="build",
                provider=provider,
                config_path=".github/workflows",
                environment=env
            )
            
            return ci_service.run_stage(config)
                
        except Exception as e:
            self.error(f"빌드 단계 실행 중 오류 발생: {str(e)}")
            return False

@click.command(name='build')
@click.option('--env', help='실행 환경 설정')
@error_handler()
def build(env: Optional[str]):
    """CI 파이프라인의 빌드 단계를 실행합니다."""
    command = BuildCommand()
    return command.execute(env=env) 