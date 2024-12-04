import click
from ..base import BaseCommand
from ...core.exceptions import error_handler
from rich.table import Table
from typing import Optional

class ListCommand(BaseCommand):
    def execute(self, env: Optional[str] = None) -> bool:
        try:
            cd_service = self.container.cd_service()
            
            if env:
                # 특정 환경의 리포지토리 조회
                repository_name = f"cc-repo-{env}" if env != 'prod' else 'cc-repo'
                versions = cd_service.list_versions(repository_name)
            else:
                # 기본 리포지토리 조회
                versions = cd_service.list_versions('cc-repo')
            
            if not versions:
                self.warning("배포 가능한 버전이 없습니다.")
                return True
            
            table = Table(title="배포 가능한 버전 목록")
            table.add_column("버전", style="cyan")
            table.add_column("생성일", style="green")
            table.add_column("상태", style="yellow")
            table.add_column("환경", style="blue")
            
            for version in versions:
                # ECR 이미지 태그 정보 처리
                tags = version.get('imageTags', [])
                digest = version.get('imageDigest', '')[:7]  # 다이제스트 앞부분만 표시
                pushed_at = version.get('imagePushedAt', '')
                
                # 각 태그에 대해 행 추가
                if tags:
                    for tag in tags:
                        table.add_row(
                            tag,  # 이미지 태그
                            pushed_at.strftime("%Y-%m-%d %H:%M:%S") if pushed_at else '',  # 푸시 시간
                            'available',  # 상태
                            env or "모든 환경"  # 환경
                        )
                else:
                    # 태그가 없는 경우 다이제스트 사용
                    table.add_row(
                        f"sha256:{digest}",
                        pushed_at.strftime("%Y-%m-%d %H:%M:%S") if pushed_at else '',
                        'available',
                        env or "모든 환경"
                    )
                
            self.console.print(table)
            return True
            
        except Exception as e:
            error_msg = str(e)
            if "UnrecognizedClientException" in error_msg:
                self.error(
                    "AWS 자격 증명이 유효하지 않습니다.\n"
                    "다음 방법으로 해결해보세요:\n"
                    "1. AWS CLI 설정 확인: aws configure\n"
                    "2. 환경 변수 확인: AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY\n"
                    "3. ~/.aws/credentials 파일 확인"
                )
            elif "AccessDeniedException" in error_msg:
                self.error(
                    "AWS ECR 접근 권한이 없습니다.\n\n"
                    "AWS 관리자에게 다음 작업을 요청하세요:\n"
                    "1. ECR 접근을 위한 권한 추가:\n"
                    "   - ecr:DescribeRepositories\n"
                    "   - ecr:DescribeImages\n"
                    "   - ecr:ListImages\n"
                    "   - ecr:BatchGetImage\n\n"
                    "2. 다음 IAM 정책을 사용자 'LETUED'에게 연결:\n"
                    "{\n"
                    '    "Version": "2012-10-17",\n'
                    '    "Statement": [\n'
                    '        {\n'
                    '            "Effect": "Allow",\n'
                    '            "Action": [\n'
                    '                "ecr:DescribeRepositories",\n'
                    '                "ecr:DescribeImages",\n'
                    '                "ecr:ListImages",\n'
                    '                "ecr:BatchGetImage"\n'
                    '            ],\n'
                    '            "Resource": "*"\n'
                    '        }\n'
                    '    ]\n'
                    "}\n\n"
                    "또는 'AmazonEC2ContainerRegistryReadOnly' 관리형 정책 연결 요청\n\n"
                    "현재 사용자는 IAM 정책을 직접 관리할 권한이 없습니다."
                )
            elif "RepositoryNotFoundException" in error_msg:
                self.error(
                    "ECR 리포지토리를 찾을 수 없습니다.\n"
                    "다음 방법으로 해결해보세요:\n"
                    "1. AWS 관리자에게 ECR 리포지토리 생성 요청\n"
                    "2. 올바른 AWS 리전을 사용하고 있는지 확인\n"
                    "3. 리포지토리 이름이 올바른지 확인"
                )
            else:
                self.error(f"버전 목록 조회 중 오류 발생: {error_msg}")
            return False

@click.command(name='list')
@click.option('--env', help='환경 지정')
@error_handler()
def list_versions(env: Optional[str]):
    """배포 가능한 버전 목록 조회"""
    command = ListCommand()
    return command.execute(env) 