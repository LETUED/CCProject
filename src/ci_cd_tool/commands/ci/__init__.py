import click
from .build import build
from .test import test
from .status import status

@click.group(name='ci')
def ci_group():
    """CI 관련 명령어 그룹"""
    pass

ci_group.add_command(build)
ci_group.add_command(test)
ci_group.add_command(status)

__all__ = ['ci_group'] 