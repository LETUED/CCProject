import click
from ..base import BaseCommand
from ...core.exceptions import error_handler
from typing import Optional

class RollbackCommand(BaseCommand):
    def execute(self, version: Optional[str] = None) -> bool:
        try:
            deploy_service = self.container.deploy_service()
            
            # 버전이 지정되지 않은 경우 이전 버전 조회
            if not version:
                versions = deploy_service.list_versions()
                if len(versions) < 2:
                    self.error("롤백할 이전 버전이 없습니다.")
                    return False
                version = versions[-2]  # 현재 버전 이전의 버전 선택
            
            # 롤백 실행
            self.info(f"버전 {version}으로 롤백 시작...")
            deploy_service.deploy(version)
            
            self.success(f"버전 {version}으로 롤백이 완료되었습니다.")
            return True
            
        except Exception as e:
            self.error(f"롤백 중 오류 발생: {str(e)}")
            return False

@click.command(name='rollback')
@click.option('--version', help='롤백할 버전 (미지정시 직전 버전)')
@error_handler()
def rollback(version: Optional[str]):
    """이전 버전으로 롤백"""
    command = RollbackCommand()
    return command.execute(version) 