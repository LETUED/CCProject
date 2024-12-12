import click
from ..base import BaseCommand
from ...core.exceptions import error_handler
from datetime import datetime
from ...models.pipeline_status import PipelineRun, PipelineSummary
from ...config.config_manager import ConfigurationManager
import requests
import os
from rich.table import Table

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
            
            # GitHub 토큰 확인
            github_token = os.getenv('GITHUB_TOKEN')
            if not github_token:
                self.error("GitHub 토큰이 설정되지 않았습니다. GITHUB_TOKEN 환경변수를 설정해주세요.")
                return False
            
            # GitHub API로 워크플로우 실행 목록 가져오기
            headers = {
                'Authorization': f'token {github_token}',
                'Accept': 'application/vnd.github.v3+json'
            }
            
            repo_info = config.get('repository', {})
            owner = repo_info.get('owner')
            repo = repo_info.get('name')
            
            if not (owner and repo):
                self.error("저장소 정보가 설정되지 않았습니다. 'cc init' 명령어로 초기화해주세요.")
                return False
            
            url = f"https://api.github.com/repos/{owner}/{repo}/actions/runs"
            response = requests.get(url, headers=headers)
            
            if response.status_code != 200:
                self.error(f"GitHub API 호출 실패: {response.json().get('message')}")
                return False
            
            workflow_runs = response.json().get('workflow_runs', [])[:limit]
            
            # 상태 요약 계산
            success_count = sum(1 for run in workflow_runs if run['conclusion'] == 'success')
            failure_count = sum(1 for run in workflow_runs if run['conclusion'] == 'failure')
            in_progress_count = sum(1 for run in workflow_runs if run['status'] == 'in_progress')
            
            pipeline_summary = PipelineSummary(
                success_count=success_count,
                failure_count=failure_count,
                in_progress_count=in_progress_count
            )
            
            # 결과 표시
            status_service = self.container.status_service()
            status_service.display_summary(pipeline_summary)
            
            # 상세 실행 정보 표시
            table = Table(title="워크플로우 실행 목록")
            table.add_column("상태", style="cyan")
            table.add_column("커밋 메시지", style="green")
            table.add_column("브랜치", style="blue")
            table.add_column("실행자", style="yellow")
            table.add_column("시작 시간", style="magenta")
            
            for run in workflow_runs:
                status_icon = "✅" if run['conclusion'] == 'success' else "❌" if run['conclusion'] == 'failure' else "⏳"
                table.add_row(
                    status_icon,
                    run['head_commit']['message'] if run.get('head_commit') else "N/A",
                    run['head_branch'],
                    run['actor']['login'],
                    run['created_at']
                )
            
            self.console.print(table)
            return True
            
        except Exception as e:
            self.error(f"CI 상태 조회 중 오류 발생: {str(e)}")
            return False

@click.command(name='status')
@click.option('-l', '--limit', default=5, help='표시할 파이프라인 수')
@click.option('-d', '--details', is_flag=True, help='상세 정보 표시')
@error_handler()
def status(limit: int, details: bool):
    """CI 파이프라인 상태 확인"""
    command = StatusCommand()
    return command.execute(limit, details) 