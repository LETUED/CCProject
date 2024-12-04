from click import group, command, option
from ..core.cd import CDService
from ..core.exceptions import error_handler

@group(name='cd')
def cd_group():
    """CD(Continuous Deployment) 관련 명령어 그룹"""
    pass

@cd_group.command(name='list')
@error_handler()
def list_versions():
    """배포된 버전 목록을 조회합니다"""
    cd_service = CDService()
    return cd_service.list_versions()

@cd_group.command(name='deploy')
@option('--version', required=True, help='배포할 버전')
@error_handler()
def deploy(version):
    """지정된 버전을 배포합니다"""
    cd_service = CDService()
    return cd_service.deploy(version) 