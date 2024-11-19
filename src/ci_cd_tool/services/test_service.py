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
        self.console.print("[green]테스트 실행 중...[/green]")
        
        if config.env:
            self.console.print(f"[blue]환경: {config.env}[/blue]")
        
        if config.fast:
            self.console.print("[yellow]빠른 테스트 모드[/yellow]")
            
        if config.report:
            self.console.print("[blue]테스트 리포트 생성[/blue]")
            
        # 실제 테스트 실행 로직
        self.console.print(f"[green]테스트 디렉토리: {config.test_dir}[/green]")

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