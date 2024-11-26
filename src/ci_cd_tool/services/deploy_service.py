from rich.console import Console
from ..deploy.aws_deployer import AWSDeployer, AWSDeployConfig
from dataclasses import dataclass
from typing import Optional, List
from datetime import datetime
import boto3

@dataclass
class DeployStatus:
    current_version: str
    status: str  # running/stopped/error
    last_deployed: str
    deployer: str
    health: str  # healthy/unhealthy
    instance_count: int

@dataclass
class VersionInfo:
    version_id: str
    created_at: str
    status: str
    deployed_by: Optional[str] = None
    environment: Optional[str] = None

@dataclass
class DeployConfig:
    env: str
    version: str
    region: Optional[str] = 'ap-northeast-2'
    instance_type: Optional[str] = 't2.micro'
    ami_id: Optional[str] = None

class DeployService:
    def __init__(self, console: Console):
        self.console = console
        self.aws_client = boto3.client('ecs')  # AWS ECS 클라이언트 예시
    
    def deploy(self, env: str, version: str) -> bool:
        """배포 실행"""
        try:
            config = DeployConfig(
                env=env,
                version=version
            )
            
            aws_config = AWSDeployConfig(
                region=config.region,
                instance_type=config.instance_type,
                ami_id=config.ami_id or 'ami-0c9c942bd7bf113a2'
            )
            
            deployer = AWSDeployer(aws_config)
            return deployer.deploy()
            
        except Exception as e:
            self.console.print(f"[red]배포 실패: {str(e)}[/red]")
            return False
    
    def rollback(self, version: str) -> bool:
        """이전 버전으로 롤백"""
        try:
            self.console.print("[yellow]버전 {}으로 롤백 중...".format(version))
            # 실제 롤백 로직 구현 필요
            return True
        except Exception as e:
            self.console.print(f"[red]롤백 실패: {str(e)}[/red]")
            return False 
    
    def get_status(self, env: str) -> DeployStatus:
        """특정 환경의 배포 상태 조회"""
        try:
            response = self.aws_client.describe_services(
                cluster=f"cc-cluster-{env}",
                services=[f"cc-service-{env}"]
            )
            
            service = response['services'][0]
            
            return DeployStatus(
                current_version=service['taskDefinition'].split('/')[-1],
                status=service['status'],
                last_deployed=service['deployments'][0]['updatedAt'].strftime("%Y-%m-%d %H:%M:%S"),
                deployer=service['deployments'][0].get('creator', 'unknown'),
                health="healthy" if service['runningCount'] == service['desiredCount'] else "unhealthy",
                instance_count=service['runningCount']
            )
            
        except Exception as e:
            self.console.print(f"[red]상태 조회 실패: {str(e)}[/red]")
            raise
            
    def get_versions(self, env: Optional[str] = None) -> List[VersionInfo]:
        """배포 가능한 버전 목록 조회"""
        try:
            ecr_client = boto3.client('ecr')
            response = ecr_client.describe_images(
                repositoryName=f"cc-repo-{env}" if env else "cc-repo",
                maxResults=10
            )
            
            return [
                VersionInfo(
                    version_id=image['imageDigest'][:12],
                    created_at=image['imagePushedAt'].strftime("%Y-%m-%d %H:%M:%S"),
                    status="available",
                    environment=env
                )
                for image in response['imageDetails']
            ]
            
        except Exception as e:
            self.console.print(f"[red]버전 목록 조회 실패: {str(e)}[/red]")
            raise 