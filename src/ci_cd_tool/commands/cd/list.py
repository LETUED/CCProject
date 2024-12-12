import click
from ..base import BaseCommand
from ...core.exceptions import error_handler
from ...services.cd_service import CDService

class ListCommand(BaseCommand):
    def execute(self, env: str = None, repo: str = None) -> bool:
        try:
            cd_service = CDService()
            
            if repo:
                # 리포지토리 목록 또는 특정 리포지토리 정보 조회
                if repo == 'all':
                    repositories = cd_service.list_repositories()
                    self._display_repositories(repositories)
                else:
                    images = cd_service.list_images(repo)
                    self._display_images(images, repo)
            else:
                # 기본 동작: 기본 리포지토리의 이미지 목록 조회
                images = cd_service.list_images()
                self._display_images(images)
                
            return True
            
        except Exception as e:
            self.error(f"버전 목록 조회 실패: {str(e)}")
            return False
            
    def _display_repositories(self, repositories):
        """리포지토리 목록 표시"""
        table = self.create_table("ECR 리포지토리 목록")
        table.add_column("리포지토리명", style="cyan")
        table.add_column("URI", style="green")
        table.add_column("생성일", style="yellow")
        
        for repo in repositories:
            table.add_row(
                repo['repositoryName'],
                repo['repositoryUri'],
                repo['createdAt'].strftime("%Y-%m-%d %H:%M:%S")
            )
            
        self.console.print(table)
        
    def _display_images(self, images, repo_name=None):
        """이미지 목록 표시"""
        title = f"{'ECR 이미지 목록' if not repo_name else f'리포지토리 {repo_name}의 이미지 목록'}"
        table = self.create_table(title)
        table.add_column("태그", style="cyan")
        table.add_column("다이제스트", style="green")
        table.add_column("크기", style="yellow")
        table.add_column("푸시 일시", style="magenta")
        
        for image in images:
            table.add_row(
                ", ".join(image.get('imageTags', ['<untagged>']),
                image['imageDigest'][:12],
                f"{image['imageSizeInBytes'] / 1024 / 1024:.1f}MB",
                image['imagePushedAt'].strftime("%Y-%m-%d %H:%M:%S")
            )
            
        self.console.print(table)

@click.command(name='list')
@click.option('--env', help='환경 필터링')
@click.option('--repo', help='리포지토리 이름 (all: 전체 목록)')
@error_handler()
def list_command(env: str = None, repo: str = None):
    """배포 가능한 버전 목록 조회"""
    command = ListCommand()
    return command.execute(env, repo) 