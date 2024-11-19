import git  # GitPython 라이브러리
import os
import click
from dataclasses import dataclass
from typing import Optional, List

# 템플릿 관련 모듈
class TemplateManager:
    def __init__(self, ci_tool, config_data):
        self.ci_tool = ci_tool
        self.config_data = config_data
        self.project_root = config_data.get('Project_Root', '.')
        self.template_filename = f"{ci_tool.lower()}_ci.yml"
        self.output_file = os.path.join(self.project_root, self.template_filename)
        self.templates_path = "CCproject/ci_cd_tool/templates/templates"
        self.default_template_file = os.path.join(self.templates_path, f"{ci_tool.lower()}.yml")

    def create_template(self):
        """템플릿 파일 생성"""
        if not os.path.exists(self.default_template_file):
            self._create_default_template()
        
        if not os.path.exists(self.default_template_file):
            click.echo(f"템플릿 파일을 찾을 수 없습니다: {self.default_template_file}")
            return

        template_content = self._read_template()
        self._write_template(template_content)
        return self.output_file

    def _create_default_template(self):
        """기본 템플릿 생성"""
        click.echo(f"{self.ci_tool} CI 템플릿 파일이 존재하지 않습니다. 기본 템플릿을 생성합니다.")
        default_template_content = TemplateContentGenerator.get_content(self.ci_tool)
        with open(self.default_template_file, 'w') as default_template:
            default_template.write(default_template_content)
        click.echo(f"기본 {self.ci_tool} CI 템플릿 파일이 생성되었습니다: {self.default_template_file}")

    def _read_template(self):
        """템플릿 파일 읽기"""
        with open(self.default_template_file, 'r') as file:
            return file.read()

    def _write_template(self, content):
        """템플릿 파일 쓰기"""
        os.makedirs(self.project_root, exist_ok=True)
        with open(self.output_file, 'w') as output:
            output.write(content)
        click.echo(f"프로젝트 루트에 {self.ci_tool} CI 템플릿 파일이 생성되었습니다: {self.output_file}")

# Git 관련 모듈
class GitManager:
    def __init__(self, ci_tool, template_file, project_root):
        self.ci_tool = ci_tool
        self.template_file = template_file
        self.project_root = project_root

    def commit_and_push(self):
        """Git 커밋 및 푸시"""
        try:
            repo = git.Repo(self.project_root)
            
            if not os.path.exists(self.template_file):
                click.echo(f"템플릿 파일을 찾을 수 없습니다: {self.template_file}")
                return

            repo.index.add([self.template_file])
            commit_message = f"Add {self.ci_tool} CI template"
            repo.index.commit(commit_message)
            
            origin = repo.remote(name='origin')
            origin.push()

            click.echo(f"{self.ci_tool} CI 템플릿 파일이 커밋되고 푸시되었습니다.")
        except git.exc.InvalidGitRepositoryError:
            click.echo("유효한 Git 리포지토리가 아닙니다. 먼저 Git 리포지토리를 초기화하세요.")
        except Exception as e:
            click.echo(f"템플릿 커밋 및 푸시 중 오류가 발생했습니다: {str(e)}")

# 템플릿 내용 생성 모듈
class TemplateContentGenerator:
    @staticmethod
    def get_content(ci_tool):
        """CI 도구별 기본 템플릿 내용 반환"""
        templates = {
            "GitHub Actions": """
name: CI Pipeline

on:
  push:
    branches:
      - main
  pull_request:
    branches:
      - main

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
    - name: Check out repository
      uses: actions/checkout@v2

    - name: Set up Python
      uses: actions/setup-python@v2
      with:
        python-version: '3.x'

    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install -r requirements.txt

    - name: Run tests
      run: pytest
        """,
            "GitLab CI": """
stages:
  - build
  - test
  - deploy

build:
  stage: build
  script:
    - echo "Building the project..."

test:
  stage: test
  script:
    - echo "Running tests..."

deploy:
  stage: deploy
  script:
    - echo "Deploying the project..."
        """,
            "Jenkins": """
pipeline {
    agent any
    stages {
        stage('Build') {
            steps {
                echo 'Building...'
            }
        }
        stage('Test') {
            steps {
                echo 'Testing...'
            }
        }
        stage('Deploy') {
            steps {
                echo 'Deploying...'
            }
        }
    }
}
        """
        }
        return templates.get(ci_tool, "# Unsupported CI tool")

# 메인 함수
def generate_and_commit_ci_template(ci_tool, config_data):
    """CI 템플릿 생성 및 Git 커밋/푸시 메인 함수"""
    template_manager = TemplateManager(ci_tool, config_data)
    output_file = template_manager.create_template()
    
    git_manager = GitManager(ci_tool, output_file, template_manager.project_root)
    git_manager.commit_and_push()

@dataclass
class CIConfiguration:
    project_root: str
    pipeline_stages: List[str]
    framework: str
    ci_tool: str
    remote_repo: Optional[str] = None
    python_version: Optional[str] = None
    gitlab_stages: Optional[List[str]] = None

class ConfigurationManager:
    def __init__(self):
        self.config = CIConfiguration()

    def save(self):
        # 설정 저장 로직
        pass

    def load(self):
        # 설정 로드 로직
        pass
