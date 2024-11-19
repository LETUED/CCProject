from rich.console import Console
from rich.panel import Panel
from ..models.pipeline_status import PipelineRun, PipelineSummary
from typing import List

class StatusDisplayService:
    def __init__(self, console: Console):
        self.console = console

    def display_summary(self, summary: PipelineSummary):
        self.console.print(
            Panel(
                f"성공: {summary.success_count}, 실패: {summary.failure_count}, "
                f"진행 중: {summary.in_progress_count}",
                title="파이프라인 요약",
                border_style="cyan"
            )
        )

    def display_pipeline_run(self, run: PipelineRun, show_details: bool):
        details_msg = self._format_pipeline_details(run, show_details)
        self.console.print(
            Panel(details_msg, title="파이프라인 정보", border_style="yellow")
        )

    def _format_pipeline_details(self, run: PipelineRun, show_details: bool) -> str:
        # 상세 정보 포맷팅 로직
        pass 