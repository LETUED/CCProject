from abc import ABC, abstractmethod
from typing import Dict, Type
from pathlib import Path
from rich.console import Console

class DeployerPlugin(ABC):
    console = Console()
    
    @property
    @abstractmethod
    def name(self) -> str:
        pass
    
    @abstractmethod
    def initialize(self, **config):
        pass
    
    @abstractmethod
    def deploy(self, **kwargs) -> bool:
        pass
    
    @abstractmethod
    def rollback(self, **kwargs) -> bool:
        pass

class PluginManager:
    _plugins: Dict[str, Type[DeployerPlugin]] = {}
    
    @classmethod
    def register(cls, plugin_class: Type[DeployerPlugin]):
        cls._plugins[plugin_class.name] = plugin_class
    
    @classmethod
    def get_plugin(cls, name: str) -> Type[DeployerPlugin]:
        return cls._plugins.get(name) 