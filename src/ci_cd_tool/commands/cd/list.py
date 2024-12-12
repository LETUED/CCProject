import click
from rich.console import Console
from rich.table import Table
from ..base import BaseCommand
from ...core.exceptions import error_handler
from typing import Optional

class ListCommand(BaseCommand):
    def execute(self, repo: Optional[str] = None) -> bool:
        try:
            cd_service = self.container.cd_service()
            
            if repo == 'all':
                # 전체 리포지토리 목록 조회
                repositories = cd_service.list_repositories()
                self.create_repositories_table(repositories)
            else:
                # 특정 리포지토리의 이미지 목록 조회
                images = cd_service.list_versions(repo)
                self.create_images_table(images)
            
            return True
                
        except Exception as e:
            self.error(f"버전 목록 조회 실패: {str(e)}")
            return False

    def create_repositories_table(self, repositories):
        """리포지토리 목록을 테이블로 표시"""
        table = Table(title="ECR 리포지토리 목록")
        table.add_column("리포지토리 이름", style="cyan")
        table.add_column("URI", style="green")
        table.add_column("생성일", style="yellow")
        
        for repo in repositories:
            table.add_row(
                repo['repositoryName'],
                repo['repositoryUri'],
                repo['createdAt'].strftime("%Y-%m-%d %H:%M:%S")
            )
        
        console = Console()
        console.print(table)

    def create_images_table(self, images):
        """이미지 목록을 테이블로 표시"""
        table = Table(title="ECR 이미지 목록")
        table.add_column("태그", style="cyan")
        table.add_column("다이제스트", style="green")
        table.add_column("푸시 일시", style="yellow")
        table.add_column("크기", style="blue")
        
        for image in images:
            tags = image.get('imageTags', ['untagged'])
            table.add_row(
                ", ".join(tags),
                image['imageDigest'][:12],
                image['imagePushedAt'].strftime("%Y-%m-%d %H:%M:%S"),
                f"{image['imageSizeInBytes'] / 1024 / 1024:.1f}MB"
            )
        
        console = Console()
        console.print(table)

@click.command(name='list')
@click.option('--repo', help='리포지토리 이름 (all: 전체 목록)')
@error_handler()
def list_command(repo: Optional[str] = None):
    """배포 가능한 버전 목록 조회"""
    command = ListCommand()
    return command.execute(repo)

__all__ = ['list_command'] 