import click
from ..base import BaseCommand
from ...core.exceptions import error_handler
import git

class CommitCommand(BaseCommand):
    def execute(self, message: str) -> bool:
        try:
            repo = git.Repo(".")
            self.info("변경사항 커밋 중...")
            repo.index.commit(message)
            self.success("변경사항이 커밋되었습니다.")
            return True
        except Exception as e:
            self.error(f"커밋 실패: {str(e)}")
            return False

@click.command(name='commit')
@click.option('-m', '--message', required=True, help='커밋 메시지')
@error_handler()
def commit(message: str):
    """변경사항을 커밋"""
    command = CommitCommand()
    return command.execute(message) 