import yaml  # PyYAML 라이브러리
import os
import click
from rich import box
from rich.console import Console
from rich.panel import Panel
from pathlib import Path
from .configuration import Configuration
from typing import Dict, Any, Optional, List
from dataclasses import dataclass
from ..core.exceptions import ConfigError
from .storage.base import ConfigStorage
from .storage.local import LocalConfigStorage

@dataclass
class ToolConfig:
    """도구 설정 정보"""
    ci_provider: str
    project_path: str
    git_branch: Optional[str] = "main"
    environment: Optional[str] = "development"

@dataclass
class CIConfiguration:
    project_root: str = ""
    pipeline_stages: List[str] = None
    framework: str = ""
    ci_tool: str = ""
    remote_repo: Optional[str] = None
    python_version: Optional[str] = None
    gitlab_stages: Optional[List[str]] = None

class ConfigurationManager:
    def __init__(self, config_path: str = None):
        self.config_path = config_path or os.path.join(str(Path.home()), '.config', 'cc', 'config.yml')
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
                'provider': 'aws',
                'region': 'us-east-1'
            },
            'project': {
                'name': Path.cwd().name,
                'type': 'Python',
                'framework': None
            },
            'repository': {
                'owner': '',  # GitHub 사용자명
                'name': Path.cwd().name  # 현재 디렉토리 이름
            }
        }

    def set_repository_info(self, owner: str, name: str = None) -> bool:
        """저장소 정보 설정"""
        try:
            config = self.load() or self.get_default_config()
            config['repository']['owner'] = owner
            if name:
                config['repository']['name'] = name
            return self.save(config)
        except Exception as e:
            raise ConfigError(f"저장소 정보 설정 실패: {str(e)}")

    def load(self) -> Dict[str, Any]:
        """설정 파일 로드"""
        try:
            if os.path.exists(self.config_path):
                with open(self.config_path, 'r') as f:
                    return yaml.safe_load(f) or {}
            return {}
        except Exception as e:
            raise ConfigError(f"설정 파일 로드 실패: {str(e)}")

    def save(self, config: Dict[str, Any]) -> bool:
        """설정 저장"""
        try:
            os.makedirs(os.path.dirname(self.config_path), exist_ok=True)
            with open(self.config_path, 'w') as f:
                yaml.dump(config, f)
            return True
        except Exception as e:
            raise ConfigError(f"설정 저장 실패: {str(e)}")

    def update_config(self, new_config: Dict[str, Any], force: bool = False) -> bool:
        """설정 업데이트"""
        current = self.load()
        if not force:
            self._deep_update(current, new_config)
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

    def get_section_config(self, section: Optional[str] = None) -> Optional[Dict]:
        """특정 섹션의 설정을 반환"""
        config = self.load()
        if not config:
            return None
            
        if section:
            return config.get(section)
        return config

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

# 설정 파일 값 변경 기능
def change_config(key, value):
    """설정 파일의 특정 값을 변경"""
    config_manager = ConfigurationManager()
    config = config_manager.load()
    config[key] = value
    config_manager.save(config)
    click.echo(f"'{key}' 값이 '{value}'로 설정되었습니다.")

# 설정 파일 초기화 기능
def reset_config():
    """설정 파일 초기화"""
    config_manager = ConfigurationManager()
    config_manager.save({})
    click.echo("설정 파일이 초기화되었습니다.")

# 이전 이름과의 호환성을 위한 별칭
ConfigManager = ConfigurationManager