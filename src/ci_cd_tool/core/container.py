from dependency_injector import containers, providers
from ..services.ci_service import CIService
from ..config.config_manager import ConfigurationManager
from rich.console import Console
from ..services.status_service import StatusService
from ..services.test_service import TestService
from ..services.deploy_service import DeployService

class Container:
    def __init__(self):
        self._console = Console()
        self._services = {}
        self._test_service = None
        self._deploy_service = None
    
    def status_service(self):
        if 'status_service' not in self._services:
            self._services['status_service'] = StatusService(self._console)
        return self._services['status_service']
    
    def test_service(self) -> TestService:
        if not self._test_service:
            self._test_service = TestService(self._console)
        return self._test_service
    
    def deploy_service(self) -> DeployService:
        if not self._deploy_service:
            self._deploy_service = DeployService(self._console)
        return self._deploy_service
    