import click
from ..base import BaseCommand
from ...core.exceptions import error_handler
from ...config.manager import ConfigManager
from rich.table import Table
from typing import Optional

class ShowCommand(BaseCommand):
    def execute(self, section: Optional[str] = None) -> bool:
        try:
            config_manager = ConfigManager()
            config = config_manager.get_section_config(section) if section else config_manager.load()
            
            if not config:
                self.error("설정을 찾을 수 없습니다")
                return False
                
            if section == 'cd':
                return self._show_cd_config(config)
            else:
                self.console.print(config)
            return True
                
        except Exception as e:
            self.error(f"설정 표시 중 오류 발생: {str(e)}")
            return False
            
    def _show_cd_config(self, config: dict) -> bool:
        table = Table(title="CD 설정")
        table.add_column("환경", style="cyan")
        table.add_column("리전", style="magenta")
        table.add_column("인스턴스 타입", style="green")
        table.add_column("AMI ID", style="yellow")
        
        for env_name, env_config in config.get('environments', {}).items():
            table.add_row(
                env_name,
                env_config.get('region', 'ap-northeast-2'),
                env_config.get('instance_type', 't2.micro'),
                env_config.get('ami_id', '')
            )
                
        self.console.print(table)
        return True

@click.command()
@click.option('--section', help='설정 섹션 지정 (예: ci, cd, test)')
@error_handler()
def show(section: Optional[str]):
    """현재 설정 표시"""
    command = ShowCommand()
    return command.execute(section) 