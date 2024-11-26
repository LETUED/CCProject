from abc import ABC, abstractmethod
from rich.console import Console
from ..core.container import Container
from ..core.logging import setup_logging
from ..core.exceptions import CommandError
import logging

class BaseCommand(ABC):
    """명령어 기본 클래스"""
    
    def __init__(self):
        self.console = Console()
        self.container = Container()
        self.logger = logging.getLogger(self.__class__.__name__)
        setup_logging()
    
    def info(self, message: str):
        """정보 메시지 출력"""
        self.logger.info(message)
        self.console.print(f"[blue]{message}[/blue]")
    
    def success(self, message: str):
        """성공 메시지 출력"""
        self.logger.info(message)
        self.console.print(f"[green]{message}[/green]")
    
    def warning(self, message: str):
        """경고 메시지 출력"""
        self.logger.warning(message)
        self.console.print(f"[yellow]{message}[/yellow]")
    
    def error(self, message: str):
        """에러 메시지 출력"""
        self.logger.error(message)
        self.console.print(f"[red]{message}[/red]")
        raise CommandError(message)
    
    @abstractmethod
    def execute(self, *args, **kwargs) -> bool:
        """명령어 실행 로직"""
        pass 