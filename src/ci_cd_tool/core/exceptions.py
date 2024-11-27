from typing import Optional
import functools
from rich.console import Console
from rich.panel import Panel
from functools import wraps
from typing import Callable
import click


class CLIError(Exception):
    """기본 CLI 에러"""
    pass

class ConfigurationError(CLIError):
    """설정 관련 에러"""
    pass

class ConfigError(CLIError):
    """설정 파일 관련 에러"""
    pass

class GitHubError(CLIError):
    """GitHub 관련 에러"""
    pass

class ProjectConfigError(Exception):
    """프로젝트 설정 관련 오류"""
    pass

class CIServiceError(CLIError):
    """CI 서비스 관련 에러"""
    pass

class TemplateError(CLIError):
    """템플릿 관련 에러"""
    pass

class CCError(Exception):
    """기본 예외 클래스"""
    pass

class TestError(Exception):
    """테스트 관련 오류"""
    pass

class CommandError(Exception):
    """명령어 실행 중 발생하는 기본 예외"""
    pass

class DeployError(Exception):
    """배포 관련 예외"""
    pass

class RollbackError(Exception):
    """롤백 관련 예외"""
    pass

def error_handler():
    """명령어 에러 처리 데코레이터"""
    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            try:
                return f(*args, **kwargs)
            except CommandError as e:
                click.echo(f"오류: {str(e)}", err=True)
                return False
            except DeployError as e:
                click.echo(f"배포 오류: {str(e)}", err=True)
                return False
            except RollbackError as e:
                click.echo(f"롤백 오류: {str(e)}", err=True)
                return False
            except ConfigError as e:
                click.echo(f"설정 오류: {str(e)}", err=True)
                return False
            except Exception as e:
                click.echo(f"예상치 못한 오류: {str(e)}", err=True)
                return False
        return wrapper
    return decorator