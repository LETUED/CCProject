import click
from ..base import BaseCommand
from ...core.exceptions import error_handler
from rich.table import Table
from typing import Optional

class ListCommand(BaseCommand):
    def execute(self, env: Optional[str] = None) -> bool:
        try:
            deploy_service = self.container.deploy_service()
            versions = deploy_service.get_versions(env)
            
            table = Table(title="배포 가능한 버전 목록")
            table.add_column("버전", style="cyan")
            table.add_column("생성일", style="green")
            table.add_column("상태", style="yellow")
            table.add_column("환경", style="blue")
            
            for version in versions:
                table.add_row(
                    version.version_id,
                    version.created_at,
                    version.status,
                    version.environment or "모든 환경"
                )
                
            self.console.print(table)
            return True
            
        except Exception as e:
            self.error(f"버전 목록 조회 중 오류 발생: {str(e)}")
            return False

@click.command(name='list')
@click.option('--env', help='환경 지정')
@error_handler()
def list_versions(env: Optional[str]):
    """배포 가능한 버전 목록 조회"""
    command = ListCommand()
    return command.execute(env) 