import click
from ..core.container import Container
from ..core.exceptions import error_handler
from ..services.test_service import TestConfig
from rich.console import Console
from typing import Optional
from ..services.test_manager import TestManager

@click.group(name='ci')
def ci_group():
    """
    CI 파이프라인 관련 명령어
    
    CI (Continuous Integration) pipeline related commands for building, testing, and quality checks.
    """
    pass

@ci_group.command(name='test')
@click.argument('module', required=False)
@click.option('--pattern', help='테스트 파일 패턴 (예: test_login*)')
@click.option('--report', is_flag=True, help='테스트 결과 리포트 생성')
@click.option('--env', default='staging', help='테스트 환경 (staging/production)')
@error_handler()
def test(module: Optional[str], pattern: Optional[str], report: bool, env: str):
    """테스트 실행
    
    MODULE이 지정되면 해당 모듈의 테스트만 실행합니다.
    지정하지 않으면 전체 테스트를 실행합니다.
    """
    console = Console()
    test_manager = TestManager(console)
    
    if not test_manager.run_tests(module, pattern, env):
        raise click.ClickException("테스트 실행 실패")

@ci_group.command(name='test-init')
@error_handler()
def test_init():
    """테스트 디렉토리 구조 초기화"""
    console = Console()
    test_manager = TestManager(console)
    test_manager.init_structure()

@ci_group.command(name='test-add')
@click.argument('module')
@error_handler()
def test_add(module: str):
    """새로운 테스트 모듈 추가"""
    console = Console()
    test_manager = TestManager(console)
    test_manager.create_module(module)

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