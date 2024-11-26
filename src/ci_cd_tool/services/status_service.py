from rich.console import Console
from ..models.pipeline_status import PipelineRun, PipelineSummary

class StatusService:
    def __init__(self, console: Console):
        self.console = console
    
    def display_summary(self, summary: PipelineSummary):
        """파이프라인 요약 정보 표시"""
        self.console.print("\n[bold]파이프라인 실행 현황[/bold]")
        self.console.print(f"✅ 성공: {summary.success_count}")
        self.console.print(f"❌ 실패: {summary.failure_count}")
        self.console.print(f"⏳ 진행 중: {summary.in_progress_count}\n")
    
    def display_pipeline_run(self, run: PipelineRun, details: bool = False):
        """개별 파이프라인 실행 정보 표시"""
        status_color = "green" if run.status == "success" else "red"
        
        self.console.print(f"[{status_color}]#{run.run_id}[/{status_color}] {run.commit_message}")
        if details:
            self.console.print(f"  🔄 상태: {run.status}")
            self.console.print(f"  👤 실행자: {run.actor}")
            self.console.print(f"  🕒 시작: {run.created_at}")
            self.console.print(f"  🔗 링크: {run.run_url}\n")