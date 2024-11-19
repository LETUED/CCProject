from rich.console import Console
from ..deploy.aws_deployer import AWSDeployer, AWSDeployConfig
from dataclasses import dataclass
from typing import Optional

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
                ami_id=config.ami_id or 'ami-0c9c942bd7bf113a2'  # Amazon Linux 2 AMI
            )
            
            deployer = AWSDeployer(aws_config)
            return deployer.deploy()
            
        except Exception as e:
            self.console.print(f"[red]배포 실패: {str(e)}[/red]")
            return False
    
    def rollback(self, version: str) -> bool:
        """롤백 실행"""
        try:
            self.console.print(f"[yellow]버전 {version}으로 롤백 중...[/yellow]")
            # AWS 롤백 로직 구현
            return True
        except Exception as e:
            self.console.print(f"[red]롤백 실패: {str(e)}[/red]")
            return False 