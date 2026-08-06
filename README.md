# cifi — CI Failure Intelligence (v0.1 Alpha)

[![Python Version](https://img.shields.io/badge/python-3.10%2B-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/License-Apache_2.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)
[![Code Style: Ruff](https://img.shields.io/badge/code%20style-ruff-000000.svg)](https://github.com/astral-sh/ruff)

**`cifi`** is a high-performance CLI tool and Python library designed to read raw CI build logs, parse multi-format stack traces, normalize error output, execute a failure rule engine, and export structured JSON optimized for **AI coding agents** and automated developer pipelines.

---

## Key Features

- **Multi-Format Log Parsers**:
  - GitHub Actions workflow annotations (`##[error]`, `##[warning]`)
  - Pytest console tracebacks & failure summary blocks
  - Jest & npm test failure outputs
  - Rust Cargo compiler errors (`error[E0425]`)
  - Generic stack traces & log streams fallback
- **Built-in Failure Rule Engine**:
  - Categorizes failures into `compilation_error`, `missing_dependency`, `assertion_failure`, `timeout`, `permission_denied`, `file_not_found`, and `syntax_error`.
- **Output Normalizer**:
  - Strips ANSI escape sequences and extracts precise file path, line number, column, and function context.
- **AI Agent JSON Exporter**:
  - Generates compact, low-token JSON or markdown prompt bundles tailored for LLM context windows (`cifi parse log.txt --ai-prompt`).
- **Pretty Rich Terminal CLI**:
  - Colorful failure panels, error counts, and context line inspection.

---

## Installation

```bash
pip install -e .
```

---

## Quickstart CLI Usage

### 1. Parse a CI Log File
```bash
cifi parse examples/sample_github_actions.log
```

### 2. Export Normalized JSON for AI Agents
```bash
cifi parse build.log --json -o failure_report.json
```

### 3. Generate LLM-Optimized Prompt Summary
```bash
cifi parse build.log --ai-prompt
```

### 4. Inspect Built-in Failure Rules
```bash
cifi rules
```

---

## Architecture Overview

```
                                ┌───────────────────────────┐
                                │   CI Log File / StdIn     │
                                └─────────────┬─────────────┘
                                              │
                                              ▼
                                ┌───────────────────────────┐
                                │      Log Parser           │
                                │ (GitHub Actions, Pytest,  │
                                │   Cargo, Jest, Generic)   │
                                └─────────────┬─────────────┘
                                              │
                                              ▼
                                ┌───────────────────────────┐
                                │     Rule Engine           │
                                │ (Categorization & Patterns)│
                                └─────────────┬─────────────┘
                                              │
                                              ▼
                                ┌───────────────────────────┐
                                │    Output Normalizer      │
                                │   (CIFailureReport Schema) │
                                └──────┬─────────────┬──────┘
                                       │             │
                        ┌──────────────┘             └──────────────┐
                        ▼                                           ▼
         ┌───────────────────────────┐               ┌───────────────────────────┐
         │     Pretty Rich CLI       │               │       JSON Exporter       │
         │   (Interactive Summary)   │               │   (AI Prompt Optimized)   │
         └───────────────────────────┘               └───────────────────────────┘
```

---

## Python API Usage

```python
from cifi.parser import get_parser
from cifi.rules import RuleEngine
from cifi.exporter import JSONExporter

log_text = "##[error]file=src/main.py,line=42::ModuleNotFoundError: No module named 'requests'"

# 1. Parse log stream
parser = get_parser(log_text)
report = parser.parse(log_text, source_name="gha_build.log")

# 2. Run rule engine
engine = RuleEngine()
report = engine.process_report(report)

# 3. Export JSON
exporter = JSONExporter()
json_output = exporter.export_json(report)
print(json_output)
```

---

## License

Licensed under the [Apache-2.0 License](LICENSE).
