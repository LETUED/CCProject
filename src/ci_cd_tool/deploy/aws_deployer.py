from dataclasses import dataclass
from typing import Optional
import boto3
from rich.console import Console
from rich.panel import Panel
from .base_deployer import BaseDeployer

@dataclass
class AWSDeployConfig:
    region: str
    instance_type: str
    ami_id: str
    
class AWSDeployer(BaseDeployer):
    def __init__(self, config: AWSDeployConfig):
        super().__init__()
        self.config = config
        self.ec2 = boto3.resource('ec2', region_name=config.region)
    
    def deploy(self) -> bool:
        try:
            self.console.print("[yellow]EC2 인스턴스 생성 중...[/yellow]")
            instance = self.ec2.create_instances(
                ImageId=self.config.ami_id,
                InstanceType=self.config.instance_type,
                MinCount=1,
                MaxCount=1
            )[0]
            
            self.console.print(f"[green]인스턴스 생성 완료 (ID: {instance.id})[/green]")
            return True
            
        except Exception as e:
            self.console.print(Panel(f"[red]배포 실패: {str(e)}[/red]", 
                                  title="오류", border_style="red"))
            return False
    
    def rollback(self) -> bool:
        try:
            self.console.print("[yellow]이전 버전으로 롤백 중...[/yellow]")
            # 롤백 로직 구현
            return True
        except Exception as e:
            self.console.print(f"[red]롤백 실패: {str(e)}[/red]")
            return False