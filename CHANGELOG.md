# Changelog

All notable changes to the `cifi` project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.1.0-alpha] - 2026-08-06

### Added
- **Core Domain Models**: `CIFailureReport`, `DiagnosticItem`, `FailureCategory`, `CodeLocation`, `LogContext`, and `RuleMatchMetadata`.
- **Multi-Format Log Parsers**:
  - `GitHubActionsParser`: Parses `##[error]` and `##[warning]` annotation logs.
  - `PytestParser`: Parses Pytest console failure blocks and traceback file locations.
  - `JestParser`: Parses Jest/npm test suite failures and stack frames.
  - `CargoParser`: Parses Rust compiler error codes (`E\d+`) and file span indicators.
  - `GenericParser`: Fallback parser using regex heuristics for common error signatures.
- **Rule Engine**: Built-in rules for `compilation_error`, `missing_dependency`, `assertion_failure`, `timeout`, `permission_denied`, and `file_not_found`.
- **Output Normalizer & Exporters**:
  - `OutputNormalizer`: Strips ANSI color escape codes and cleans trace text.
  - `JSONExporter`: Export reports to formatted JSON files or compact LLM prompt context bundles.
- **Pretty Rich CLI**:
  - Interactive terminal summary tables and failure panels (`cifi parse`).
  - Rule catalog command (`cifi rules`).
- **Test Suite**: Comprehensive unit and integration test suite using `pytest`.
