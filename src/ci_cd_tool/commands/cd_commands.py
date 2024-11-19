import click
from rich.console import Console
from ..core.container import Container
from ..core.exceptions import error_handler

@click.group(name='cd')
def cd_group():
    """CD 파이프라인 관련 명령어"""
    pass

@cd_group.command()
@click.option('--env', required=True, help='배포할 환경 설정')
@click.option('--version', required=True, help='배포할 버전')
@error_handler()
def deploy(env: str, version: str):
    """환경별 배포 실행"""
    container = Container()
    deploy_service = container.deploy_service()
    
    console = Console()
    console.print("[green]배포가 시작되었습니다[/green]")
    console.print(f"[blue]환경: {env}, 버전: {version}[/blue]")
    
    deploy_service.deploy(env, version)

@cd_group.command()
@click.option('--version', required=True, help='롤백할 버전')
@error_handler()
def rollback(version: str):
    """이전 버전으로 롤백"""
    container = Container()
    deploy_service = container.deploy_service()
    
    console = Console()
    console.print("[green]롤백이 시작되었습니다[/green]")
    console.print(f"[blue]롤백 버전: {version}[/blue]")
    
    deploy_service.rollback(version)