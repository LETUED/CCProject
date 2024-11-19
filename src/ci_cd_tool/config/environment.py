from dataclasses import dataclass
from typing import Dict, Any
import yaml
from pathlib import Path

@dataclass
class Environment:
    name: str
    branch: str
    deploy_url: str
    variables: Dict[str, str]

class EnvironmentManager:
    def __init__(self, config_dir: str = "ci_cd_tool/config/environments"):
        self.config_dir = Path(config_dir)
        self.environments = {}
        self._load_environments()
    
    def _load_environments(self):
        for config_file in self.config_dir.glob("*.yml"):
            env_name = config_file.stem
            with open(config_file) as f:
                config = yaml.safe_load(f)
                self.environments[env_name] = Environment(
                    name=env_name,
                    branch=config.get('branch', 'main'),
                    deploy_url=config.get('deploy_url', ''),
                    variables=config.get('variables', {})
                ) 