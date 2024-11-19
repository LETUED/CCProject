from abc import ABC, abstractmethod
from rich.console import Console
from typing import Dict, Optional

class BaseCI(ABC):
    def __init__(self):
        self.console = Console()
    
    @abstractmethod
    def create_pipeline(self, config: Dict) -> bool:
        pass
    
    @abstractmethod
    def run_tests(self, test_config: Dict) -> bool:
        pass
    
    @abstractmethod
    def get_status(self) -> Dict:
        pass 