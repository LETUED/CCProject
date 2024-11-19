from rich.console import Console
from ..config.configuration import Configuration
from ..config.config_manager import ConfigurationManager
from ..templates.template_manager import TemplateManager

class InitializationService:
    def __init__(self, console: Console):
        self.console = console
        self.config_manager = ConfigurationManager()
        self.config = Configuration.from_dict({})

    def initialize(self) -> bool:
        try:
            if not self._setup_project():
                return False
            
            if not self._setup_pipeline():
                return False
                
            if not self._setup_ci():
                return False
            
            self.config_manager.save(self.config)
            self._setup_templates()
            return True
            
        except Exception as e:
            self.console.print(f"[red]초기화 중 오류 발생: {str(e)}[/red]")
            return False

    def _setup_templates(self):
        template_manager = TemplateManager(
            self.config.ci_tool,
            self.config.to_dict()
        )
        template_manager.create_template()