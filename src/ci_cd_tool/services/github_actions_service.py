import os
from rich.console import Console
from rich.panel import Panel
from ..config.config_manager import ConfigurationManager

class GitHubActionsService:
    def __init__(self, console: Console, config_manager: ConfigurationManager):
        self.console = console
        self.config_manager = config_manager
        self.template_path = "src/ci_cd_tool/templates/templates/github_actions_ci.yml"

    def add_test_configuration(self, fast: bool, report: bool):
        try:
            test_block = self._generate_test_block(fast, report)
            self._update_actions_file(test_block)
            self._show_success_message()
        except Exception as e:
            self._handle_error(e)

    def _generate_test_block(self, fast: bool, report: bool) -> str:
        test_commands = []
        test_dir = "tests/fast" if fast else "tests"
        test_commands.append(f"python -m unittest discover -s {test_dir}")
        if report:
            test_commands.append("python -m unittest discover -s tests --report")
        return "\n".join(f"        {cmd}" for cmd in test_commands)

    def _update_actions_file(self, test_block: str):
        if not os.path.exists(self.template_path):
            raise FileNotFoundError(f"GitHub Actions 템플릿 파일을 찾을 수 없습니다: {self.template_path}")
            
        with open(self.template_path, 'r+') as file:
            content = file.readlines()
            updated_content = self._insert_test_block(content, test_block)
            file.seek(0)
            file.writelines(updated_content)

    def _insert_test_block(self, content: list, test_block: str) -> list:
        for i, line in enumerate(content):
            if '- name: Run Tests' in line:
                while i + 1 < len(content) and content[i + 1].strip().startswith('run: |'):
                    i += 1
                content.insert(i + 1, f"{test_block}\n")
                break
        else:
            content.append("\n    - name: Run Tests\n      run: |\n" + test_block + "\n")
        return content 