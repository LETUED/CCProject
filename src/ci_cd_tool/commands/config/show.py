import click
from rich.table import Table
from ..base import BaseCommand
from ...core.exceptions import error_handler
from ...config.config_manager import ConfigManager

class ShowCommand(BaseCommand):
    """설정 표시 명령어"""
    
    def execute(self, section: str = None) -> bool:
        try:
            config = ConfigManager()
            
            if section:
                self.info(f"{section} 설정 표시")
                config_data = config.get_value(section)
                if not config_data:
                    self.warning(f"{section} 설정이 없습니다")
                    return True
            else:
                self.info("전체 설정 표시")
                config_data = config.config
            
            self._display_config(config_data, section)
            return True
                
        except Exception as e:
            self.error(f"설정 표시 실패: {str(e)}")
            return False
            
    def _display_config(self, config: dict, section: str = None):
        """설정을 테이블로 표시"""
        table = Table(title=f"{'전체' if not section else section.upper()} 설정")
        
        table.add_column("설정", style="cyan")
        table.add_column("값", style="green")
        
        def add_rows(data, prefix=''):
            for key, value in data.items():
                if isinstance(value, dict):
                    add_rows(value, f"{prefix}{key}.")
                else:
                    table.add_row(f"{prefix}{key}", str(value))
                    
        add_rows(config)
        self.console.print(table)

@click.command()
@click.option('--section', help='설정 섹션 지정 (예: ci, cd, test)')
@error_handler()
def show(section: str = None):
    """현재 설정 표시"""
    command = ShowCommand()
    return command.execute(section)

__all__ = ['show'] 