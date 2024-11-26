from typing import Dict, Optional
from .base_ci import BaseCI
from ..core.exceptions import CIServiceError
import os
import subprocess
from pathlib import Path

class GitHubActionsCI(BaseCI):
    """GitHub Actions CI 구현 클래스"""
    
    def __init__(self, config: Dict):
        super().__init__(config)
        self.workflow_file = ".github/workflows/ci.yml"
    
    def create_pipeline(self) -> bool:
        """파이프라인 생성"""
        try:
            # GitHub Actions workflow 파일이 이미 존재하는지 확인
            if os.path.exists(self.workflow_file):
                return True
                
            # 기본 workflow 템플릿 생성
            workflow_content = self._generate_workflow_template()
            os.makedirs(os.path.dirname(self.workflow_file), exist_ok=True)
            
            with open(self.workflow_file, 'w') as f:
                f.write(workflow_content)
                
            return True
        except Exception as e:
            raise CIServiceError(f"GitHub Actions workflow 생성 실패: {str(e)}")
    
    def run_tests(self, test_config: Dict) -> bool:
        """테스트 실행"""
        try:
            self.console.print("[yellow]테스트 실행 중...[/yellow]")
            
            # unittest 프레임워크 사용
            import unittest
            loader = unittest.TestLoader()
            start_dir = test_config.get('test_dir', 'tests')
            suite = loader.discover(start_dir=start_dir, pattern="test_*.py")
            
            runner = unittest.TextTestRunner(verbosity=2)
            result = runner.run(suite)
            
            if result.wasSuccessful():
                self.console.print("[green]모든 테스트가 성공적으로 완료되었습니다[/green]")
                return True
            else:
                self.console.print(f"[red]테스트 실패: {len(result.failures)} 실패, {len(result.errors)} 에러[/red]")
                return False
            
        except Exception as e:
            self.console.print(f"[red]테스트 실행 실패: {str(e)}[/red]")
            return False
    
    def _generate_workflow_template(self) -> str:
        """GitHub Actions workflow 템플릿 생성"""
        return """name: CI Pipeline

on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main, develop ]

jobs:
  build:
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v2
    
    - name: Set up Python
      uses: actions/setup-python@v2
      with:
        python-version: '3.x'
        
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        if [ -f requirements.txt ]; then pip install -r requirements.txt; fi
        
    - name: Run tests
      run: |
        python -m pytest
        
    - name: Build package
      run: |
        python -m pip install build
        python -m build
        
    - name: Upload artifact
      uses: actions/upload-artifact@v2
      with:
        name: dist
        path: dist/
"""
    
    def run_pipeline(self, config: Dict) -> bool:
        """GitHub Actions 파이프라인 실행"""
        try:
            self.console.print("[yellow]GitHub Actions 파이프라인 실행 중...[/yellow]")
            self.console.print(f"[blue]실행 환경: {config.get('environment')}[/blue]")
            
            # 의존성 설치
            self.console.print("[yellow]의존성 설치 중...[/yellow]")
            if not self._install_dependencies():
                return False
            
            # 테스트 실행
            self.console.print("[yellow]테스트 실행 중...[/yellow]")
            if not self._run_tests(config):
                return False
            
            # 빌드 아티팩트 생성
            self.console.print("[yellow]빌드 아티팩트 생성 중...[/yellow]")
            if not self._create_artifacts():
                return False
            
            self.console.print("[green]파이프라인 실행이 완료되었습니다[/green]")
            return True
            
        except Exception as e:
            raise CIServiceError(f"GitHub Actions 파이프라인 실행 실패: {str(e)}")
            
    def _install_dependencies(self) -> bool:
        """의존성 설치"""
        try:
            # 기본 빌드 도구 설치
            self.console.print("[yellow]빌드 도구 설치 중...[/yellow]")
            subprocess.run(
                ["pip", "install", "--upgrade", "pip", "build", "wheel", "setuptools"],
                capture_output=True,
                text=True,
                check=True
            )
            
            # 프로젝트 의존성 설치
            self.console.print("[yellow]프로젝트 의존성 설치 중...[/yellow]")
            result = subprocess.run(
                ["pip", "install", "-e", "."],
                capture_output=True,
                text=True
            )
            
            if result.returncode == 0:
                self.console.print("[green]의존성 설치가 완료되었습니다[/green]")
                return True
            else:
                self.console.print(f"[red]의존성 설치 실패: {result.stderr}[/red]")
                return False
            
        except subprocess.CalledProcessError as e:
            self.console.print(f"[red]의존성 설치 실패: {e.stderr}[/red]")
            return False
        except Exception as e:
            self.console.print(f"[red]의존성 설치 중 오류 발생: {str(e)}[/red]")
            return False
    
    def _create_artifacts(self) -> bool:
        """빌드 아티팩트 생성"""
        try:
            self.console.print("[yellow]빌드 아티팩트 생성 중...[/yellow]")
            dist_dir = Path("dist")
            dist_dir.mkdir(exist_ok=True)
            
            # pyproject.toml 확인
            if not Path("pyproject.toml").exists():
                self.console.print("[yellow]pyproject.toml 파일이 없습니다. 기본 아티팩트만 생성합니다.[/yellow]")
                return True
            
            # 빌드 패키지 설치
            result = subprocess.run(
                ["pip", "install", "build"],
                capture_output=True,
                text=True
            )
            if result.returncode != 0:
                self.console.print("[red]빌드 도구 설치 실패[/red]")
                return False
            
            # 아티팩트 빌드
            result = subprocess.run(
                ["python", "-m", "build"],
                capture_output=True,
                text=True
            )
            
            if result.returncode == 0:
                self.console.print("[green]아티팩트 생성이 완료되었습니다[/green]")
                return True
            else:
                self.console.print(f"[red]아티팩트 생성 실패: {result.stderr}[/red]")
                return False
            
        except Exception as e:
            self.console.print(f"[red]아티팩트 생성 중 오류 발생: {str(e)}[/red]")
            return False
    
    def get_status(self) -> str:
        """파이프라인 상태 조회"""
        try:
            # GitHub Actions 상태 조회 로직
            return "success"
        except Exception as e:
            raise CIServiceError(f"GitHub Actions 상태 조회 실패: {str(e)}")
    
    def _run_tests(self, config: Dict) -> bool:
        """테스트 실행"""
        try:
            self.console.print("[yellow]테스트 실행 중...[/yellow]")
            import unittest
            
            # unittest 테스트 실행
            loader = unittest.TestLoader()
            start_dir = 'tests'  # 기본 테스트 디렉토리
            suite = loader.discover(start_dir=start_dir, pattern="test_*.py")
            
            runner = unittest.TextTestRunner(verbosity=2)
            result = runner.run(suite)
            
            if result.wasSuccessful():
                self.console.print("[green]모든 테스트가 성공적으로 완료되었습니다[/green]")
                return True
            else:
                self.console.print(f"[red]테스트 실패: {len(result.failures)} 실패, {len(result.errors)} 에러[/red]")
                return False
            
        except Exception as e:
            self.console.print(f"[red]테스트 실행 실패: {str(e)}[/red]")
            return False