import click
from ..base import BaseCommand
from ...core.exceptions import error_handler
import git
from typing import List

class AddCommand(BaseCommand):
    def execute(self, files: List[str]) -> bool:
        try:
            repo = git.Repo(".")
            self.info(f"파일 스테이징 중: {', '.join(files)}")
            repo.index.add(files)
            self.success("파일이 스테이징되었습니다.")
            return True
        except Exception as e:
            self.error(f"파일 스테이징 실패: {str(e)}")
            return False

@click.command(name='add')
@click.argument('files', nargs=-1, required=True)
@error_handler()
def add(files: List[str]):
    """파일을 스테이징 영역에 추가"""
    command = AddCommand()
    return command.execute(files) 