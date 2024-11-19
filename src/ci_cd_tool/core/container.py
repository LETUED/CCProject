from rich.console import Console
from ..services.test_service import TestService
from ..config.config_manager import ConfigurationManager
from ..services.deploy_service import DeployService

class Container:
    def __init__(self):
        self.console = Console()
    
    def test_service(self) -> TestService:
        return TestService(console=self.console)
    
    def get_config_manager(self) -> ConfigurationManager:
        return self.config_manager 
    
    def deploy_service(self):
        return DeployService(self.console)