import click
from ..base import BaseCommand
from ...core.exceptions import error_handler
import git

class InitCommand(BaseCommand):
    def execute(self, path: str = ".") -> bool:
        try:
            self.info(f"Git 저장소 초기화 중: {path}")
            git.Repo.init(path)
            self.success("Git 저장소가 초기화되었습니다.")
            return True
        except Exception as e:
            self.error(f"Git 저장소 초기화 실패: {str(e)}")
            return False

@click.command(name='init')
@click.argument('path', default=".")
@error_handler()
def init(path: str):
    """Git 저장소 초기화"""
    command = InitCommand()
    return command.execute(path) 