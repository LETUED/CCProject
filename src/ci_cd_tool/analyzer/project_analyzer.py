from dataclasses import dataclass
from typing import List, Optional
from pathlib import Path
import os
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
        """프로젝트 구조를 분석하고 결과를 반환"""
        path = Path(project_path)
        self._validate_project_requirements(path)
        return self._analyze_project_structure(path)

    def _analyze_project_structure(self, path: Path) -> ProjectStructure:
        """프로젝트 구조 분석"""
        language = self._detect_language(path)
        framework = self._detect_framework(path)
        test_framework = self._detect_test_framework(path)
        dependencies = self._get_dependencies(path)
        ci_provider = self._detect_ci_provider(path)
        branch_strategy = self._detect_branch_strategy(path)
        
        return ProjectStructure(
            language=language,
            framework=framework,
            test_framework=test_framework,
            dependencies=dependencies,
            ci_provider=ci_provider,
            branch_strategy=branch_strategy
        )

    def _detect_language(self, path: Path) -> str:
        """프로젝트 주 언어 감지"""
        if (path / "requirements.txt").exists() or (path / "setup.py").exists():
            return "Python"
        elif (path / "package.json").exists():
            return "JavaScript/TypeScript"
        elif (path / "pom.xml").exists():
            return "Java"
        return "Unknown"

    def _detect_framework(self, path: Path) -> Optional[str]:
        """프레임워크 감지"""
        if self._has_dependency(path, ["django"]):
            return "Django"
        elif self._has_dependency(path, ["flask"]):
            return "Flask"
        elif self._has_dependency(path, ["fastapi"]):
            return "FastAPI"
        return None

    def _detect_test_framework(self, path: Path) -> Optional[str]:
        """테스트 프레임워크 감지"""
        if self._has_dependency(path, ["pytest"]):
            return "pytest"
        elif self._has_dependency(path, ["unittest"]):
            return "unittest"
        return None

    def _detect_ci_provider(self, path: Path) -> Optional[str]:
        """CI 제공자 감지"""
        if (path / ".github" / "workflows").exists():
            return "GitHub Actions"
        elif (path / ".gitlab-ci.yml").exists():
            return "GitLab CI"
        elif (path / "Jenkinsfile").exists():
            return "Jenkins"
        return None

    def _detect_branch_strategy(self, path: Path) -> Optional[str]:
        """브랜치 전략 감지"""
        try:
            from git import Repo
            repo = Repo(path)
            branches = [b.name for b in repo.branches]
            
            if "develop" in branches:
                return "GitFlow"
            elif "main" in branches:
                return "GitHub Flow"
        except:
            pass
        return None

    def _has_dependency(self, path: Path, dependencies: List[str]) -> bool:
        """특정 의존성 존재 여부 확인"""
        req_file = path / "requirements.txt"
        if req_file.exists():
            content = req_file.read_text().lower()
            return any(dep.lower() in content for dep in dependencies)
        return False

    def _get_dependencies(self, path: Path) -> List[str]:
        """프로젝트 의존성 목록 추출"""
        dependencies = []
        req_file = path / "requirements.txt"
        if req_file.exists():
            with open(req_file) as f:
                dependencies = [line.strip() for line in f if line.strip() 
                              and not line.startswith('#')]
        return dependencies

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