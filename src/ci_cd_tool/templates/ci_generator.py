from pathlib import Path
import os
import click
import git
from typing import List, Dict, Optional
from rich.console import Console

from ..analyzer.project_analyzer import ProjectStructure
from ..core.exceptions import GitHubError, ConfigurationError
from .template_content_generator import TemplateContentGenerator
from .git_manager import GitManager
from .template_manager import TemplateManager

class CIGenerator:
    def __init__(self, structure: ProjectStructure):
        self.structure = structure
        self.console = Console()
        self.templates_dir = Path("CCproject/ci_cd_tool/templates/templates")
        self.templates_dir.mkdir(parents=True, exist_ok=True)

    def generate(self) -> List[str]:
        """CI/CD 설정 파일 생성 및 Git 커밋"""
        try:
            # 1. CI 도구 결정
            ci_tool = self._determine_ci_tool()
            
            # 2. 설정 데이터 준비
            config_data = self._prepare_config_data()
            
            # 3. 템플릿 생성
            template_manager = TemplateManager(ci_tool, config_data)
            output_file = template_manager.create_template()
            
            # 4. Git 커밋 및 푸시
            if output_file:
                git_manager = GitManager(ci_tool, output_file, config_data['project_root'])
                git_manager.commit_and_push()
            
            return [output_file] if output_file else []
            
        except Exception as e:
            raise ConfigurationError(f"CI/CD 설정 생성 중 오류 발생: {str(e)}")

    def _determine_ci_tool(self) -> str:
        """프로젝트에 적합한 CI 도구 결정"""
        if self.structure.ci_provider:
            return self.structure.ci_provider
            
        try:
            repo = git.Repo('.')
            remote_url = repo.remotes.origin.url
            if 'github.com' in remote_url:
                return 'github'
            elif 'gitlab.com' in remote_url:
                return 'gitlab'
        except:
            pass
        return 'github'  # 기본값

    def _prepare_config_data(self) -> Dict:
        """CI 설정 데이터 준비"""
        return {
            'project_root': '.',
            'language': self.structure.language,
            'framework': self.structure.framework,
            'test_framework': self.structure.test_framework,
            'package_manager': self.structure.package_manager,
            'pipeline_stages': ['build', 'test', 'deploy']
        } 