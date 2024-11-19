from typing import List, Optional
from github import Github
from rich.console import Console

class GitHubService:
    def __init__(self, base_url: str, token: str, owner: str, repo: str):
        self.github = Github(token)
        self.repo = self.github.get_repo(f"{owner}/{repo}")
        self.console = Console()

    def get_pipeline_runs(self, branch: str = "main", limit: int = 5) -> List[dict]:
        workflows = self.repo.get_workflows()
        runs = []
        
        for workflow in workflows:
            for run in workflow.get_runs(branch=branch)[:limit]:
                runs.append({
                    "id": run.id,
                    "name": workflow.name,
                    "status": run.status,
                    "conclusion": run.conclusion,
                    "created_at": run.created_at,
                    "url": run.html_url
                })
        return runs 