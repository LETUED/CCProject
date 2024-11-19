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

class GitHubError(CLIError):
    """GitHub 연동 관련 에러"""
    pass

class ProjectConfigError(CLIError):
    """프로젝트 설정 관련 에러"""
    pass

class NoGitRepositoryError(ProjectConfigError):
    """Git 저장소가 없을 때 발생하는 에러"""
    pass

class NoDependencyFileError(ProjectConfigError):
    """의존성 파일이 없을 때 발생하는 에러"""
    pass

def error_handler(console: Optional[Console] = None):
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