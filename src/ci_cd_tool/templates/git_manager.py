import os
import git
from rich.console import Console
from ..core.exceptions import GitHubError

class GitManager:
    def __init__(self, ci_tool: str, template_file: str, project_root: str):
        self.ci_tool = ci_tool
        self.template_file = template_file
        self.project_root = project_root
        self.console = Console()

    def commit_and_push(self) -> None:
        """Git 커밋 및 푸시"""
        try:
            repo = git.Repo(self.project_root)
            
            if not os.path.exists(self.template_file):
                self.console.print(f"[yellow]템플릿 파일을 찾을 수 없습니다: {self.template_file}[/yellow]")
                return

            repo.index.add([self.template_file])
            commit_message = f"chore: Add {self.ci_tool} CI configuration"
            repo.index.commit(commit_message)
            
            origin = repo.remote(name='origin')
            origin.push()

            self.console.print(f"[green]{self.ci_tool} CI 템플릿 파일이 커밋되고 푸시되었습니다.[/green]")
            
        except git.exc.InvalidGitRepositoryError:
            self.console.print("[red]유효한 Git 리포지토리가 아닙니다. 먼저 Git 리포지토리를 초기화하세요.[/red]")
        except Exception as e:
            raise GitHubError(f"Git 작업 중 오류 발생: {str(e)}") 