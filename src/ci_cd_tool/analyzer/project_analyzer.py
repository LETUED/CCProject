from dataclasses import dataclass
from typing import List, Optional
from pathlib import Path
from rich.console import Console
from ..core.exceptions import ProjectConfigError

@dataclass
class ProjectStructure:
    """프로젝트 구조 정보를 담는 데이터 클래스"""
    language: str
    framework: Optional[str] = None
    test_framework: Optional[str] = None
    dependencies: List[str] = None
    ci_provider: Optional[str] = None
    branch_strategy: Optional[str] = None
    package_manager: Optional[str] = None

    def __post_init__(self):
        self.dependencies = self.dependencies or []

class ProjectAnalyzer:
    """프로젝트 분석을 담당하는 클래스"""
    
    def __init__(self, console: Console):
        self.console = console

    def analyze(self, project_path: str = ".") -> ProjectStructure:
        """
        프로젝트 구조를 분석하고 결과를 반환합니다.
        
        Args:
            project_path: 분석할 프로젝트 경로
            
        Returns:
            ProjectStructure: 분석된 프로젝트 구조 정보
            
        Raises:
            ProjectConfigError: 프로젝트 설정이 잘못된 경우
        """
        path = Path(project_path)
        self._validate_project_requirements(path)
        return self._analyze_project_structure(path)

    def _validate_project_requirements(self, path: Path) -> None:
        missing = self._get_missing_requirements(path)
        if missing:
            raise ProjectConfigError(self._format_error_message(missing))

    def _get_missing_requirements(self, path: Path) -> List[str]:
        missing = []
        if not (path / ".git").exists():
            missing.append("Git 저장소")
        if not self._has_dependency_file(path):
            missing.append("의존성 파일")
        return missing

    def _has_dependency_file(self, path: Path) -> bool:
        dependency_files = [
            "requirements.txt",
            "setup.py",
            "pyproject.toml",
            "package.json"
        ]
        return any((path / file).exists() for file in dependency_files)