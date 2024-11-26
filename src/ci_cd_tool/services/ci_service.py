from dataclasses import dataclass
from typing import Optional, Dict
from rich.console import Console
from ..ci.base_ci import BaseCI
from ..core.factory import CIFactory
from ..core.exceptions import CIServiceError

@dataclass
class CIConfig:
    """CI 설정 정보"""
    stage: str
    provider: str
    config_path: str
    environment: Optional[str] = None
    test_command: Optional[str] = None
    build_command: Optional[str] = None

class CIService:
    """CI 서비스 관리 클래스"""
    
    def __init__(self, console: Console):
        self.console = console
        self._ci_provider: Optional[BaseCI] = None
    
    def initialize(self, config: CIConfig) -> bool:
        """
        CI 서비스 초기화
        
        Args:
            config: CI 설정 정보
            
        Returns:
            bool: 초기화 성공 여부
        """
        try:
            provider_config = self._prepare_provider_config(config)
            self._ci_provider = CIFactory.create_ci_service(
                config.provider, 
                provider_config
            )
            return True
        except Exception as e:
            raise CIServiceError(f"CI 서비스 초기화 실패: {str(e)}")
    
    def run_pipeline(self, config: Dict) -> bool:
        """
        CI 파이프라인 실행
        
        Args:
            config: 파이프라인 설정
            
        Returns:
            bool: 실행 성공 여부
        """
        if not self._ci_provider:
            raise CIServiceError("CI 서비스가 초기화되지 않았습니다")
        
        try:
            return self._ci_provider.run_pipeline(config)
        except Exception as e:
            raise CIServiceError(f"파이프라인 실행 실패: {str(e)}") 
    
    def create_pipeline(self, config: Dict) -> bool:
        """파이프라인 생성"""
        if not self._ci_provider:
            raise CIServiceError("CI 서비스가 초기화되지 않았습니다")
        
        try:
            return self._ci_provider.create_pipeline()
        except Exception as e:
            raise CIServiceError(f"파이프라인 생성 실패: {str(e)}")
    
    def run_stage(self, config: CIConfig) -> bool:
        """특정 CI 스테이지 실행"""
        try:
            if not self.initialize(config):
                return False
            
            stage_config = {
                'stage': config.stage,
                'environment': config.environment,
                'config_path': config.config_path
            }
            
            if config.stage == 'build':
                return self.create_pipeline(stage_config) and self.run_pipeline(stage_config)
            elif config.stage == 'test':
                return self.run_tests(stage_config)
            else:
                raise CIServiceError(f"지원하지 않는 스테이지입니다: {config.stage}")
            
        except Exception as e:
            raise CIServiceError(f"스테이지 실행 실패: {str(e)}")
    
    def _prepare_provider_config(self, config: CIConfig) -> Dict:
        """CI 제공자별 설정 준비"""
        return {
            'config_path': config.config_path,
            'environment': config.environment,
            'test_command': config.test_command,
            'build_command': config.build_command
        }