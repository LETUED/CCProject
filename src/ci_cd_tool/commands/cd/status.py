import click
from ..base import BaseCommand
from ...core.exceptions import error_handler
from rich.table import Table
from typing import Optional
from dataclasses import dataclass
from datetime import datetime
import boto3

@dataclass
class ServiceStatus:
    current_version: str = 'N/A'
    status: str = 'N/A'
    last_deployed: str = 'N/A'
    deployer: str = 'N/A'
    health: str = 'N/A'
    instance_count: int = 0

class StatusCommand(BaseCommand):
    def execute(self, env: Optional[str] = None) -> bool:
        try:
            cd_service = self.container.cd_service()
            
            if env:
                # 특정 환경의 상태만 조회
                self._show_env_status(env, cd_service)
            else:
                # 모든 환경의 상태 조회
                for env_name in ['dev', 'staging', 'prod']:
                    try:
                        self._show_env_status(env_name, cd_service)
                    except Exception as e:
                        self.warning(f"{env_name} 환경 상태 조회 실패: {str(e)}")
            
            return True
                
        except Exception as e:
            self.error(f"상태 조회 중 오류 발생: {str(e)}")
            return False

    def _show_env_status(self, env: str, cd_service) -> None:
        # 클러스터 이름 생성
        cluster_name = f"cc-cluster-{env}"
        service_name = f"cc-service-{env}"
        
        # 서비스 상태 조회
        status = ServiceStatus()
        
        try:
            # ECR 이미지 조회
            repository_name = f"cc-repo-{env}" if env != 'prod' else 'cc-repo'
            images = cd_service.list_versions(repository_name)
            if images:
                latest_image = images[0]  # 가장 최근 이미지
                status.current_version = latest_image.get('imageTags', ['N/A'])[0]
                status.last_deployed = latest_image['imagePushedAt'].strftime("%Y-%m-%d %H:%M:%S")
            
            # ECS 서비스 상태 조회
            ecs = boto3.client('ecs', region_name='us-east-1')
            service = ecs.describe_services(
                cluster=cluster_name,
                services=[service_name]
            )['services'][0]
            
            status.status = service['status']
            status.health = 'healthy' if service['runningCount'] == service['desiredCount'] else 'unhealthy'
            status.instance_count = service['runningCount']
            
        except Exception as e:
            self.warning(f"상세 상태 조회 실패: {str(e)}")
        
        # 상태 테이블 출력
        table = Table(title=f"{env} 환경 배포 상태")
        table.add_column("항목", style="cyan")
        table.add_column("상태", style="green")
        
        table.add_row("현재 버전", status.current_version)
        table.add_row("배포 상태", status.status)
        table.add_row("마지막 배포", status.last_deployed)
        table.add_row("배포자", status.deployer)
        table.add_row("서비스 상태", status.health)
        table.add_row("실행 인스턴스", str(status.instance_count))
        
        self.console.print(table)
        self.console.print("")  # 빈 줄 추가

@click.command(name='status')
@click.option('--env', help='환경 지정 (생략시 전체 환경)')
@error_handler()
def status_command(env: Optional[str] = None):
    """CD 상태 확인"""
    command = StatusCommand()
    return command.execute(env)

__all__ = ['status_command'] 