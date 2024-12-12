import click
from ..base import BaseCommand
from ...core.exceptions import error_handler
from typing import Optional

class DeployCommand(BaseCommand):
    """배포 명령어 처리"""
    
    def execute(self, env: str, version: str) -> bool:
        try:
            self.info(f"배포 시작 - 환경: {env}, 버전: {version}")
            
            deploy_service = self.container.deploy_service()
            result = deploy_service.deploy(env, version)
            
            if result:
                self.success("배포가 성공적으로 완료되었습니다")
                return True
            else:
                self.error("배포 중 오류가 발생했습니다")
                return False
                
        except Exception as e:
            self.error(f"배포 실패: {str(e)}")
            return False

@click.command(name='deploy')
@click.option('--env', required=True, help='배포할 환경 설정')
@click.option('--version', required=True, help='배포할 버전')
@error_handler()
def deploy_command(env: str, version: str):
    """환경별 배포 실행"""
    command = DeployCommand()
    return command.execute(env, version)

__all__ = ['deploy_command'] 