from dataclasses import dataclass
from typing import Optional
from rich.console import Console
from ..core.exceptions import CIServiceError
from ..config.config_manager import ConfigurationManager
import subprocess
from pathlib import Path
import os
from git import Repo
from rich.panel import Panel
import shutil

@dataclass
class BuildConfig:
    env: Optional[str] = None
    use_cache: bool = True

class BuildService:
    def __init__(self, console: Console):
        self.console = console
        self.config_manager = ConfigurationManager()
        
    def run_build(self, config: BuildConfig) -> bool:
        try:
            settings = self.config_manager.load()
            ci_provider = settings.get('ci_tool', 'GitHub Actions')
            self.console.print(f"[blue]CI 제공자: {ci_provider}[/blue]")
            
            # 빌드 환경 설정
            env = config.env or self._detect_environment()
            self.console.print(f"[blue]빌드 환경: {env}[/blue]")
            
            # 의존성 설치
            if not self._install_dependencies(config.use_cache):
                self.console.print("[red]빌드 실패: 의존성 설치 실패[/red]")
                return False
                
            # 테스트 실행
            if not self._run_tests():
                self.console.print("[red]빌드 실패: 테스트 실패[/red]")
                return False
                
            # 빌드 아티팩트 생성
            if not self._create_artifacts():
                self.console.print("[red]빌드 실패: 아티팩트 생성 실패[/red]")
                return False
                
            self.console.print("[green]빌드가 성공적으로 완료되었습니다[/green]")
            return True
            
        except Exception as e:
            raise CIServiceError(f"빌드 실패: {str(e)}")
            
    def _detect_environment(self) -> str:
        """Git 브랜치 기반으로 빌드 환경 자동 감지"""
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
            return 'dev'  # 기본값
            
    def _validate_project_structure(self) -> bool:
        """프로젝트 구조 검증"""
        required_files = [
            "pyproject.toml",
            "requirements.txt",
            "src/ci_cd_tool"
        ]
        
        for file_path in required_files:
            if not Path(file_path).exists():
                self.console.print(Panel(
                    f"[red]필수 파일/디렉토리가 없습니다: {file_path}[/red]",
                    title="구조 검증 실패",
                    border_style="red"
                ))
                return False
        return True
        
    def _install_dependencies(self, use_cache: bool) -> bool:
        try:
            if not self._validate_project_structure():
                return False
                
            self.console.print("[yellow]의존성 설치 중...[/yellow]")
            
            # 가상환경 확인
            if not os.environ.get('VIRTUAL_ENV'):
                self.console.print(Panel(
                    "[yellow]가상환경이 활성화되어 있지 않습니다. 가상환경을 활성화하는 것을 권장합니다.[/yellow]",
                    title="경고",
                    border_style="yellow"
                ))
            
            # 개발 모드로 설치
            cmd = ["pip", "install", "-e", ".", "-r", "requirements.txt"]
            if not use_cache:
                cmd.append("--no-cache-dir")
            
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                check=False
            )
            
            if result.returncode != 0:
                self.console.print(Panel(
                    f"[red]의존성 설치 실패:[/red]\n{result.stderr}",
                    title="오류",
                    border_style="red"
                ))
                return False
                
            self.console.print("[green]의존성 설치 완료[/green]")
            return True
            
        except Exception as e:
            self.console.print(Panel(
                f"[red]의존성 설치 중 오류 발생: {str(e)}[/red]",
                title="오류",
                border_style="red"
            ))
            return False
            
    def _run_tests(self) -> bool:
        """테스트 실행"""
        try:
            self.console.print("[yellow]테스트 실행 중...[/yellow]")
            import unittest
            
            loader = unittest.TestLoader()
            suite = loader.discover(start_dir='tests')
            runner = unittest.TextTestRunner(verbosity=2)
            result = runner.run(suite)
            
            return result.wasSuccessful()
            
        except Exception as e:
            self.console.print(f"[red]테스트 실행 실패: {str(e)}[/red]")
            return False
            
    def _create_artifacts(self) -> bool:
        """빌드 아티팩트 생성"""
        try:
            self.console.print("[yellow]아티팩트 생성 ��...[/yellow]")
            dist_dir = Path("dist")
            dist_dir.mkdir(exist_ok=True)
            
            # pyproject.toml 확인
            if not Path("pyproject.toml").exists():
                self.console.print("[yellow]pyproject.toml 파일이 없습니다. 기본 아티팩트만 생성합니다.[/yellow]")
                return True
            
            # 빌드 실행
            try:
                subprocess.run(["python", "-m", "build"], check=True)
                
                # 테스트 리포트 복사
                if Path("unittest/test_report.txt").exists():
                    shutil.copy2("unittest/test_report.txt", dist_dir / "test_report.txt")
                    
                # 커버리지 리포트 복사
                if Path("coverage_report").exists():
                    shutil.copytree("coverage_report", dist_dir / "coverage_report", dirs_exist_ok=True)
                    
                self.console.print("[green]아티팩트 생성이 완료되었습니다[/green]")
                self.console.print(f"[blue]생성된 아티팩트 위치: {dist_dir}[/blue]")
                return True
                
            except subprocess.CalledProcessError as e:
                self.console.print(f"[red]빌드 실행 실패: {str(e)}[/red]")
                return False
                
        except Exception as e:
            self.console.print(f"[red]아티팩트 생성 실패: {str(e)}[/red]")
            return False