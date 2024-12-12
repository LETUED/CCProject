import click
from .init import init
from .show import show
from .set import set

@click.group(name='config')
def config_group():
    """설정 관련 명령어"""
    pass

config_group.add_command(init)
config_group.add_command(show)
config_group.add_command(set)

__all__ = ['config_group'] 