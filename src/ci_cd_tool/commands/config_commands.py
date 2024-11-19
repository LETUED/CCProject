import click
from rich.console import Console

@click.group(name='config')
def config_group():
    """
    설정 관련 명령어
    
    Configuration related commands for managing tool settings and preferences.
    """
    pass

@config_group.command()
def init():
    """설정 초기화"""
    console = Console()
    console.print("[green]설정 초기화[/green]")

@config_group.command()
def show():
    """현재 설정 표시"""
    console = Console()
    console.print("[green]현재 설정을 표시합니다[/green]")

# 명시적으로 export
__all__ = ['config_group'] 