from typing import Optional
import functools
from rich.console import Console
from rich.panel import Panel

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

class ProjectConfigError(CLIError):
    """프로젝트 설정 관련 에러"""
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

class TestError(CCError):
    """테스트 관련 예외 클래스"""
    pass

def error_handler(console: Optional[Console] = None):
    """에러 처리 데코레이터"""
    if console is None:
        console = Console()
        
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except CLIError as e:
                console.print(Panel(str(e), title="오류", border_style="red"))
                return False
            except Exception as e:
                console.print(Panel(
                    f"예상치 못한 오류: {str(e)}", 
                    title="시스템 오류",
                    border_style="red"
                ))
                return False
        return wrapper
    return decorator 