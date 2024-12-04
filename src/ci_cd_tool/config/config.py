from typing import Any, Dict, Optional
from .storage.local import LocalConfigStorage

class Config:
    """설정 관리 클래스"""
    
    def __init__(self, storage=None):
        self.storage = storage or LocalConfigStorage()
        self._config = None
    
    @property
    def config(self) -> Dict[str, Any]:
        """설정 로드"""
        if self._config is None:
            self._config = self.storage.load() or {}
        return self._config
    
    def get(self, key: str, default: Any = None) -> Any:
        """설정값 조회"""
        return self.config.get(key, default)
    
    def set(self, key: str, value: Any) -> bool:
        """설정값 저장"""
        self.config[key] = value
        return self.storage.save(self.config)
    
    def get_aws_credentials(self) -> Optional[Dict[str, str]]:
        """AWS 자격 증명 조회"""
        return self.storage.get_aws_credentials() 