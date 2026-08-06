# cifi — Log Intelligence Engine (v0.1.0-alpha.1)

[![Python Version](https://img.shields.io/badge/python-3.10%2B-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/License-Apache_2.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)
[![Engine Mode: Zero-AI](https://img.shields.io/badge/engine-100%25%20Deterministic%20(No--AI)-brightgreen.svg)](https://github.com/aryanp160/cifi)

**`cifi`** is a high-performance **Log Intelligence Engine** engineered to diagnose **80%+ of common CI build failures deterministically WITHOUT AI**.

$$\text{Log} \longrightarrow \text{Parser} \longrightarrow \text{Normalizer} \longrightarrow \text{Rule Engine} \longrightarrow \text{Actionable Remediation Report}$$

---

## 🎯 Why No-AI Engine?

When CI build pipelines fail, sending raw 50,000-line logs to LLM APIs is expensive, slow, and unreliable. `cifi` executes a deterministic 5-stage pipeline locally in milliseconds, delivering:

1. **Zero LLM Cost & Microsecond Benchmarks**: Diagnoses failures locally in <5ms.
2. **80%+ Common Failure Diagnosis**: Identifies root causes with 15 deterministic classification rules (`R001` - `R015`).
3. **Actionable Remediation Hints**: Provides exact non-AI fix instructions (e.g. precise `pip`/`npm` command, ENV variable check, DB migration command).
4. **Structured JSON & Token-Dense AI Prompts**: Generates clean JSON schema or compact prompt blocks if downstream LLMs are used.

---

## ⚙️ 5-Stage Pipeline Architecture

```
┌─────────────────────────────────────────────────────────────────────────────────────────────┐
│                                   LogIntelligencePipeline                                   │
│                                                                                             │
│  ┌──────────────┐     ┌──────────────┐     ┌──────────────┐     ┌──────────────┐            │
│  │  Raw Log     │ ──▶ │  Log Parser  │ ──▶ │  Normalizer  │ ──▶ │ Rule Engine  │ ──┐        │
│  └──────────────┘     └──────────────┘     └──────────────┘     └──────────────┘   │        │
│                                                                                    │        │
│  ┌──────────────┐     ┌────────────────────────────────────────────────────────┐   │        │
│  │ Final Report │ ◄── │ Actionable Remediation Hints (80% No-AI Diagnosis)     │ ◄─┘        │
│  └──────────────┘     └────────────────────────────────────────────────────────┘            │
└─────────────────────────────────────────────────────────────────────────────────────────────┘
```

---

## 📜 Deterministic Rule Catalog (80% Non-AI Coverage)

| Rule ID | Rule Name | Category | Actionable Remediation Hint |
| :--- | :--- | :--- | :--- |
| **`R001`** | Compilation or Syntax Error | `compilation_error` | Check syntax at reported file location and verify imports/types. |
| **`R002`** | Missing Dependency | `missing_dependency` | Install missing package or add to pyproject.toml / package.json / Cargo.toml. |
| **`R003`** | Test Assertion Failure | `assertion_failure` | Inspect test assertion expectations vs actual return values. |
| **`R004`** | Execution Timeout | `timeout` | Increase job timeout in CI config or optimize slow blocking operations. |
| **`R005`** | Permission or Authentication Denied | `permission_denied` | Verify file read/write permissions or update secret access tokens. |
| **`R006`** | File Not Found | `file_not_found` | Verify path exists or add build step to generate required file. |
| **`R007`** | Memory Exceeded / OOM | `memory_exceeded` | Increase memory limits on CI worker runner or optimize memory allocations. |
| **`R008`** | Network Connection Failure | `network_error` | Verify network connectivity, proxy settings, or remote host availability. |
| **`R009`** | Database Schema / Migration Issue | `database_migration` | Run database migration scripts (e.g. alembic upgrade head / prisma db push). |
| **`R010`** | Missing Environment Variable | `environment_variable` | Set missing environment variable in CI secrets / .env configuration. |
| **`R011`** | Type Mismatch Error | `type_mismatch` | Check type annotations, function signature parameters, and type conversions. |
| **`R012`** | Lock or Resource Deadlock | `lock_timeout` | Clear stale lock files or ensure concurrent jobs release locks. |
| **`R013`** | Docker Container Failure | `docker_error` | Check Dockerfile build syntax, container memory limits (exit 137), or image credentials. |
| **`R014`** | Disk Space Exhausted | `disk_space` | Clean temporary build artifacts or expand disk storage allocation on CI runner. |
| **`R015`** | Dependency Version Conflict | `dependency_conflict` | Resolve package version pin constraints in lockfile or lock compatible versions. |

---

## Quickstart Usage

```bash
# 1. Inspect built-in deterministic rules & remediation table
cifi rules

# 2. Run Log Intelligence Engine on a CI log
cifi parse examples/sample_github_actions.log

# 3. Export JSON report with execution benchmark time
cifi parse build.log --json

# 4. Generate LLM prompt context with actionable fix hints
cifi parse build.log --ai-prompt
```

---

## Python API Usage

```python
from cifi.pipeline import LogIntelligencePipeline

raw_log = "##[error]file=src/auth.py,line=42::ModuleNotFoundError: No module named 'pyjwt'"

# Execute 5-stage Log Intelligence Engine
pipeline = LogIntelligencePipeline()
report = pipeline.run(raw_log, source_name="ci_workflow.log")

print(f"Benchmark: {report.execution_time_ms} ms")
for diag in report.diagnostics:
    print(f"Rule: {diag.rule_match.rule_id} ({diag.rule_match.rule_name})")
    print(f"Fix:  {diag.suggested_remediation}")
```

---

## License

Licensed under the [Apache-2.0 License](LICENSE).
