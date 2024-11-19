from abc import ABC, abstractmethod
from rich.console import Console

class BaseDeployer(ABC):
    def __init__(self):
        self.console = Console()
    
    @abstractmethod
    def deploy(self) -> bool:
        pass
    
    @abstractmethod
    def rollback(self) -> bool:
        pass 