from abc import ABC, abstractmethod
from typing import Dict, Any
from rich.console import Console

class Command(ABC):
    def __init__(self):
        self.console = Console()
        self._state: Dict[str, Any] = {}
    
    @abstractmethod
    def execute(self, **kwargs) -> bool:
        pass
    
    @abstractmethod
    def undo(self) -> bool:
        pass
    
    def save_state(self, **kwargs):
        self._state.update(kwargs) 