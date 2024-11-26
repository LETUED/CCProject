from typing import Dict
from ..ci.base_ci import BaseCI
from ..ci.github_actions import GitHubActionsCI
from ..ci.gitlab_ci import GitLabCI, GitLabCIConfig
from ..ci.jenkins import JenkinsCI, JenkinsConfig
from ..core.exceptions import CIServiceError

class CIFactory:
    """CI 서비스 팩토리 클래스"""
    
    _providers = {
        'github': GitHubActionsCI,
        'github-actions': GitHubActionsCI,
        'github actions': GitHubActionsCI,  # 공백이 있는 형식 지원
        'github_actions': GitHubActionsCI,  # 언더스코어 형식 지원
    }
    
    @classmethod
    def create_ci_service(cls, provider: str, config: Dict) -> BaseCI:
        """CI 서비스 인스턴스 생성"""
        provider = provider.lower().replace('_', ' ')  # 정규화
        if provider not in cls._providers:
            raise CIServiceError(f"지원하지 않는 CI 도구입니다: {provider}")
            
        provider_class = cls._providers[provider]
        return provider_class(config) 