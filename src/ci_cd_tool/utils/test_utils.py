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
        """테스트 실행"""
        try:
            import unittest
            
            loader = unittest.TestLoader()
            start_dir = test_path or str(self.project_root)
            suite = loader.discover(start_dir=start_dir, pattern=pattern)
            
            runner = unittest.TextTestRunner(verbosity=2)
            result = runner.run(suite)
            
            return result.wasSuccessful()
            
        except Exception as e:
            raise TestError(f"테스트 실행 실패: {str(e)}") 