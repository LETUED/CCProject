import click
from ..base import BaseCommand
from ...core.exceptions import error_handler
import subprocess
import os

class PushCommand(BaseCommand):
    def execute(self, version: str, env: str = None) -> bool:
        try:
            # ECR 리포지토리 주소 구성
            account_id = "545009827973"
            region = "us-east-1"
            repository = f"cc-repo-{env}" if env and env != 'prod' else 'cc-repo'
            ecr_url = f"{account_id}.dkr.ecr.{region}.amazonaws.com"
            image_url = f"{ecr_url}/{repository}:{version}"
            
            # ECR 로그인
            self.info("ECR 로그인 중...")
            login_cmd = f"aws ecr get-login-password --region {region} | docker login --username AWS --password-stdin {ecr_url}"
            subprocess.run(login_cmd, shell=True, check=True)
            
            # 도커 이미지 빌드
            self.info(f"도커 이미지 빌드 중: {version}")
            subprocess.run(f"docker build -t {repository}:{version} .", shell=True, check=True)
            
            # 이미지 태그 변경
            self.info("이미지 태그 변경 중...")
            subprocess.run(f"docker tag {repository}:{version} {image_url}", shell=True, check=True)
            
            # ECR에 이미지 푸시
            self.info("ECR에 이미지 푸시 중...")
            subprocess.run(f"docker push {image_url}", shell=True, check=True)
            
            self.success(f"버전 {version}이 성공적으로 푸시되었습니다.")
            return True
            
        except subprocess.CalledProcessError as e:
            self.error(f"명령어 실행 실패: {e.stderr if e.stderr else str(e)}")
            return False
        except Exception as e:
            self.error(f"이미지 푸시 중 오류 발생: {str(e)}")
            return False

@click.command(name='push')
@click.argument('version')
@click.option('--env', help='환경 (dev/staging/prod)')
@error_handler()
def push(version: str, env: str):
    """새로운 버전을 ECR에 푸시"""
    command = PushCommand()
    return command.execute(version, env) 