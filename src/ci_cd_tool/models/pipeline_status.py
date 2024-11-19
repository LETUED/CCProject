from dataclasses import dataclass
from datetime import datetime
from typing import List, Optional

@dataclass
class JobStatus:
    name: str
    status: str
    conclusion: str

@dataclass
class PipelineRun:
    status: str
    conclusion: str
    commit_message: str
    run_id: str
    run_url: str
    actor: str
    created_at: datetime
    updated_at: datetime
    jobs: Optional[List[JobStatus]] = None

@dataclass
class PipelineSummary:
    success_count: int
    failure_count: int
    in_progress_count: int 