import click
from ..base import BaseCommand
from ...core.exceptions import error_handler
import boto3
import time

class InitCommand(BaseCommand):
    def execute(self, env: str) -> bool:
        try:
            self.info(f"{env} 환경 초기화 중...")
            
            # IAM 클라이언트 생성
            iam = boto3.client('iam', region_name='us-east-1')
            
            # ECS 서비스 연결 역할 생성
            try:
                self.info("ECS 서비스 연결 역할 생성 중...")
                iam.create_service_linked_role(
                    AWSServiceName='ecs.amazonaws.com',
                    Description='ECS Service Linked Role'
                )
                # 역할이 생성되고 전파될 때까지 대기
                time.sleep(10)
            except iam.exceptions.InvalidInputException as e:
                if 'Service role name AWSServiceRoleForECS has been taken' in str(e):
                    self.info("ECS 서비스 연결 역할이 이미 존재합니다.")
                else:
                    raise e
            
            # ECR 리포지토리 생성
            ecr = boto3.client('ecr', region_name='us-east-1')
            repository_name = f"cc-repo-{env}" if env != 'prod' else 'cc-repo'
            
            try:
                self.info(f"ECR 리포지토리 생성 중: {repository_name}")
                ecr.create_repository(
                    repositoryName=repository_name,
                    imageScanningConfiguration={'scanOnPush': True},
                    encryptionConfiguration={'encryptionType': 'AES256'}
                )
            except ecr.exceptions.RepositoryAlreadyExistsException:
                self.info(f"ECR 리포지토리가 이미 존재합니다: {repository_name}")
            
            # ECS 클라이언트 생성
            ecs = boto3.client('ecs', region_name='us-east-1')
            
            # 클러스터 이름 생성
            cluster_name = f"cc-cluster-{env}"
            
            # 클러스터 생성
            self.info(f"ECS 클러스터 생성 중: {cluster_name}")
            response = ecs.create_cluster(
                clusterName=cluster_name,
                capacityProviders=['FARGATE'],
                defaultCapacityProviderStrategy=[
                    {
                        'capacityProvider': 'FARGATE',
                        'weight': 1
                    }
                ]
            )
            
            # 서비스 생성
            service_name = f"cc-service-{env}"
            self.info(f"ECS 서비스 생성 중: {service_name}")
            
            # TODO: 서비스 생성 로직 추가
            # - 태스크 정의 생성
            # - 서비스 생성
            # - 로드 밸런서 설정
            
            self.success(f"{env} 환경 초기화가 완료되었습니다.")
            return True
            
        except Exception as e:
            self.error(f"환경 초기화 실패: {str(e)}")
            return False

@click.command(name='init')
@click.option('--env', required=True, type=click.Choice(['dev', 'staging', 'prod']), help='초기화할 환경')
@error_handler()
def init(env: str):
    """CD 환경 초기화"""
    command = InitCommand()
    return command.execute(env) 