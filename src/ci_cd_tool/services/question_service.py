from typing import List, Optional, Any
import inquirer
from rich.console import Console

class QuestionService:
    def __init__(self, console: Console):
        self.console = console

    def ask_text(self, name: str, message: str) -> Optional[str]:
        question = inquirer.Text(name, message=message)
        return self._prompt_question(question)

    def ask_list(self, name: str, message: str, choices: List[str]) -> Optional[str]:
        question = inquirer.List(name, message=message, choices=choices)
        return self._prompt_question(question)

    def _prompt_question(self, question: Any) -> Optional[str]:
        try:
            answers = inquirer.prompt([question])
            return answers.get(question.name) if answers else None
        except Exception as e:
            self.console.print(f"[red]오류: {str(e)}[/red]")
            return None 