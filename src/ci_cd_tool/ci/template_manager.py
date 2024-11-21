from typing import Dict, Optional
from pathlib import Path
from ..templates.template_content_generator import TemplateContentGenerator

class TemplateManager:
    def __init__(self, ci_tool: str, config: Dict):
        self.ci_tool = ci_tool
        self.config = config

    def create_template(self) -> Optional[str]:
        """CI/CD 템플릿 파일을 생성하고 파일 경로를 반환합니다."""
        if self.ci_tool == "GitHub Actions":
            return self._create_github_workflow()
        elif self.ci_tool == "gitlab":
            return self._create_gitlab_ci()
        elif self.ci_tool == "jenkins":
            return self._create_jenkinsfile()
        else:
            raise ValueError(f"지원하지 않는 CI 도구입니다: {self.ci_tool}")

    def _create_github_workflow(self) -> str:
        """GitHub Actions workflow 템플릿을 생성합니다."""
        workflows_dir = Path(".github/workflows")
        workflows_dir.mkdir(parents=True, exist_ok=True)
        
        template_content = TemplateContentGenerator.get_content("GitHub Actions")
        output_file = workflows_dir / "ci.yml"
        output_file.write_text(template_content)
        return str(output_file)

    def _create_gitlab_ci(self) -> str:
        """GitLab CI 템플릿을 생성합니다."""
        template_content = TemplateContentGenerator.get_content("gitlab")
        output_file = Path(".gitlab-ci.yml")
        output_file.write_text(template_content)
        return str(output_file)

    def _create_jenkinsfile(self) -> str:
        """Jenkinsfile 템플릿을 생성합니다."""
        template_content = TemplateContentGenerator.get_content("jenkins")
        output_file = Path("Jenkinsfile")
        output_file.write_text(template_content)
        return str(output_file) 