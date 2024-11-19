import click
from ..core.container import Container
from ..core.exceptions import error_handler
from ..services.test_service import TestConfig
from rich.console import Console

@click.group(name='ci')
def ci_group():
    """
    CI 파이프라인 관련 명령어
    
    CI (Continuous Integration) pipeline related commands for building, testing, and quality checks.
    """
    pass

@ci_group.command(name='test')
@click.option('--env', default='staging', help='테스트 실행 환경 설정')
@click.option('--fast', is_flag=True, help='빠른 테스트 모드로 일부 테스트만 실행')
@click.option('--report', is_flag=True, help='테스트 결과 리포트를 생성')
@error_handler()
def test(env: str, fast: bool, report: bool):
    """테스트 실행"""
    container = Container()
    test_service = container.test_service()
    
    config = TestConfig(
        env=env,
        fast=fast,
        report=report
    )
    
    test_service.run_tests(config)

@ci_group.command(name='status')
@click.option('--env', help='상태를 확인할 환경 설정 / Environment to check status')
@click.option('--details', is_flag=True, help='상세 정보 표시 / Show detailed information')
@click.option('--limit', type=int, help='표시할 파이프라인 수 제한 / Limit the number of pipelines to display')
@error_handler()
def status(env: str, details: bool, limit: int):
    """
    파이프라인 상태 확인
    
    Check the current status of CI pipelines and their execution results.
    
    Options:
        --env: 특정 환경의 파이프라인 상태 확인
              Check pipeline status for specific environment
        
        --details: 커밋 정보, 테스트 결과 등 상세 정보 표시
                  Show detailed information including commits and test results
        
        --limit: 최근 N개의 파이프라인 결과만 표시
                Display only N most recent pipeline results
    """
    container = Container()
    status_service = container.status_service()
    status_service.show_status(env, details, limit)

@ci_group.command()
def build():
    """
    빌드 실행
    
    Execute build process for the project.
    
    프로젝트 소스 코드를 컴파일하고 실행 가능한 형태로 빌드니다.
    Compiles source code and creates executable artifacts.
    """
    console = Console()
    console.print("[bold green]빌드를 시작합니다...[/]")

@ci_group.command()
def config():
    """설정 관련 명령어"""
    pass 