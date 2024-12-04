import click
from ..base import BaseCommand
from ...core.exceptions import error_handler
import git
from rich.table import Table

class StatusCommand(BaseCommand):
    def execute(self) -> bool:
        try:
            repo = git.Repo(".")
            
            # 상태 테이블 생성
            table = Table(title="Git 상태")
            table.add_column("상태", style="cyan")
            table.add_column("파일", style="green")
            
            # 수정된 파일
            for item in repo.index.diff(None):
                table.add_row("수정됨", item.a_path)
            
            # 추적되지 않는 파일
            for item in repo.untracked_files:
                table.add_row("추적되지 않음", item)
            
            self.console.print(table)
            return True
            
        except Exception as e:
            self.error(f"상태 확인 실패: {str(e)}")
            return False

@click.command(name='status')
@error_handler()
def status():
    """Git 저장소 상태 확인"""
    command = StatusCommand()
    return command.execute() 