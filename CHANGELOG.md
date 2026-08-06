# Changelog

All notable changes to the `cifi` project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.1.0-alpha.1] - 2026-08-06

### Added
- **`LogIntelligencePipeline`**: Unified 5-stage deterministic execution engine (`Log -> Parser -> Normalizer -> Rule Engine -> Actionable Report`).
- **Expanded Rule Catalog (`R007` - `R015`)**:
  - `MemoryExceededRule` (`R007`): Detects OOM / malloc / heap limits.
  - `NetworkConnectionRule` (`R008`): Detects ECONNREFUSED, DNS failures, socket timeouts.
  - `DatabaseMigrationRule` (`R009`): Detects unapplied schema migrations and missing tables.
  - `EnvironmentVariableRule` (`R010`): Detects missing ENV secrets and KeyError configs.
  - `TypeMismatchRule` (`R011`): Detects TypeError and ClassCastException.
  - `LockTimeoutRule` (`R012`): Detects deadlock and file lock acquisition timeouts.
  - `DockerContainerRule` (`R013`): Detects exit code 137, ImagePullBackOff, Dockerfile syntax errors.
  - `DiskSpaceRule` (`R014`): Detects ENOSPC and disk quota exhaustion.
  - `DependencyConflictRule` (`R015`): Detects package constraint conflicts and peer dependency errors.
- **Actionable Remediation Hints**: Every rule trigger attaches non-AI deterministic fix recommendations (`suggested_remediation`).
- **Pipeline Benchmark Profiler**: Tracks microsecond execution duration (`execution_time_ms`) and diagnosis ratio (`diagnosed_count`).

## [0.1.0-alpha] - 2026-08-06

### Added
- **Core Domain Models**: `CIFailureReport`, `DiagnosticItem`, `FailureCategory`, `CodeLocation`, `LogContext`, and `RuleMatchMetadata`.
- **Multi-Format Log Parsers**: `GitHubActionsParser`, `PytestParser`, `JestParser`, `CargoParser`, and `GenericParser`.
- **Rule Engine**: Initial built-in rules `R001` - `R006`.
- **Output Normalizer & Exporters**: `OutputNormalizer` and `JSONExporter`.
- **Pretty Rich CLI**: Initial `cifi parse` and `cifi rules` CLI commands.
