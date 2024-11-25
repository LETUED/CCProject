import unittest
import os
from rich.console import Console
from rich.panel import Panel
from typing import Optional
from dataclasses import dataclass

@dataclass
class TestConfig:
    """테스트 설정 클래스"""
    env: str = 'staging'
    fast: bool = False
    report: bool = False
    test_dir: str = 'tests'

class TestService:
    def __init__(self, console: Console):
        self.console = console
        
    def run_tests(self, config: TestConfig):
        """테스트 실행"""
        if not self._validate_test_directory(config.test_dir):
            return False
            
        self.console.print("[green]테스트 실행 중...[/green]")
        self.console.print(f"[blue]환경: {config.env}[/blue]")
        
        result = self._execute_tests(config.test_dir)
        
        if config.report:
            self._generate_report(config.test_dir)
            
        return result.wasSuccessful()

    def _validate_test_directory(self, test_dir: str) -> bool:
        if not os.path.exists(test_dir):
            self.console.print(Panel(
                f"[red]테스트 디렉토리가 존재하지 않습니다: {test_dir}[/red]",
                title="오류",
                border_style="red"
            ))
            return False
        return True

    def _execute_tests(self, test_dir: str) -> unittest.TestResult:
        loader = unittest.TestLoader()
        suite = loader.discover(start_dir=test_dir)
        runner = unittest.TextTestRunner(verbosity=2)
        return runner.run(suite)

    def _generate_report(self, test_dir: str):
        report_file = os.path.join(test_dir, 'test_report.txt')
        with open(report_file, 'w') as f:
            suite = unittest.TestLoader().discover(start_dir=test_dir)
            runner = unittest.TextTestRunner(stream=f, verbosity=2)
            runner.run(suite)
        self.console.print(Panel(
            f"[cyan]테스트 리포트가 생성되었습니다: {report_file}[/cyan]",
            title="리포트 생성",
            border_style="cyan"
        )) 