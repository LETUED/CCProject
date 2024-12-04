import logging
from rich.logging import RichHandler
from pathlib import Path
from typing import Optional
from dataclasses import dataclass

@dataclass
class LogConfig:
    level: int = logging.INFO
    format: str = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    log_file: str = ".cc/cc.log"
    use_rich: bool = True

class LoggerFactory:
    _instance: Optional['LoggerFactory'] = None
    _loggers = {}

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._setup_root_logger()
        return cls._instance

    def _setup_root_logger(self):
        log_path = Path(LogConfig.log_file)
        log_path.parent.mkdir(parents=True, exist_ok=True)
        
        handlers = []
        if LogConfig.use_rich:
            handlers.append(RichHandler(rich_tracebacks=True))
        else:
            handlers.append(logging.StreamHandler())
        handlers.append(logging.FileHandler(LogConfig.log_file))
        
        logging.basicConfig(
            level=LogConfig.level,
            format=LogConfig.format,
            handlers=handlers
        )

    def get_logger(self, name: str) -> logging.Logger:
        if name not in self._loggers:
            logger = logging.getLogger(name)
            logger.setLevel(LogConfig.level)
            self._loggers[name] = logger
        return self._loggers[name]

def setup_logging(log_level: str = "INFO", log_file: str = ".cc/cc.log", use_rich: bool = True) -> None:
    LogConfig.level = getattr(logging, log_level)
    LogConfig.log_file = log_file
    LogConfig.use_rich = use_rich
    LoggerFactory()