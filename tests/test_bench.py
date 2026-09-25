"""
Unit tests for Poly-Bench procedural generation, bug injection, and evaluation.
"""

import unittest
from poly_bench.models import BugTaxonomy
from poly_bench.synthesizer import ProceduralASTSynthesizer
from poly_bench.evaluator import BenchmarkEvaluator


class TestPolyBench(unittest.TestCase):

    def test_synthesizer_structure(self):
        task = ProceduralASTSynthesizer.synthesize_task(101, BugTaxonomy.OFF_BY_ONE)
        self.assertTrue(task.task_id.startswith("poly-"))
        self.assertIn("src/models.py", task.source_files)
        self.assertIn("src/service.py", task.source_files)
        self.assertIn("tests/test_service.py", task.test_files)
        self.assertGreater(task.contamination_entropy, 3.5)

    def test_pristine_oracle_passes(self):
        task = ProceduralASTSynthesizer.synthesize_task(202, BugTaxonomy.OFF_BY_ONE)
        clean_res = BenchmarkEvaluator.evaluate_task(task, source_override=task.clean_sources)
        self.assertTrue(clean_res.success)
        self.assertEqual(clean_res.passed_tests, 3)
        self.assertEqual(clean_res.failed_tests, 0)

    def test_mutated_oracle_fails(self):
        task = ProceduralASTSynthesizer.synthesize_task(303, BugTaxonomy.OFF_BY_ONE)
        mutated_res = BenchmarkEvaluator.evaluate_task(task)
        self.assertFalse(mutated_res.success)
        self.assertGreater(mutated_res.failed_tests, 0)

    def test_repair_verification(self):
        task = ProceduralASTSynthesizer.synthesize_task(404, BugTaxonomy.AUTH_BYPASS)
        # 1. Broken fails
        broken_res = BenchmarkEvaluator.evaluate_task(task)
        self.assertFalse(broken_res.success)

        # 2. Model provides patch (clean sources)
        fixed_res = BenchmarkEvaluator.evaluate_task(
            task,
            source_override=task.clean_sources,
            model_name="Claude Opus 5.5"
        )
        self.assertTrue(fixed_res.success)
        self.assertEqual(fixed_res.repaired_by_model, "Claude Opus 5.5")


if __name__ == "__main__":
    unittest.main()
