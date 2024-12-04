import click
from ..base import BaseCommand
from ...core.exceptions import error_handler
import git

class PushCommand(BaseCommand):
    def execute(self, remote: str = "origin", branch: str = None) -> bool:
        try:
            repo = git.Repo(".")
            self.info(f"변경사항을 {remote}로 푸시 중...")
            if branch:
                repo.remote(remote).push(branch)
            else:
                repo.remote(remote).push()
            self.success("변경사항이 푸시되었습니다.")
            return True
        except Exception as e:
            self.error(f"푸시 실패: {str(e)}")
            return False

@click.command(name='push')
@click.option('--remote', default="origin", help='원격 저장소 이름')
@click.option('--branch', help='브랜치 이름')
@error_handler()
def push(remote: str, branch: str):
    """변경사항을 원격 저장소에 푸시"""
    command = PushCommand()
    return command.execute(remote, branch) 