from dependency_injector import containers, providers
from ..config.config_manager import ConfigManager
from ..services.ci_service import CIService
from ..services.cd_service import CDService

class Container(containers.DeclarativeContainer):
    """DI 컨테이너"""
    
    config = providers.Singleton(ConfigManager)
    
    ci_service = providers.Singleton(
        CIService,
        config=config
    )
    
    cd_service = providers.Singleton(
        CDService,
        config=config
    )

__all__ = ['Container']
    