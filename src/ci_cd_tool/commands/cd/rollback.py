import click
from ..base import BaseCommand
from ...core.exceptions import error_handler
from typing import Optional

class RollbackCommand(BaseCommand):
    """롤백 명령어 처리"""
    
    def execute(self, version: str, env: Optional[str] = None) -> bool:
        try:
            if env:
                self.info(f"롤백 시작 - 환경: {env}, 버전: {version}")
            else:
                self.info(f"롤백 시작 - 버전: {version}")
            
            rollback_service = self.container.rollback_service()
            result = rollback_service.rollback(version, env)
            
            if result:
                self.success("롤백이 성공적으로 완료되었습니다")
                return True
            else:
                self.error("롤백 중 오류가 발생했습니다")
                return False
                
        except Exception as e:
            self.error(f"롤백 실패: {str(e)}")
            return False

@click.command(name='rollback')
@click.option('--version', required=True, help='롤백할 버전')
@click.option('--env', required=False, help='환경 설정 (선택사항)')
@error_handler()
def rollback_command(version: str, env: Optional[str] = None):
    """이전 버전으로 롤백 실행"""
    command = RollbackCommand()
    return command.execute(version, env)

__all__ = ['rollback_command'] 