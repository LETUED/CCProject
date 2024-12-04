from typing import Optional
import functools
from rich.console import Console
from rich.theme import Theme
from rich.style import Style
from functools import wraps
from typing import Callable
import click

# Rich 콘솔 설정
console = Console(theme=Theme({
    "error": "red bold",
    "warning": "yellow bold",
    "info": "cyan",
    "success": "green bold"
}))

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
                console.print(f"[error]오류:[/error] {str(e)}")
                console.print("[warning]해결 방법:[/warning] 명령어 구문을 확인하고, 필요한 옵션이 모두 제공되었는지 확인하세요.")
                return False
            except DeployError as e:
                console.print(f"[error]배포 오류:[/error] {str(e)}")
                console.print("[warning]해결 방법:[/warning] 배포 환경 설정과 버전 번호를 확인하세요. AWS 자격 증명과 권한도 확인하세요.")
                return False
            except RollbackError as e:
                console.print(f"[error]롤백 오류:[/error] {str(e)}")
                console.print("[warning]해결 방법:[/warning] 롤백할 버전이 올바른지 확인하세요. 롤백 가능한 상태인지도 점검하세요.")
                return False
            except ConfigError as e:
                console.print(f"[error]설정 오류:[/error] {str(e)}")
                console.print("[warning]해결 방법:[/warning] 설정 파일의 경로와 내용이 올바른지 확인하세요. 필요한 설정이 누락되지 않았는지 점검하세요.")
                return False
            except Exception as e:
                console.print(f"[error]예상치 못한 오류:[/error] {str(e)}")
                console.print("[warning]해결 방법:[/warning] 로그 파일을 확인하고, 필요시 지원팀에 문의하세요. 추가적인 디버깅이 필요할 수 있습니다.")
                return False
        return wrapper
    return decorator