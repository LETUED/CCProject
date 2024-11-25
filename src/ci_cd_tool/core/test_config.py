from dataclasses import dataclass
from typing import List, Optional
from pathlib import Path

@dataclass
class TestConfig:
    """테스트 설정 클래스"""
    root_dir: Path = Path("unittest")
    test_modules: List[str] = None
    patterns: List[str] = None
    verbosity: int = 2
    failfast: bool = False
    report: bool = False
    report_dir: Path = Path("reports")
    env: str = 'staging'
    
    def __post_init__(self):
        self.test_modules = self.test_modules or []
        self.patterns = self.patterns or ["test_*.py"] 