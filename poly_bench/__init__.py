"""
poly-bench: Non-Memorizable, Procedural Full-Stack Benchmark Generator for Coding Agents.
"""

from .models import (
    BugTaxonomy,
    ProceduralTaskSpec,
    EvaluationResult,
    BenchmarkSummary,
)
from .synthesizer import ProceduralASTSynthesizer
from .evaluator import BenchmarkEvaluator

__version__ = "0.1.0"
__all__ = [
    "BugTaxonomy",
    "ProceduralTaskSpec",
    "EvaluationResult",
    "BenchmarkSummary",
    "ProceduralASTSynthesizer",
    "BenchmarkEvaluator",
]
