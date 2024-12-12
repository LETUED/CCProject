from typing import Optional
import click
from rich.table import Table
from ..base import BaseCommand
from ...core.exceptions import error_handler
from ...config.config_manager import ConfigManager
from ...services.ci_service import CIService

class StatusCommand(BaseCommand):
    """CI 상태 확인 명령어"""
    
    def execute(self, limit: Optional[int] = None) -> bool:
        try:
            self.info("CI 파이프라인 상태 확인")
            
            ci_service = self.container.ci_service()
            status = ci_service.status()
            
            if not status:
                self.warning("CI 파이프라인 정보가 없습니다")
                return True
                
            self._display_status(status, limit)
            return True
                
        except Exception as e:
            self.error(f"상태 확인 실패: {str(e)}")
            return False
            
    def _display_status(self, status: dict, limit: Optional[int] = None):
        """상태 정보를 테이블로 표시"""
        table = Table(title="CI 파이프라인 상태")
        
        table.add_column("단계", style="cyan")
        table.add_column("상태", style="green")
        table.add_column("시작 시간", style="yellow")
        table.add_column("종료 시간", style="yellow")
        
        stages = list(status.items())
        if limit:
            stages = stages[:limit]
            
        for stage, info in stages:
            table.add_row(
                stage,
                info.get('status', ''),
                info.get('start_time', ''),
                info.get('end_time', '')
            )
            
        self.console.print(table)

@click.command()
@click.option('--limit', type=int, help='표시할 항목 수 제한')
@error_handler()
def status(limit: Optional[int] = None):
    """CI 파이프라인 상태 확인"""
    command = StatusCommand()
    return command.execute(limit)

__all__ = ['status'] 