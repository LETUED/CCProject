import click
from .deploy import deploy_command
from .rollback import rollback_command
from .status import status_command
from .list import list_command
from .push import push_command
from .init import init

@click.group(name='cd')
def cd_group():
    """CD(Continuous Deployment) 관련 명령어 그룹"""
    pass

cd_group.add_command(deploy_command)
cd_group.add_command(rollback_command)
cd_group.add_command(status_command)
cd_group.add_command(list_command)
cd_group.add_command(push_command)
cd_group.add_command(init)

__all__ = ['cd_group'] 