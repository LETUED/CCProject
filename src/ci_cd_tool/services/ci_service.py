from dataclasses import dataclass
from typing import Optional, Dict
from rich.console import Console
from ..ci.base_ci import BaseCI
from ..core.factory import CIFactory
from ..core.exceptions import CIServiceError, CommandError
from .base_service import BaseService

@dataclass
class CIConfig:
    """CI 설정 정보"""
    stage: str
    provider: str
    config_path: str
    environment: Optional[str] = None
    test_command: Optional[str] = None
    build_command: Optional[str] = None

class CIService(BaseService):
    """CI 서비스 관리 클래스"""
    
    def __init__(self, console: Console):
        super().__init__(use_logger=True)
        self.console = console
        self._ci_provider: Optional[BaseCI] = None
        
    def initialize(self, config: CIConfig) -> bool:
        """CI 서비스 초기화"""
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
        if not self._ci_provider:
            raise CIServiceError("CI 서비스가 초기화되지 않았습니다")
        
        try:
            self.logger.info("CI 파이프라인 실행 시작")
            return self._ci_provider.run_pipeline(config)
        except Exception as e:
            error_msg = str(e)
            self.logger.error(f"파이프라인 실행 중 오류 발생: {error_msg}")
            raise CommandError(f"파이프라인 실행 중 오류 발생: {error_msg}")
            
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
                return self.run_pipeline(stage_config)
            else:
                raise CIServiceError(f"지원하지 않는 스테이지입니다: {config.stage}")
                
        except Exception as e:
            error_msg = str(e)
            self.logger.error(f"스테이지 실행 중 오류 발생: {error_msg}")
            raise CIServiceError(f"스테이지 실행 실패: {error_msg}")
            
    def _prepare_provider_config(self, config: CIConfig) -> Dict:
        """CI 제공자별 설정 준비"""
        return {
            'config_path': config.config_path,
            'environment': config.environment,
            'test_command': config.test_command,
            'build_command': config.build_command
        }