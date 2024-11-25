import click
from rich.console import Console
from ..services.test_service import TestService, TestConfig
from ..core.exceptions import error_handler
from typing import Optional

@click.group(name='test')
def test_group():
    """
    테스트 관련 명령어
    """
    pass

@test_group.command(name='run')
@click.argument('module', required=False)
@click.option('--env', help='테스트 환경 (자동 감지되지 않는 경우 지정)')
@click.option('--report', is_flag=True, help='테스트 결과 리포트 생성')
@error_handler()
def run(module: Optional[str], env: Optional[str], report: bool):
    """테스트 실행
    
    현재 Git 브랜치를 기반으로 테스트 환경이 자동 감지됩니다.
    config.yml의 environments 설정을 참조하며, 없는 경우 기본 매핑을 사용합니다:
    - develop/development 브랜치 -> dev 환경
    - main/master 브랜치 -> prod 환경
    - 기타 브랜치 -> staging 환경
    """
    console = Console()
    test_service = TestService(console)
    
    config = TestConfig(
        env=env,  # None이면 자동 감지
        test_dir=f"unittest/{module}" if module else "unittest",
        report=report
    )
    
    test_service.run_tests(config) 