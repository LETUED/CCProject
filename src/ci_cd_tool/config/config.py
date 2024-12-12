from dataclasses import dataclass
from typing import Dict, Optional
import yaml
import os
from pathlib import Path

@dataclass
class Config:
    """CI/CD 도구 설정"""
    ci_provider: str = "github"
    cd_provider: str = "github"
    project_name: str = ""
    repository_url: str = ""
    environment: str = "development"

    @classmethod
    def from_dict(cls, data: Dict) -> 'Config':
        return cls(
            ci_provider=data.get('ci', {}).get('provider', 'github'),
            cd_provider=data.get('cd', {}).get('provider', 'github'),
            project_name=data.get('project', {}).get('name', ''),
            repository_url=data.get('project', {}).get('repository', ''),
            environment=data.get('environment', 'development')
        )

    def to_dict(self) -> Dict:
        return {
            'ci': {
                'provider': self.ci_provider
            },
            'cd': {
                'provider': self.cd_provider
            },
            'project': {
                'name': self.project_name,
                'repository': self.repository_url
            },
            'environment': self.environment
        }