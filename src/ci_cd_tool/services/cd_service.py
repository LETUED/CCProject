from ..config.config_manager import ConfigManager

class CDService:
    """CD 서비스"""
    
    def __init__(self, config: ConfigManager):
        self.config = config
        
    def deploy(self, version: str):
        """배포 실행"""
        pass
        
    def rollback(self, version: str):
        """롤백 실행"""
        pass
        
    def status(self):
        """상태 확인"""
        pass

__all__ = ['CDService'] 