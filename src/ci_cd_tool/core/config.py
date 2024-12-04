import os
import yaml
from pathlib import Path
from typing import Any, Dict, Optional
from .exceptions import ConfigError

class Config:
    """설정 관리 클래스"""
    
    _instance = None  # 싱글톤 인스턴스
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.config = {}
            cls._instance._load_config()
        return cls._instance
    
    def _load_config(self):
        """설정 파일을 로드합니다"""
        if hasattr(self, '_loaded') and self._loaded:
            return
            
        config_paths = [
            Path.home() / '.config' / 'cc' / 'config.yml',  # 글로벌 설정
            Path.cwd() / '.cc' / 'config.yml'  # 프로젝트 설정
        ]
        
        for path in config_paths:
            if path.exists():
                try:
                    with open(path) as f:
                        self.config.update(yaml.safe_load(f) or {})
                except Exception as e:
                    raise ConfigError(f"설정 파일 로드 중 오류 발생: {str(e)}")
                    
        # 환경 변수로부터 설정 로드
        self._load_from_env()
        self._loaded = True
        
    def _load_from_env(self):
        """환경 변수로부터 설정을 로드합니다"""
        env_mapping = {
            'AWS_REGION': 'aws_region',
            'ECR_REPOSITORY': 'ecr_repository',
            'AWS_ACCESS_KEY_ID': 'aws_access_key_id',
            'AWS_SECRET_ACCESS_KEY': 'aws_secret_access_key'
        }
        
        for env_key, config_key in env_mapping.items():
            if value := os.getenv(env_key):
                self.config[config_key] = value
                
    def get(self, key: str, default: Any = None) -> Any:
        """설정값을 조회합니다"""
        return self.config.get(key, default)
        
    def set(self, key: str, value: Any):
        """설정값을 저장합니다"""
        self.config[key] = value