"""
Data models and taxonomy definitions for Poly-Bench.
Non-Memorizable, Procedural Full-Stack Benchmark Generator for Coding Agents.
"""

from dataclasses import dataclass, field
from enum import Enum
from typing import Dict, List, Optional, Any
import time


class BugTaxonomy(str, Enum):
    OFF_BY_ONE = "OFF_BY_ONE"
    RACE_CONDITION = "RACE_CONDITION"
    TYPE_MISMATCH = "TYPE_MISMATCH"
    AUTH_BYPASS = "AUTH_BYPASS"
    STALE_CACHE = "STALE_CACHE"
    UNHANDLED_EXCEPTION = "UNHANDLED_EXCEPTION"


@dataclass
class ProceduralTaskSpec:
    task_id: str
    domain_name: str
    bug_type: BugTaxonomy
    description: str
    source_files: Dict[str, str] = field(default_factory=dict)
    test_files: Dict[str, str] = field(default_factory=dict)
    clean_sources: Dict[str, str] = field(default_factory=dict)
    seed: int = 0
    contamination_entropy: float = 0.0
    created_at: float = field(default_factory=time.time)


@dataclass
class EvaluationResult:
    task_id: str
    success: bool
    passed_tests: int
    failed_tests: int
    test_output: str
    repaired_by_model: Optional[str] = None
    duration_ms: float = 0.0


@dataclass
class BenchmarkSummary:
    total_tasks: int = 0
    passed_tasks: int = 0
    failed_tasks: int = 0
    pass_at_1_rate: float = 0.0
    avg_entropy_score: float = 0.0
    total_duration_ms: float = 0.0
