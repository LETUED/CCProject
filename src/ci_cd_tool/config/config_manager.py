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
    
    def __init__(self, config_path: str = ".cc/config.yml"):
        self.config_path = Path(config_path)
        self._config: Optional[Dict[str, Any]] = None
    
    def load(self) -> Dict[str, Any]:
        """설정 파일 로드"""
        try:
            if not self.config_path.exists():
                return {}
                
            with self.config_path.open() as f:
                self._config = yaml.safe_load(f)
            return self._config or {}
            
        except Exception as e:
            raise ConfigError(f"설정 로드 실패: {str(e)}")
    
    def save(self, config: Dict[str, Any]) -> None:
        """설정 저장"""
        try:
            self.config_path.parent.mkdir(parents=True, exist_ok=True)
            with self.config_path.open('w') as f:
                yaml.dump(config, f)
        except Exception as e:
            raise ConfigError(f"설정 저장 실패: {str(e)}")

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
    config_manager = ConfigurationManager()
    config_manager.save(Configuration.from_dict({}))
    click.echo(f"{CONFIG_FILE} 파일이 초기화되었습니다.")