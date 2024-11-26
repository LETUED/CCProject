from dataclasses import dataclass
from typing import Optional

@dataclass
class TestConfig:
    test_dir: str
    env: Optional[str] = None
    report: bool = False 