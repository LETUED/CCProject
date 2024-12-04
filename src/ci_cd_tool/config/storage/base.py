from abc import ABC, abstractmethod
from typing import Dict, Any, Optional

class ConfigStorage(ABC):
    """설정 저장소 추상 클래스"""
    
    @abstractmethod
    def load(self) -> Optional[Dict[str, Any]]:
        """설정 로드"""
        pass
        
    @abstractmethod
    def save(self, config: Dict[str, Any]) -> bool:
        """설정 저장"""
        pass
        
    @abstractmethod
    def get_aws_credentials(self) -> Optional[Dict[str, str]]:
        """AWS 자격 증명 조회"""
        pass

class AWSCredentialsManager:
    """AWS 자격 증명 관리자"""
    
    def get_credentials(self) -> Optional[Dict[str, str]]:
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