import click
from ..base import BaseCommand
from ...core.exceptions import error_handler
from ...services.test_service import TestConfig
from typing import Optional

class TestCommand(BaseCommand):
    """테스트 실행 명령어 처리"""
    
    def execute(self, module: Optional[str], env: Optional[str], report: bool) -> bool:
        try:
            self.info("테스트 실행 준비 중...")
            
            test_service = self.container.test_service()
            config = TestConfig(
                env=env,
                test_dir=f"unittest/{module}" if module else "unittest",
                report=report
            )
            
            self.info(f"테스트 환경: {config.env or '자동 감지'}")
            result = test_service.run_tests(config)
            
            if result:
                self.success("모든 테스트가 성공적으로 완료되었습니다")
                return True
            else:
                self.error("일부 테스트가 실패했습니다")
                return False
                
        except Exception as e:
            self.error(f"테스트 실행 중 오류 발생: {str(e)}")
            return False

@click.command(name='test')
@click.argument('module', required=False)
@click.option('--env', help='테스트 환경 (자동 감지되지 않는 경우 지정)')
@click.option('--report', is_flag=True, help='테스트 결과 리포트 생성')
@error_handler()
def test(module: Optional[str], env: Optional[str], report: bool):
    """테스트 실행
    
    현재 Git 브랜치를 기반으로 테스트 환경이 자동 감지됩니다.
    config.yml의 environments 설정을 참조하며, 없는 경우 기본 매핑을 사용합니다:
    - develop/development 브랜치 -> dev 환경
    - main/master 브랜치 -> prod 환경
    - 기타 브랜치 -> staging 환경
    """
    command = TestCommand()
    return command.execute(module, env, report) 