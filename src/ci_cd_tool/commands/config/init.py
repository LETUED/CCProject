import click
from ..base import BaseCommand
from ...core.exceptions import error_handler
from ...config.config_manager import ConfigManager

class InitCommand(BaseCommand):
    """설정 초기화 명령어"""
    
    def execute(self) -> bool:
        try:
            self.info("기본 설정 초기화 중...")
            
            # 기본 설정 값
            default_config = {
                'ci': {
                    'provider': 'github',
                    'test_command': 'pytest',
                    'build_command': 'python -m build'
                },
                'cd': {
                    'environments': {
                        'dev': {'region': 'ap-northeast-2'},
                        'prod': {'region': 'ap-northeast-2'}
                    }
                },
                'dev': {
                    'aws': {
                        'region': 'ap-northeast-2',
                        'ecr': {
                            'repository': 'cc-tool-dev'
                        }
                    },
                    'repository': {
                        'name': 'cc-tool',
                        'branch': 'develop'
                    },
                    'deploy': {
                        'strategy': 'rolling',
                        'replicas': 2,
                        'healthcheck': {
                            'path': '/health',
                            'port': 8000
                        }
                    }
                },
                'test': {
                    'modules': [],
                    'coverage': {'min': 80}
                }
            }
            
            config = ConfigManager()
            for key, value in default_config.items():
                config.set_value(key, value)
                
            self.success("기본 설정이 초기화되었습니다")
            return True
                
        except Exception as e:
            self.error(f"설정 초기화 실패: {str(e)}")
            return False

@click.command()
@error_handler()
def init():
    """기본 설정 초기화"""
    command = InitCommand()
    return command.execute()

__all__ = ['init'] 