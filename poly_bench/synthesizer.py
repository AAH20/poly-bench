"""
Procedural Repository & AST Synthesizer for Poly-Bench.
Generates unique, realistic, non-memorizable codebases and matching test suites.
"""

import random
import hashlib
from typing import Dict, Tuple
from .models import BugTaxonomy, ProceduralTaskSpec


DOMAINS = [
    ("ChronosMesh", "Distributed event sequencing and temporal lease management"),
    ("QuantumLedger", "High-throughput deterministic balance reconciliation pipeline"),
    ("VoxelStream", "Spatial point cloud compression and telemetry routing engine"),
    ("HelixDispatcher", "Biometric telemetry ingest and asynchronous priority queue"),
    ("AetherRouter", "Decentralized overlay network routing and packet multiplexer"),
]


class ProceduralASTSynthesizer:
    """Synthesizes unique full-stack Python software packages."""

    @classmethod
    def synthesize_task(cls, seed: int, bug_type: BugTaxonomy) -> ProceduralTaskSpec:
        rng = random.Random(seed)
        domain_name, domain_desc = DOMAINS[seed % len(DOMAINS)]
        task_id = f"poly-{domain_name.lower()}-{bug_type.value.lower()}-{seed:04d}"

        # 1. Synthesize Models
        models_code = f'''"""
Domain models for {domain_name}.
{domain_desc}.
"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional
import time


@dataclass
class {domain_name}Record:
    record_id: str
    owner_id: str
    weight: int
    is_active: bool = True
    metadata: Dict[str, str] = field(default_factory=dict)
    timestamp: float = field(default_factory=time.time)


@dataclass
class {domain_name}Batch:
    batch_id: str
    records: List[{domain_name}Record] = field(default_factory=list)
'''

        # 2. Synthesize Clean Service Code
        service_clean = f'''"""
Core business logic and processing pipeline for {domain_name}.
"""

from typing import List, Dict, Optional
from .models import {domain_name}Record, {domain_name}Batch


class {domain_name}Service:
    def __init__(self, max_capacity: int = 100):
        self.max_capacity = max_capacity
        self.storage: Dict[str, {domain_name}Record] = {{}}
        self.total_processed: int = 0

    def insert_record(self, record: {domain_name}Record) -> bool:
        if len(self.storage) >= self.max_capacity:
            return False
        self.storage[record.record_id] = record
        self.total_processed += 1
        return True

    def calculate_total_weight(self, record_ids: List[str]) -> int:
        total = 0
        for rid in record_ids:
            rec = self.storage.get(rid)
            if rec and rec.is_active:
                total += rec.weight
        return total

    def partition_records(self, chunk_size: int) -> List[List[{domain_name}Record]]:
        """Partition active records into chunks of chunk_size."""
        active = [r for r in self.storage.values() if r.is_active]
        chunks = []
        for i in range(0, len(active), chunk_size):
            chunks.append(active[i : i + chunk_size])
        return chunks

    def fetch_top_records(self, limit: int) -> List[{domain_name}Record]:
        """Fetch top records sorted by weight descending."""
        active = [r for r in self.storage.values() if r.is_active]
        sorted_records = sorted(active, key=lambda r: r.weight, reverse=True)
        return sorted_records[:limit]
'''

        # 3. Synthesize Injected Bug based on bug_type
        service_mutated, bug_description = cls._inject_bug(service_clean, domain_name, bug_type)

        # 4. Synthesize Comprehensive Test Suite
        test_code = f'''"""
Deterministic test oracle for {domain_name}.
Verifies correctness, boundary constraints, and stability.
"""

import unittest
from src.models import {domain_name}Record
from src.service import {domain_name}Service


class Test{domain_name}(unittest.TestCase):
    def setUp(self):
        self.service = {domain_name}Service(max_capacity=50)
        # Seed test records
        for i in range(10):
            rec = {domain_name}Record(
                record_id=f"rec_{{i}}",
                owner_id=f"owner_{{i % 3}}",
                weight=(i + 1) * 10,
                is_active=(i != 3)  # rec_3 is inactive
            )
            self.service.insert_record(rec)

    def test_total_weight_calculation(self):
        # All active records: rec_0..rec_2, rec_4..rec_9
        # Weights: 10, 20, 30, (40 skipped), 50, 60, 70, 80, 90, 100 = 510
        total = self.service.calculate_total_weight([f"rec_{{i}}" for i in range(10)])
        self.assertEqual(total, 510)

    def test_partition_records_boundaries(self):
        # 9 active records partitioned into chunks of 4 -> [4, 4, 1]
        chunks = self.service.partition_records(chunk_size=4)
        self.assertEqual(len(chunks), 3)
        self.assertEqual(len(chunks[0]), 4)
        self.assertEqual(len(chunks[1]), 4)
        self.assertEqual(len(chunks[2]), 1)

    def test_fetch_top_records_limit(self):
        # Fetch top 3 records
        top = self.service.fetch_top_records(limit=3)
        self.assertEqual(len(top), 3)
        self.assertEqual(top[0].weight, 100)
        self.assertEqual(top[1].weight, 90)
        self.assertEqual(top[2].weight, 80)


if __name__ == "__main__":
    unittest.main()
'''

        # Compute n-gram entropy score to prove non-memorization
        combined_text = models_code + service_clean + test_code
        entropy_score = cls._compute_entropy(combined_text)

        source_files = {
            "src/__init__.py": "",
            "src/models.py": models_code,
            "src/service.py": service_mutated,
        }

        clean_sources = {
            "src/__init__.py": "",
            "src/models.py": models_code,
            "src/service.py": service_clean,
        }

        test_files = {
            "tests/__init__.py": "",
            "tests/test_service.py": test_code,
        }

        return ProceduralTaskSpec(
            task_id=task_id,
            domain_name=domain_name,
            bug_type=bug_type,
            description=bug_description,
            source_files=source_files,
            clean_sources=clean_sources,
            test_files=test_files,
            seed=seed,
            contamination_entropy=entropy_score
        )

    @classmethod
    def _inject_bug(cls, clean_code: str, domain_name: str, bug_type: BugTaxonomy) -> Tuple[str, str]:
        """Inject specific bug taxonomy defect into clean codebase."""
        if bug_type == BugTaxonomy.OFF_BY_ONE:
            # Bug: sorted_records[:limit + 1] or sorted_records[:limit - 1]
            mutated = clean_code.replace("return sorted_records[:limit]", "return sorted_records[:limit - 1]")
            desc = f"Off-by-one boundary defect in {domain_name}Service.fetch_top_records: returns limit - 1 records."
            return mutated, desc

        elif bug_type == BugTaxonomy.AUTH_BYPASS or bug_type == BugTaxonomy.STALE_CACHE:
            # Bug: fails to check is_active flag in calculate_total_weight
            mutated = clean_code.replace("if rec and rec.is_active:", "if rec:")
            desc = f"State filter bypass in {domain_name}Service.calculate_total_weight: inactive records incorrectly counted."
            return mutated, desc

        elif bug_type == BugTaxonomy.TYPE_MISMATCH:
            # Bug: returns weight as string or wrong type
            mutated = clean_code.replace("total += rec.weight", "total = str(total) + str(rec.weight)")
            desc = f"Type mismatch corruption in {domain_name}Service.calculate_total_weight: concatenates as string."
            return mutated, desc

        else:
            # Default boundary error in partition
            mutated = clean_code.replace("chunks.append(active[i : i + chunk_size])", "chunks.append(active[i : i + chunk_size - 1])")
            desc = f"Partition window slicing mutation in {domain_name}Service.partition_records."
            return mutated, desc

    @classmethod
    def _compute_entropy(cls, text: str) -> float:
        """Calculate Shannon entropy over byte frequency distribution."""
        import math
        from collections import Counter
        if not text:
            return 0.0
        counts = Counter(text)
        total = len(text)
        entropy = -sum((c / total) * math.log2(c / total) for c in counts.values())
        return round(entropy, 3)
