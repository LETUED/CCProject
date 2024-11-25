from pathlib import Path
from typing import Optional, Dict, Tuple
from rich.console import Console
from rich.panel import Panel
from ..utils.test_utils import TestRunner
from ..core.exceptions import TestError
import yaml
import os
from git import Repo

class TestManager:
    def __init__(self, console: Console):
        self.console = console
        self.config_file = Path(".cc/test_config.yml")
        self.unittest_dir = Path("unittest")
        self.test_runner = TestRunner()

    def init_structure(self):
        """테스트 디렉토리 구조 초기화"""
        try:
            # unittest 디렉토리 생성
            self.unittest_dir.mkdir(exist_ok=True)
            (self.unittest_dir / "__init__.py").touch()
            
            # 기본 설정 파일 생성
            self._create_default_config()
            
            # 기본 테스트 예제 생성
            self._create_example_test()
            
            self.console.print(Panel(
                "[green]테스트 디렉토리 구조가 성공적으로 초기화되었습니다.[/green]",
                title="초기화 완료",
                border_style="green"
            ))
            
        except Exception as e:
            raise TestError(f"테스트 구조 초기화 실패: {str(e)}")

    def create_module(self, module_name: str):
        """새로운 테스트 모듈 생성"""
        try:
            module_dir = self.unittest_dir / module_name
            module_dir.mkdir(exist_ok=True)
            
            # __init__.py 생성
            (module_dir / "__init__.py").touch()
            
            # 기본 테스트 파일 생성
            test_file = module_dir / f"test_{module_name}.py"
            if not test_file.exists():
                test_content = self._generate_test_template(module_name)
                test_file.write_text(test_content)
            
            # 설정 파일 업데이트
            self._update_config_modules(module_name)
            
            self.console.print(Panel(
                f"[green]테스트 모듈이 생성되었습니다: {module_name}[/green]",
                title="모듈 생성",
                border_style="green"
            ))
            
        except Exception as e:
            raise TestError(f"테스트 모듈 생성 실패: {str(e)}")

    def _detect_environment(self) -> Tuple[str, str]:
        """현재 Git 브랜치를 기반으로 환경 감지"""
        try:
            repo = Repo('.')
            current_branch = repo.active_branch.name
            
            # config.yml에서 환경 설정 로드
            config_manager = ConfigurationManager()
            config = config_manager.load()
            environments = config.get('environments', {})
            
            # 브랜치 이름으로 환경 찾기
            for env, env_config in environments.items():
                if env_config.get('branch') == current_branch:
                    return env, current_branch
            
            # 기본 매핑 사용
            if current_branch in ['develop', 'development']:
                return 'dev', current_branch
            elif current_branch in ['main', 'master']:
                return 'prod', current_branch
            
            return 'staging', current_branch
            
        except Exception as e:
            self.console.print(f"[yellow]Git 브랜치 감지 실패: {str(e)}[/yellow]")
            return 'staging', 'unknown'

    def run_tests(self, module_name: Optional[str] = None, pattern: Optional[str] = None, env: Optional[str] = None) -> bool:
        """테스트 실행"""
        try:
            # 환경이 지정되지 않은 경우 자동 감지
            if not env:
                env, branch = self._detect_environment()
                self.console.print(f"[blue]Git 브랜치: {branch}[/blue]")
            
            test_path = self.unittest_dir
            if module_name:
                test_path = test_path / module_name
                if not test_path.exists():
                    raise TestError(f"테스트 모듈을 찾을 수 없습니다: {module_name}")
            
            self.console.print(f"[blue]테스트 실행 중... ({test_path})[/blue]")
            self.console.print(f"[blue]환경: {env}[/blue]")
            
            # 환경 변수 설정
            os.environ['TEST_ENV'] = env
            
            success = self.test_runner.run_tests(
                test_path=str(test_path),
                pattern=pattern or "test_*.py"
            )
            
            if success:
                self.console.print("[green]테스트가 성공적으로 완료되었습니다.[/green]")
            else:
                self.console.print("[red]테스트 실행 중 실패가 발생했습니다.[/red]")
            
            return success
            
        except Exception as e:
            raise TestError(f"테스트 실행 실패: {str(e)}")

    def _create_default_config(self):
        """기본 테스트 설정 파일 생성"""
        if not self.config_file.exists():
            config = {
                "test_config": {
                    "root_dir": "unittest",
                    "modules": [],
                    "patterns": ["test_*.py"],
                    "options": {
                        "verbosity": 2,
                        "failfast": False
                    }
                }
            }
            self.config_file.parent.mkdir(parents=True, exist_ok=True)
            self.config_file.write_text(yaml.dump(config))

    def _create_example_test(self):
        """기본 예제 테스트 파일 생성"""
        example_file = self.unittest_dir / "test_example.py"
        if not example_file.exists():
            example_content = self._generate_test_template("example")
            example_file.write_text(example_content)

    def _generate_test_template(self, module_name: str) -> str:
        """테스트 파일 템플릿 생성"""
        return f'''import unittest

class Test{module_name.title()}(unittest.TestCase):
    def setUp(self):
        """테스트 설정"""
        pass
        
    def tearDown(self):
        """테스트 정리"""
        pass
        
    def test_example(self):
        """예제 테스트"""
        self.assertTrue(True)

if __name__ == '__main__':
    unittest.main()
'''

    def _update_config_modules(self, module_name: str):
        """설정 파일의 모듈 목록 업데이트"""
        if self.config_file.exists():
            config = yaml.safe_load(self.config_file.read_text())
            if module_name not in config["test_config"]["modules"]:
                config["test_config"]["modules"].append(module_name)
                self.config_file.write_text(yaml.dump(config))
        