import os
import unittest
from rich.console import Console
from rich.panel import Panel
from dataclasses import dataclass
from typing import Optional
from git import Repo
from ..models.test_config import TestConfig

@dataclass
class TestConfig:
    env: Optional[str]
    test_dir: str
    report: bool = False

class TestService:
    def __init__(self, console: Console):
        self.console = console
        
    def _detect_environment(self) -> str:
        """Git 브랜치 기반으로 테스트 환경 자동 감지"""
        try:
            repo = Repo(os.getcwd())
            branch = repo.active_branch.name
            
            if branch in ['main', 'master']:
                return 'prod'
            elif branch in ['develop', 'development']:
                return 'dev'
            else:
                return 'staging'
        except:
            return 'staging'  # 기본값
            
    def run_tests(self, config: TestConfig):
        """테스트 실행"""
        if config.env is None:
            config.env = self._detect_environment()
            self.console.print(f"[blue]환경 자동 감지: {config.env}[/blue]")
        
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
        result = runner.run(suite)
        
        # 테스트 결과 요약
        self.console.print("\n[bold]테스트 결과 요약[/bold]")
        self.console.print(f"실행된 테스트: {result.testsRun}")
        self.console.print(f"성공: [green]{result.testsRun - len(result.failures) - len(result.errors)}[/green]")
        
        if result.failures:
            self.console.print(f"실패: [red]{len(result.failures)}[/red]")
        if result.errors:
            self.console.print(f"에러: [red]{len(result.errors)}[/red]")
            
        return result

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

    def _generate_coverage_report(self, test_dir: str):
        """테스트 커버리지 리포트 생성"""
        try:
            import coverage
            
            cov = coverage.Coverage()
            cov.start()
            
            # 테스트 실행
            self._execute_tests(test_dir)
            
            cov.stop()
            cov.save()
            
            # 리포트 생성
            cov.html_report(directory='coverage_report')
            
            self.console.print(Panel(
                "[cyan]커버리지 리포트가 생성되었습니다: coverage_report/index.html[/cyan]",
                title="커버리지 리포트",
                border_style="cyan"
            ))
            
        except ImportError:
            self.console.print("[yellow]coverage 패키지가 설치되어 있지 않습니다.[/yellow]") 