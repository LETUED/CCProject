from .base_ci import BaseCI
from dataclasses import dataclass
from typing import Dict

@dataclass
class JenkinsConfig:
    url: str
    username: str
    token: str
    job_name: str

class JenkinsCI(BaseCI):
    def __init__(self, config: JenkinsConfig):
        super().__init__()
        self.config = config
        
    def create_pipeline(self, config: Dict) -> bool:
        try:
            self.console.print("[yellow]Jenkins 파이프라인 생성 중...[/yellow]")
            jenkinsfile = self._generate_jenkinsfile(config)
            self._create_jenkins_job(jenkinsfile)
            return True
        except Exception as e:
            self.console.print(f"[red]파이프라인 생성 실패: {str(e)}[/red]")
            return False