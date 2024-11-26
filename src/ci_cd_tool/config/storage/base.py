from abc import ABC, abstractmethod
from typing import Optional, Dict, Any

class ConfigStorage(ABC):
    """설정 저장소 인터페이스"""
    
    @abstractmethod
    def load(self) -> Optional[Dict[str, Any]]:
        """설정 로드"""
        pass
        
    @abstractmethod
    def save(self, config: Dict[str, Any]) -> bool:
        """설정 저장"""
        pass
        
    @abstractmethod
    def delete(self) -> bool:
        """설정 삭제"""
        pass 