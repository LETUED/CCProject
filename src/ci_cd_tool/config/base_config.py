from dataclasses import dataclass
from typing import List, Optional

@dataclass
class BaseConfiguration:
    project_root: str
    pipeline_stages: List[str]
    framework: str
    ci_tool: str
    remote_repo: Optional[str] = None
    python_version: Optional[str] = None
    gitlab_stages: Optional[List[str]] = None

    @classmethod
    def create_default(cls):
        return cls(
            project_root="",
            pipeline_stages=[],
            framework="pytest",
            ci_tool="GitHub Actions",
            remote_repo=None
        ) 