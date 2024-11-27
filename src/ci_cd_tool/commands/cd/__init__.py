import click
from .deploy import deploy
from .rollback import rollback
from .status import status
from .list import list_versions

@click.group(name='cd')
def cd_group():
    """CD(Continuous Deployment) 파이프라인 관리"""
    pass

cd_group.add_command(deploy)
cd_group.add_command(rollback)
cd_group.add_command(status)
cd_group.add_command(list_versions, name='list')

__all__ = ['cd_group'] 