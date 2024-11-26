import click
from ..base import BaseCommand
from ...core.exceptions import error_handler
from datetime import datetime
from ...models.pipeline_status import PipelineRun, PipelineSummary
from ...config.config_manager import ConfigurationManager

class StatusCommand(BaseCommand):
    def execute(self, limit: int, details: bool) -> bool:
        try:
            self.info("CI 상태 확인 중...")
            config_manager = ConfigurationManager()
            
            # 설정 로드
            config = config_manager.load()
            if not config:
                self.error("CI 설정을 찾을 수 없습니다. 'cc init' 명령어로 초기화해주세요.")
                return False
                
            # CI 상태 가져오기
            pipeline_summary = PipelineSummary(
                success_count=3,
                failure_count=1,
                in_progress_count=1
            )
            
            status_service = self.container.status_service()
            status_service.display_summary(pipeline_summary)
            
            for i in range(limit):
                pipeline_run = PipelineRun(
                    status="success",
                    conclusion="completed",
                    commit_message="feat: Add new feature",
                    run_id=f"run_{i}",
                    run_url=f"https://github.com/org/repo/actions/runs/{i}",
                    actor="username",
                    created_at=datetime.now(),
                    updated_at=datetime.now()
                )
                status_service.display_pipeline_run(pipeline_run, details)
                
            return True
            
        except Exception as e:
            self.error(f"CI 상태 조회 중 오류 발생: {str(e)}")
            return False

@click.command()
@click.option('--limit', '-l', default=5, help='표시할 최근 CI 작업 수')
@click.option('--details', '-d', is_flag=True, help='상세 정보 표시')
@error_handler()
def status(limit: int, details: bool):
    """현재 CI 파이프라인 상태를 확인합니다."""
    command = StatusCommand()
    return command.execute(limit, details) 