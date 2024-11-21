from dependency_injector import containers, providers
from ..services.ci_service import CIService
from ..config.config_manager import ConfigurationManager

class Container(containers.DeclarativeContainer):
    config = providers.Singleton(ConfigurationManager)
    ci_service = providers.Factory(
        CIService,
        config=config
    )