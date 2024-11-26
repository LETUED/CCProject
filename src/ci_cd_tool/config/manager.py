from typing import Optional, Dict, Any, List
from pathlib import Path
import yaml
from dataclasses import dataclass
from rich.console import Console
from .storage.base import ConfigStorage
from .storage.local import LocalConfigStorage

@dataclass
class CIConfiguration:
    project_root: str = ""
    pipeline_stages: List[str] = None
    framework: str = ""
    ci_tool: str = ""
    remote_repo: Optional[str] = None
    python_version: Optional[str] = None
    gitlab_stages: Optional[List[str]] = None

class ConfigManager:
    def __init__(self, storage: Optional[ConfigStorage] = None):
        self.storage = storage or LocalConfigStorage()
        self.console = Console()
        
    def get_default_config(self) -> Dict[str, Any]:
        """기본 설정 템플릿 반환"""
        return {
            'ci': {
                'provider': None,
                'branch_strategy': None,
                'language': None,
                'framework': None,
                'test_framework': None,
                'python_version': None,
                'pipeline_stages': [],
                'project_root': str(Path.cwd()),
                'remote_repo': None
            },
            'cd': {
                'environments': {
                    'dev': {
                        'region': 'ap-northeast-2',
                        'instance_type': 't2.micro',
                        'ami_id': 'ami-0c9c942bd7bf113a2'
                    },
                    'staging': {
                        'region': 'ap-northeast-2',
                        'instance_type': 't2.small',
                        'ami_id': 'ami-0c9c942bd7bf113a2'
                    },
                    'prod': {
                        'region': 'ap-northeast-2',
                        'instance_type': 't2.medium',
                        'ami_id': 'ami-0c9c942bd7bf113a2'
                    }
                }
            },
            'test': {
                'root_dir': 'unittest',
                'modules': [],
                'patterns': ['test_*.py'],
                'options': {
                    'verbosity': 2,
                    'failfast': False
                }
            }
        }

    def load(self) -> Optional[Dict[str, Any]]:
        """설정 로드"""
        return self.storage.load()
            
    def save(self, config: Dict[str, Any]) -> bool:
        """설정 저장"""
        return self.storage.save(config)

    def update_config(self, new_config: Dict[str, Any], force: bool = False) -> bool:
        """설정 업데이트"""
        current = self.load() or {}
        if not force:
            for section, values in new_config.items():
                if section not in current:
                    current[section] = {}
                if isinstance(values, dict):
                    self._deep_update(current[section], values)
                else:
                    current[section] = values
        else:
            current = new_config
        return self.save(current)

    def _deep_update(self, d: dict, u: dict) -> dict:
        """딕셔너리 깊은 업데이트"""
        for k, v in u.items():
            if isinstance(v, dict) and k in d and isinstance(d[k], dict):
                self._deep_update(d[k], v)
            else:
                d[k] = v
        return d

    def get_section_config(self, section: str, subsection: Optional[str] = None) -> Optional[Dict[str, Any]]:
        """특정 섹션의 설정 조회"""
        config = self.load()
        if not config:
            return None
            
        section_config = config.get(section, {})
        if subsection:
            return section_config.get(subsection)
        return section_config

    def get_ci_config(self) -> CIConfiguration:
        """CI 설정을 CIConfiguration 객체로 반환"""
        config = self.get_section_config('ci')
        if not config:
            return CIConfiguration()
            
        return CIConfiguration(
            project_root=config.get('project_root', ''),
            pipeline_stages=config.get('pipeline_stages', []),
            framework=config.get('framework', ''),
            ci_tool=config.get('provider', ''),
            python_version=config.get('python_version'),
            gitlab_stages=config.get('pipeline_stages'),
            remote_repo=config.get('remote_repo')
        )