from pathlib import Path
import yaml
from typing import Optional, Dict, Any
from .base import ConfigStorage

class LocalConfigStorage(ConfigStorage):
    """로컬 파일 기반 설정 저장소"""
    
    def __init__(self):
        self.config_dir = Path.home() / '.cc'
        self.config_file = self.config_dir / 'config.yml'
        
    def load(self) -> Optional[Dict[str, Any]]:
        if not self.config_file.exists():
            return None
            
        with open(self.config_file, 'r') as f:
            return yaml.safe_load(f)
            
    def save(self, config: Dict[str, Any]) -> bool:
        try:
            self.config_dir.mkdir(parents=True, exist_ok=True)
            with open(self.config_file, 'w') as f:
                yaml.dump(config, f)
            return True
        except Exception:
            return False
            
    def delete(self) -> bool:
        try:
            if self.config_file.exists():
                self.config_file.unlink()
            return True
        except Exception:
            return False 