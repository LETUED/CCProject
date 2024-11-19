from typing import Dict
from ..ci.base_ci import BaseCI
from ..ci.github_actions import GitHubActionsCI
from ..ci.gitlab_ci import GitLabCI, GitLabCIConfig
from ..ci.jenkins import JenkinsCI, JenkinsConfig

class CIFactory:
    @staticmethod
    def create_ci_service(tool: str, config: Dict) -> BaseCI:
        if tool == "github":
            return GitHubActionsCI(config)
        elif tool == "gitlab":
            return GitLabCI(GitLabCIConfig(**config))
        elif tool == "jenkins":
            return JenkinsCI(JenkinsConfig(**config))
        raise ValueError(f"지원하지 않는 CI 도구입니다: {tool}") 