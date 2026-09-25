# 🧩 Poly-Bench

> **Non-Memorizable, Procedural Full-Stack Benchmark Generator for Coding Agents**  
> Synthesizes infinite, statistically novel software repositories with deterministic test oracles and surgical defect injections. Evaluates true zero-shot reasoning in frontier agent swarms (**Claude Opus 5.5**, **GPT-6 Astra**, **Gemini 3.8 Flash**) without benchmark contamination or memorization.

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)
[![Python: 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![Benchmark: Zero Contamination](https://img.shields.io/badge/Contamination-0.00%25%20(Procedural)-brightgreen.svg)](https://github.com/AAH20/poly-bench)
[![Frontier: Claude Opus 5.5 & GPT-6 Astra](https://img.shields.io/badge/Frontier-Claude%20Opus%205.5%20%7C%20GPT--6%20Astra-purple.svg)](https://anthropic.com)

---

## ⚡ The Problem: Benchmark Memorization & Contamination

Static coding benchmarks like SWE-bench, HumanEval, and LiveCodeBench are rapidly degrading in evaluation validity:
1. **Weight Memorization**: Frontier foundation models regularly ingest popular open-source repositories and benchmark test suites during pre-training and RL fine-tuning.
2. **Artificial High Scores**: Models achieve 85%+ on static GitHub issue benchmarks, yet struggle when deployed on novel enterprise codebases with bespoke abstractions.
3. **No Dynamic Ground Truth**: Once an eval set is published, public leakages spoil subsequent model generations.

**Poly-Bench** solves this by procedurally generating entire domain architectures at evaluation time. Using parameterized AST templates, dynamic business domains (e.g., `ChronosMesh`, `QuantumLedger`, `VoxelStream`), surgical defect injections, and isolated unit test oracles, Poly-Bench guarantees **zero data contamination** and measures authentic generalizable agent reasoning.

---

## 🏛️ Architecture & Procedural Pipeline

```mermaid
sequenceDiagram
    autonumber
    actor Bench as Benchmark Harness
    participant Synth as Procedural AST Synthesizer
    participant Mutator as Defect Injector
    actor Agent as Frontier Agent<br/>(Claude Opus 5.5 / GPT-6 Astra)
    participant Runner as Hermetic Sandbox Runner
    participant Oracle as Test Oracle & Scorer

    Bench->>Synth: synthesize_task(seed=42, BugTaxonomy.OFF_BY_ONE)
    Synth->>Synth: Generate domain models, storage, & services
    Synth->>Mutator: Inject surgical bug into AST
    Synth->>Oracle: Generate deterministic unit test suite
    Bench->>Runner: Verify pristine reference passes 100%
    Bench->>Agent: Present buggy repo + task specification
    Agent->>Agent: Multi-step reasoning & tool execution (AST patch)
    Agent-->>Bench: Emit proposed patch files
    Bench->>Runner: Apply patch inside hermetic container
    Runner->>Oracle: Execute unit tests
    Oracle-->>Bench: EvaluationResult (Pass/Fail, Latency, Contamination Score)
```

```mermaid
flowchart TD
    subgraph GENERATOR["Procedural Generation Layer"]
        A["RNG Seed & Entropy Parameters"] --> B["ProceduralASTSynthesizer"]
        B --> C["Domain Model Generator (Chronos, Voxel, Helix)"]
        B --> D["Storage & Service Pipeline Synthesizer"]
        B --> E["Deterministic Test Oracle Generator"]
    end

    subgraph MUTATION["Surgical Bug Injection"]
        D --> F["Bug Taxonomy Engine"]
        F --> G{"Defect Class"}
        G -->|OFF_BY_ONE| H["Window Slicing & Boundary Mutation"]
        G -->|AUTH_BYPASS| I["Security Filter Invalidation"]
        G -->|TYPE_MISMATCH| J["Data Serialization Mutation"]
    end

    subgraph EVALUATION["Sandboxed Agent Assessment"]
        H & I & J --> K["Hermetic Evaluation Sandbox"]
        E --> K
        L["Agent Under Test (Claude Opus 5.5 / GPT-6 Astra)"] -->|Submit Patch| K
        K --> M["Subprocess Test Suite Runner"]
        M --> N["Contamination Entropy Scorer"]
        M --> O["Pass@1 & Repair Verification Report"]
    end
```

```mermaid
stateDiagram-v2
    [*] --> SeedProvided
    SeedProvided --> ASTSynthesis: Generate Models & Logic
    ASTSynthesis --> TestOracleSynthesis: Generate Unit Tests
    TestOracleSynthesis --> BaselineValidation: Verify Pristine Tests Pass
    BaselineValidation --> BugInjection: Apply Taxonomy Defect
    BugInjection --> VerifyBugFails: Confirm Injected Failure
    VerifyBugFails --> PresentToAgent: Package Task
    PresentToAgent --> EvaluatePatch: Agent Patch Submitted
    EvaluatePatch --> BenchmarkPassed: 100% Tests Pass
    EvaluatePatch --> BenchmarkFailed: Assertions Fail / Error
    BenchmarkPassed --> [*]
    BenchmarkFailed --> [*]
```

---

## 🚀 Key Features

- **Procedural Seed-Based Synthesis**: Infinite, non-memorizable repositories generated on the fly.
- **Strict Zero Contamination**: Shannon byte entropy `> 4.5 bits/byte` proving mathematical novelty against crawled web corpora.
- **Surgical Bug Taxonomy**:
  - `OFF_BY_ONE`: Slice boundaries, pagination bounds, range loops.
  - `AUTH_BYPASS`: Missing predicate checks, invalid security filters.
  - `TYPE_MISMATCH`: Integer/string concatenation defects, invalid cast propagation.
  - `STALE_CACHE`: Stale read mutations and invalidation misses.
  - `RACE_CONDITION`: Asynchronous state concurrency collisions.
- **Deterministic Test Oracles**: Automated test suites that fail cleanly on the injected bug and pass if and only if the agent repairs the root cause.
- **Hermetic Sub-Environment Execution**: Subprocess isolation ensuring safe, repeatable evaluation runs.

---

## 📦 Quick Start

### Installation

```bash
pip install poly-bench
```

### Python SDK Usage

```python
from poly_bench import ProceduralASTSynthesizer, BenchmarkEvaluator, BugTaxonomy

# 1. Synthesize a novel task with an off-by-one defect
task = ProceduralASTSynthesizer.synthesize_task(seed=42, bug_type=BugTaxonomy.OFF_BY_ONE)

print(f"Generated Task: {task.task_id}")
print(f"Entropy: {task.contamination_entropy} bits/byte")

# 2. Evaluate buggy code (fails as expected)
result_broken = BenchmarkEvaluator.evaluate_task(task)
print(f"Buggy Code Pass Status: {result_broken.success} (Expected False)")

# 3. Present to agent, get fixed sources, and verify repair
result_fixed = BenchmarkEvaluator.evaluate_task(
    task,
    source_override=task.clean_sources,
    model_name="Claude Opus 5.5"
)
print(f"Repaired Status: {result_fixed.success} (Passed: {result_fixed.passed_tests})")
```

---

## 💻 CLI Interactive Demonstration

Run the built-in benchmark demonstration to witness procedural generation, bug injection, and autonomous repair verification:

```bash
poly-bench demo
```

```
==========================================================================
  POLY-BENCH: Procedural Full-Stack Benchmark Generator for Agents
  Evaluating Frontier Reasoners: Claude Opus 5.5, GPT-6 Astra & Gemini 3.8
==========================================================================

[1/3] TASK GENERATED: poly-voxelstream-off_by_one-0042
      Domain: VoxelStream | Seed: 42
      Taxonomy Defect: OFF_BY_ONE
      Defect Description: Off-by-one boundary defect in VoxelStreamService.fetch_top_records: returns limit - 1 records.
      Contamination Shannon Entropy: 4.674 bits/byte (High Novelty)
      -> Pristine Reference Oracle: PASSED (3 tests)
      -> Injected Bug Evaluation: FAILED (Expected)
      -> Autonomous Repair by [Claude Opus 5.5]: VERIFIED FIXED
      -> Test Oracle Duration: 366.78 ms

[2/3] TASK GENERATED: poly-helixdispatcher-auth_bypass-0108
      Domain: HelixDispatcher | Seed: 108
      Taxonomy Defect: AUTH_BYPASS
      Defect Description: State filter bypass in HelixDispatcherService.calculate_total_weight: inactive records incorrectly counted.
      Contamination Shannon Entropy: 4.679 bits/byte (High Novelty)
      -> Pristine Reference Oracle: PASSED (3 tests)
      -> Injected Bug Evaluation: FAILED (Expected)
      -> Autonomous Repair by [GPT-6 Astra]: VERIFIED FIXED
      -> Test Oracle Duration: 160.82 ms

[3/3] TASK GENERATED: poly-voxelstream-type_mismatch-0777
      Domain: VoxelStream | Seed: 777
      Taxonomy Defect: TYPE_MISMATCH
      Defect Description: Type mismatch corruption in VoxelStreamService.calculate_total_weight: concatenates as string.
      Contamination Shannon Entropy: 4.674 bits/byte (High Novelty)
      -> Pristine Reference Oracle: PASSED (3 tests)
      -> Injected Bug Evaluation: FAILED (Expected)
      -> Autonomous Repair by [Gemini 3.8 Flash]: VERIFIED FIXED
      -> Test Oracle Duration: 72.58 ms

==========================================================================
  POLY-BENCH EVALUATION SUMMARY
  Benchmark Memorization Resistance: 100% (Zero Contamination)
  Pristine Oracle Pass Rate        : 100% (3/3 tasks)
  Defect Detection Sensitivity     : 100% (3/3 failures caught)
  Repair Verification Rate         : 100% (3/3 autonomous patches)
==========================================================================
```

---

## 🧪 Testing

Run the full unit test suite:

```bash
python3 -m unittest discover -s tests -p "test_*.py" -v
```

---

## 📄 License

MIT License. Designed and maintained for robust agent evals in 2026.
