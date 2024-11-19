import logging
from pathlib import Path
from rich.logging import RichHandler
from typing import Optional

class LogManager:
    """로깅 관리 클래스"""
    
    def __init__(
        self,
        log_dir: str = "logs",
        log_level: str = "INFO",
        log_format: Optional[str] = None
    ):
        self.log_dir = Path(log_dir)
        self.log_level = getattr(logging, log_level.upper())
        self.log_format = log_format or (
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        )
    
    def setup(self) -> None:
        """로깅 설정"""
        self.log_dir.mkdir(parents=True, exist_ok=True)
        
        logging.basicConfig(
            level=self.log_level,
            format=self.log_format,
            handlers=[
                RichHandler(rich_tracebacks=True),
                logging.FileHandler(self.log_dir / "ci_cd_tool.log")
            ]
        )
        
        # 서드파티 로깅 레벨 조정
        for logger_name in ["urllib3", "github", "gitlab"]:
            logging.getLogger(logger_name).setLevel(logging.WARNING)