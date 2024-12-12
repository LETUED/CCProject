import click
from ..base import BaseCommand
from ...core.exceptions import error_handler
from git import Repo
from git.exc import GitCommandError

class PushCommand(BaseCommand):
    """소스 코드 푸시 명령어"""
    
    def execute(self, remote: str = 'origin', branch: str = None) -> bool:
        try:
            self.info(f"변경사항을 {remote}로 푸시 중...")
            
            repo = Repo('.')
            current_branch = repo.active_branch.name
            
            if not branch:
                branch = current_branch
                
            # 원격 저장소 확인
            try:
                remote_repo = repo.remote(remote)
            except ValueError:
                self.error(f"원격 저장소 '{remote}'를 찾을 수 없습니다.")
                return False
                
            # upstream 브랜치가 없는 경우 강제로 푸시
            try:
                self.info(f"{remote}/{branch}로 푸시 중...")
                remote_repo.push(refspec=f"{current_branch}:{branch}", force=True)
                self.success(f"{remote}/{branch}로 성공적으로 푸시되었습니다")
                return True
                
            except GitCommandError as e:
                # 원격 브랜치가 없는 경우
                if "remote ref does not exist" in str(e):
                    try:
                        self.info(f"원격 브랜치 생성 중: {remote}/{branch}")
                        remote_repo.push(refspec=f"{current_branch}:{branch}")
                        self.success(f"새 브랜치 {remote}/{branch}가 생성되었습니다")
                        return True
                    except GitCommandError as e2:
                        self.error(f"브랜치 생성 실패: {str(e2)}")
                        return False
                else:
                    self.error(f"푸시 실패: {str(e)}")
                    return False
                    
        except Exception as e:
            self.error(f"푸시 실패: {str(e)}")
            return False

@click.command()
@click.option('--remote', default='origin', help='원격 저장소 이름')
@click.option('--branch', help='푸시할 브랜치 이름')
@error_handler()
def push(remote: str, branch: str = None):
    """현재 브랜치의 변경사항을 원격 저장소로 푸시"""
    command = PushCommand()
    return command.execute(remote, branch)

__all__ = ['push'] 