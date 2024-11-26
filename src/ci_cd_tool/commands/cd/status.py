import click
from ..base import BaseCommand
from ...core.exceptions import error_handler
from rich.table import Table
from typing import Optional

class StatusCommand(BaseCommand):
    def execute(self, env: Optional[str] = None) -> bool:
        try:
            deploy_service = self.container.deploy_service()
            
            if env:
                status = deploy_service.get_status(env)
                self._show_env_status(env, status)
            else:
                # 모든 환경의 상태 표시
                for env in ['dev', 'staging', 'prod']:
                    try:
                        status = deploy_service.get_status(env)
                        self._show_env_status(env, status)
                    except Exception as e:
                        self.warning(f"{env} 환경 상태 조회 실패: {str(e)}")
                        
            return True
            
        except Exception as e:
            self.error(f"상태 조회 중 오류 발생: {str(e)}")
            return False
            
    def _show_env_status(self, env: str, status) -> None:
        table = Table(title=f"{env} 환경 배포 상태")
        table.add_column("항목", style="cyan")
        table.add_column("상태", style="green")
        
        table.add_row("현재 버전", status.current_version)
        table.add_row("배포 상태", status.status)
        table.add_row("마지막 배포", status.last_deployed)
        table.add_row("배포자", status.deployer)
        table.add_row("서비스 상태", status.health)
        table.add_row("실행 인스턴스", str(status.instance_count))
        
        self.console.print(table)
        self.console.print("")  # 빈 줄 추가

@click.command()
@click.option('--env', help='환경 지정 (생략시 전체 환경)')
@error_handler()
def status(env: Optional[str]):
    """CD 상태 확인"""
    command = StatusCommand()
    return command.execute(env) 