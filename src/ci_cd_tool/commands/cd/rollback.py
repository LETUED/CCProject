import click
from ..base import BaseCommand
from ...core.exceptions import error_handler

class RollbackCommand(BaseCommand):
    def execute(self, version: str) -> bool:
        try:
            self.info(f"롤백 시작 - 버전: {version}")
            
            deploy_service = self.container.deploy_service()
            result = deploy_service.rollback(version)
            
            if result:
                self.success("롤백이 성공적으로 완료되었습니다")
                return True
            else:
                self.error("롤백 중 오류가 발생했습니다")
                return False
                
        except Exception as e:
            self.error(f"롤백 실패: {str(e)}")
            return False

@click.command()
@click.option('--version', required=True, help='롤백할 버전')
@error_handler()
def rollback(version: str):
    """이전 버전으로 롤백"""
    command = RollbackCommand()
    return command.execute(version) 