from pathlib import Path
from typing import Optional, List
import subprocess
from ..core.exceptions import TestError

class TestRunner:
    """테스트 실행 유틸리티"""
    
    def __init__(self, project_root: str = "."):
        self.project_root = Path(project_root)
    
    def run_tests(
        self,
        test_path: Optional[str] = None,
        pattern: str = "test_*.py",
        markers: Optional[List[str]] = None
    ) -> bool:
        """
        테스트 실행
        
        Args:
            test_path: 테스트 경로
            pattern: 테스트 파일 패턴
            markers: pytest 마커
            
        Returns:
            bool: 테스트 성공 여부
        """
        try:
            cmd = ["pytest"]
            
            if test_path:
                cmd.append(str(Path(test_path)))
            
            if markers:
                cmd.extend(["-m", " or ".join(markers)])
            
            cmd.extend(["--cov", "--cov-report=term-missing"])
            
            result = subprocess.run(cmd, cwd=self.project_root)
            return result.returncode == 0
            
        except Exception as e:
            raise TestError(f"테스트 실행 실패: {str(e)}") 