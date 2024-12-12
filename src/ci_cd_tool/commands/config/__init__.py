import click
from .init import init
from .show import show

@click.group(name='config')
def config_group():
    """설정 관리 명령어 그룹"""
    pass

config_group.add_command(init)
config_group.add_command(show)

__all__ = ['config_group'] 