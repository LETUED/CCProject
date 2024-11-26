import yaml  # PyYAML 라이브러리
import os
import click
from rich import box
from rich.console import Console
from rich.panel import Panel
from pathlib import Path
from .configuration import Configuration
from typing import Dict, Any, Optional
from dataclasses import dataclass
from ..core.exceptions import ConfigError
from .manager import ConfigManager

# 설정 파일 경로
# CONFIG_FILE = "ci_cd_tool/config/config_test.yml"
CONFIG_FILE = "ci_cd_tool/config/config.yml"
console = Console()

@dataclass
class ToolConfig:
    """도구 설정 정보"""
    ci_provider: str
    project_path: str
    git_branch: Optional[str] = "main"
    environment: Optional[str] = "development"

class ConfigurationManager:
    """설정 관리 클래스"""
    
    def __init__(self):
        self.config_dir = Path.home() / '.cc'
        self.config_file = self.config_dir / 'config.yml'
    
    def load(self):
        if not self.config_file.exists():
            return None
        
        with open(self.config_file, 'r') as f:
            return yaml.safe_load(f)
            
    def save(self, config):
        self.config_dir.mkdir(parents=True, exist_ok=True)
        with open(self.config_file, 'w') as f:
            yaml.dump(config, f)

    def update_config(self, new_config: dict, force: bool = False) -> bool:
        """기존 설정을 유지하면서 새로운 설정으로 업데이트"""
        current = self.load() or {}
        if not force:
            # 기존 설정이 있으면 새로운 설정으로 업데이트
            for section, values in new_config.items():
                if section not in current:
                    current[section] = {}
                current[section].update(values)
        else:
            # 강제 설정이면 완전히 덮어쓰기
            current = new_config
            
        return self.save(current)

    def get_default_config(self) -> dict:
        """기본 설정 템플릿 반환"""
        return {
            'ci': {
                'provider': None,
                'branch_strategy': None,
                'language': None,
                'framework': None,
                'test_framework': None
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
            }
        }

    def show(self):
        """현재 설정 표시"""
        config = self.load()
        if config:
            config_text = "\n".join(
                f"[bold]{k}:[/bold] {v}" 
                for k, v in config.items()
            )
            console.print(Panel(
                config_text,
                title="[green bold]Config 설정 정보[/]",
                border_style="green"
            ))


# 설정 파일 값 변경 기능
def change_config(key, value):
    """설정 파일의 특정 값을 변경"""
    config_manager = ConfigurationManager()
    config = config_manager.load()
    config_dict = config.to_dict()
    config_dict[key] = value
    config_manager.save(Configuration.from_dict(config_dict))
    click.echo(f"'{key}' 값이 '{value}'로 설정되었습니다.")


# 설정 파일 초기화 기능
def reset_config():
    """설정 파일 초기화"""
    config_manager = ConfigManager()
    config_manager.save({})
    click.echo("설정 파일이 초기화되었습니다.")