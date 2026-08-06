import json
from typing import Dict, Any
from cifi.models import CIFailureReport
from cifi.exporter.normalizer import OutputNormalizer


class JSONExporter:
    """Serializes CIFailureReport models to JSON format and AI prompt formats."""

    def __init__(self, normalizer: OutputNormalizer = None):
        self.normalizer = normalizer or OutputNormalizer()

    def to_dict(self, report: CIFailureReport) -> Dict[str, Any]:
        """Convert report to dictionary representation after normalization."""
        normalized_report = self.normalizer.normalize(report)
        return json.loads(normalized_report.model_dump_json())

    def export_json(self, report: CIFailureReport, pretty: bool = True) -> str:
        """Export report as JSON string."""
        data = self.to_dict(report)
        indent = 2 if pretty else None
        return json.dumps(data, indent=indent, default=str)

    def export_file(self, report: CIFailureReport, file_path: str, pretty: bool = True) -> None:
        """Save report to a JSON file."""
        json_str = self.export_json(report, pretty=pretty)
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(json_str)

    def export_ai_prompt_format(self, report: CIFailureReport) -> str:
        """Generate a dense, LLM-optimized summary representation of the failure report."""
        data = self.to_dict(report)
        failures = [d for d in data.get("diagnostics", []) if d.get("severity") == "error"]

        output = [
            f"=== CI FAILURE DIAGNOSTIC REPORT (Log Intelligence Engine) ===",
            f"Log Source: {data.get('log_source')}",
            f"Ecosystem: {data.get('detected_language')} ({data.get('detected_framework')})",
            f"Execution Time: {data.get('execution_time_ms')} ms",
            f"Total Failures: {len(failures)}",
            "",
        ]

        for idx, f in enumerate(failures, 1):
            rule_info = f.get("rule_match", {})
            loc = f.get("location", {})
            exp = f.get("explainability", {})
            remediation = f.get("suggested_remediation")
            fp = f.get("fingerprint")
            conf = f.get("confidence_score", 0.9)
            conf_str = "HIGH" if conf >= 0.85 else ("MEDIUM" if conf >= 0.60 else "LOW")

            output.append(f"[{idx}] {f.get('summary')}")
            if fp:
                output.append(f"    Fingerprint: {fp}")
            output.append(f"    Category: {f.get('category')}")
            output.append(f"    Confidence: {conf_str}")
            if rule_info:
                output.append(f"    Rule: {rule_info.get('rule_id')} ({rule_info.get('rule_name')})")
            if loc and loc.get("file_path"):
                output.append(f"    Location: {loc.get('file_path')}:{loc.get('line_number') or 1}")
            if exp and exp.get("reason"):
                output.append(f"    Why?: {exp.get('reason')}")
            if remediation:
                output.append(f"    Actionable Fix: {remediation}")
            output.append(f"    Snippet: {f.get('message')}")
            output.append("")

        return "\n".join(output)
