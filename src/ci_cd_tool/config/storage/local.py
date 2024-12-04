import os
import yaml
from typing import Dict, Any, Optional
from .base import ConfigStorage

class LocalConfigStorage(ConfigStorage):
    """로컬 파일 시스템 기반 설정 저장소"""
    
    def __init__(self, config_file: str = ".cc/config.yml"):
        self.config_file = config_file
        
    def load(self) -> Optional[Dict[str, Any]]:
        """설정 로드"""
        try:
            if not os.path.exists(self.config_file):
                return None
                
            with open(self.config_file, 'r') as f:
                return yaml.safe_load(f)
        except Exception as e:
            print(f"설정 로드 중 오류 발생: {str(e)}")
            return None
            
    def save(self, config: Dict[str, Any]) -> bool:
        """설정 저장"""
        try:
            os.makedirs(os.path.dirname(self.config_file), exist_ok=True)
            
            with open(self.config_file, 'w') as f:
                yaml.dump(config, f, default_flow_style=False)
            return True
        except Exception as e:
            print(f"설정 저장 중 오류 발생: {str(e)}")
            return False
            
    def get_aws_credentials(self) -> Optional[Dict[str, str]]:
        """AWS 자격 증명 조회"""
        try:
            import boto3
            session = boto3.Session()
            credentials = session.get_credentials()
            if credentials:
                frozen_credentials = credentials.get_frozen_credentials()
                return {
                    'aws_access_key_id': frozen_credentials.access_key,
                    'aws_secret_access_key': frozen_credentials.secret_key
                }
        except Exception as e:
            print(f"AWS 자격 증명 조회 중 오류 발생: {str(e)}")
        return None 