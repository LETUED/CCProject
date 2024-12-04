import boto3
from botocore.exceptions import ClientError
from .exceptions import DeployError
from ..config import Config
from .base_service import BaseService
from ..config.storage.base import AWSCredentialsManager
import os

class CDService(BaseService):
    """CD(Continuous Deployment) 서비스 클래스"""
    
    def __init__(self):
        super().__init__(use_logger=True)
        self.config = Config()
        self._ecr_client = None
        self._aws_credentials = None
        
    @property
    def aws_credentials(self):
        """AWS 자격 증명을 지연 초기화합니다"""
        if self._aws_credentials is None:
            credentials_manager = AWSCredentialsManager()
            self._aws_credentials = credentials_manager.get_credentials()
            if not self._aws_credentials:
                raise DeployError("AWS 자격 증명을 찾을 수 없습니다. AWS CLI 설정을 확인하세요.")
        return self._aws_credentials
        
    @property
    def ecr_client(self):
        """ECR 클라이언트를 지연 초기화합니다"""
        if self._ecr_client is None:
            credentials = self.aws_credentials
            region = 'us-east-1'
            self.logger.info(f"ECR 클라이언트 초기화 - 리전: {region}")
            self.logger.info(f"AWS CLI 설정된 리전: {boto3.Session().region_name}")
            self.logger.info(f"환경 변수 AWS_DEFAULT_REGION: {os.environ.get('AWS_DEFAULT_REGION')}")
            
            self._ecr_client = boto3.client(
                'ecr',
                region_name=region,
                aws_access_key_id=credentials['aws_access_key_id'],
                aws_secret_access_key=credentials['aws_secret_access_key']
            )
            self.logger.info(f"ECR 클라이언트 생성됨 - 실제 사용 리전: {self._ecr_client.meta.region_name}")
        return self._ecr_client
        
    def list_versions(self, repository_name: str = 'cc-repo'):
        """배포된 버전 목록을 조회합니다"""
        try:
            self.logger.info(f"ECR 리포지토리 {repository_name}의 이미지 목록 조회 중...")
            
            response = self.ecr_client.describe_images(
                repositoryName=repository_name,
                filter={'tagStatus': 'TAGGED'}
            )
            return response['imageDetails']
        except ClientError as e:
            error_msg = str(e)
            self.logger.error(f"버전 목록 조회 중 오류 발생: {error_msg}")
            raise DeployError(error_msg)
            
    def deploy(self, version: str):
        """지정된 버전을 배포합니다"""
        try:
            repository_name = self.config.get('ecr_repository', 'cc-repo')
            self.logger.info(f"버전 {version} 배포 시작")
            
            # 버전 존재 여부 확인
            try:
                self.ecr_client.describe_images(
                    repositoryName=repository_name,
                    imageIds=[{'imageTag': version}]
                )
            except ClientError as e:
                if e.response['Error']['Code'] == 'ImageNotFoundException':
                    raise DeployError(f"버전 {version}을 찾을 수 없습니다.")
                raise e
            
            # TODO: 실제 배포 로직 구현
            # 예: ECS 서비스 업데이트, EKS 배포 등
            
            return True
        except Exception as e:
            error_msg = str(e)
            self.logger.error(f"배포 중 오류 발생: {error_msg}")
            raise DeployError(f"배포 중 오류 발생: {error_msg}") 