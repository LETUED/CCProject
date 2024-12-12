import click
from .init import init
from .add import add
from .commit import commit
from .status import status
from .push import push

@click.group(name='src')
def src_group():
    """소스 코드 관리 명령어 그룹"""
    pass


src_group.add_command(init)
src_group.add_command(add)
src_group.add_command(commit)
src_group.add_command(status)
src_group.add_command(push)

__all__ = ['src_group']
