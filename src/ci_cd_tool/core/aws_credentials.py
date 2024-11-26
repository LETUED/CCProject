import boto3
import os
from pathlib import Path
from configparser import ConfigParser
from typing import Optional

class AWSCredentialsManager:
    def __init__(self):
        self.credentials_file = Path.home() / '.aws' / 'credentials'
        self.config_file = Path.home() / '.aws' / 'config'
    
    def get_credentials(self) -> Optional[dict]:
        """AWS 자격 증명 조회"""
        # 환경 변수 확인
        access_key = os.getenv('AWS_ACCESS_KEY_ID')
        secret_key = os.getenv('AWS_SECRET_ACCESS_KEY')
        
        if access_key and secret_key:
            return {
                'aws_access_key_id': access_key,
                'aws_secret_access_key': secret_key
            }
            
        # credentials 파일 확인
        if self.credentials_file.exists():
            config = ConfigParser()
            config.read(self.credentials_file)
            if 'default' in config:
                return dict(config['default'])
                
        return None 