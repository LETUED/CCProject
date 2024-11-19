from .base import Command
from ...deploy.aws_deployer import AWSDeployer, AWSDeployConfig

class DeployCommand(Command):
    def __init__(self, deployer):
        super().__init__()
        self.deployer = deployer
    
    def execute(self, **kwargs) -> bool:
        try:
            self.save_state(**kwargs)
            return self.deployer.deploy(**kwargs)
        except Exception as e:
            self.console.print(f"[red]배포 실패: {str(e)}[/red]")
            return False
    
    def undo(self) -> bool:
        if not self._state:
            return False
        try:
            return self.deployer.rollback(**self._state)
        except Exception as e:
            self.console.print(f"[red]롤백 실패: {str(e)}[/red]")
            return False 