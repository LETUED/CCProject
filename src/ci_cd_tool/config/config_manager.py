import os
import yaml
from pathlib import Path

class ConfigManager:
    def __init__(self, config_path=None):
        self.config_path = config_path or os.path.expanduser('~/.cc/config.yml')
        self.config = self._load_config()

    def _load_config(self):
        """설정 파일 로드"""
        if not os.path.exists(self.config_path):
            return {}
            
        with open(self.config_path, 'r') as f:
            return yaml.safe_load(f) or {}

    def get_value(self, key):
        """설정값 조회"""
        keys = key.split('.')
        value = self.config
        for k in keys:
            if isinstance(value, dict):
                value = value.get(k)
            else:
                return None
        return value

    def set_value(self, key, value):
        """설정값 저장"""
        keys = key.split('.')
        current = self.config
        for k in keys[:-1]:
            current = current.setdefault(k, {})
        current[keys[-1]] = value
        self._save_config()

    def _save_config(self):
        """설정 파일 저장"""
        os.makedirs(os.path.dirname(self.config_path), exist_ok=True)
        with open(self.config_path, 'w') as f:
            yaml.dump(self.config, f)