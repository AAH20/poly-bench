"""
Isolated Test Runner & Contamination Scorer for Poly-Bench.
Executes test oracles against procedural codebases in ephemeral sandboxes.
"""

import os
import sys
import tempfile
import subprocess
import time
from typing import Dict, Optional
from .models import ProceduralTaskSpec, EvaluationResult


class BenchmarkEvaluator:
    """Evaluates agent repairs and pristine baselines in hermetic sub-environments."""

    @staticmethod
    def evaluate_task(
        task: ProceduralTaskSpec,
        source_override: Optional[Dict[str, str]] = None,
        model_name: Optional[str] = None
    ) -> EvaluationResult:
        """
        Executes test suite against current or patched task sources.
        """
        start_time = time.time()
        sources = source_override if source_override is not None else task.source_files

        with tempfile.TemporaryDirectory() as tmpdir:
            # 1. Write source files
            for rel_path, content in sources.items():
                full_path = os.path.join(tmpdir, rel_path)
                os.makedirs(os.path.dirname(full_path), exist_ok=True)
                with open(full_path, "w", encoding="utf-8") as f:
                    f.write(content)

            # 2. Write test files
            for rel_path, content in task.test_files.items():
                full_path = os.path.join(tmpdir, rel_path)
                os.makedirs(os.path.dirname(full_path), exist_ok=True)
                with open(full_path, "w", encoding="utf-8") as f:
                    f.write(content)

            # 3. Execute tests via subprocess
            env = os.environ.copy()
            env["PYTHONPATH"] = tmpdir

            proc = subprocess.run(
                [sys.executable, "-m", "unittest", "discover", "-s", "tests", "-p", "test_*.py"],
                cwd=tmpdir,
                env=env,
                capture_output=True,
                text=True
            )

            output = (proc.stdout + "\n" + proc.stderr).strip()
            success = (proc.returncode == 0)

            # Parse passed / failed counts
            passed = 0
            failed = 0
            if "Ran " in output:
                try:
                    ran_line = [l for l in output.split("\n") if "Ran " in l][0]
                    total_ran = int(ran_line.split()[1])
                    if success:
                        passed = total_ran
                        failed = 0
                    else:
                        failed = 1
                        passed = max(0, total_ran - failed)
                except Exception:
                    passed = 1 if success else 0
                    failed = 0 if success else 1
            else:
                passed = 1 if success else 0
                failed = 0 if success else 1

            duration_ms = (time.time() - start_time) * 1000.0

            return EvaluationResult(
                task_id=task.task_id,
                success=success,
                passed_tests=passed,
                failed_tests=failed,
                test_output=output,
                repaired_by_model=model_name,
                duration_ms=duration_ms
            )
