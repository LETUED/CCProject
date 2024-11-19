import time
import functools
from typing import Callable
import logging
from dataclasses import dataclass
from datetime import datetime
from typing import List, Optional
from rich.console import Console
from rich.table import Table
from rich.panel import Panel

logger = logging.getLogger(__name__)

@dataclass
class PipelineStatus:
    pipeline_id: str
    name: str
    status: str
    created_at: datetime
    conclusion: Optional[str] = None
    url: Optional[str] = None

class MonitoringService:
    def __init__(self):
        self.console = Console()
        self.active_pipelines: List[PipelineStatus] = []

    def update_pipeline_status(self, pipeline: PipelineStatus):
        self.active_pipelines.append(pipeline)

    def display_status(self):
        table = Table(title="파이프라인 상태")
        table.add_column("ID", style="cyan")
        table.add_column("이름", style="magenta")
        table.add_column("상태", style="green")
        table.add_column("결과", style="yellow")
        table.add_column("생성 시간", style="blue")
        
        for pipeline in self.active_pipelines:
            table.add_row(
                pipeline.pipeline_id,
                pipeline.name,
                pipeline.status,
                pipeline.conclusion or "진행 중",
                pipeline.created_at.strftime("%Y-%m-%d %H:%M:%S")
            )
        
        self.console.print(table)

def monitor_performance(threshold_ms: int = 1000):
    def decorator(func: Callable):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            start_time = time.time()
            result = func(*args, **kwargs)
            execution_time = (time.time() - start_time) * 1000
            
            logger.info(
                f"함수 {func.__name__} 실행 시간: {execution_time:.2f}ms"
            )
            
            if execution_time > threshold_ms:
                logger.warning(
                    f"함수 {func.__name__}의 실행 시간이 {threshold_ms}ms를 초과했습니다"
                )
            
            return result
        return wrapper
    return decorator 