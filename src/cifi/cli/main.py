import sys
import click
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

from cifi import __version__
from cifi.parser import PARSER_REGISTRY
from cifi.rules import RuleEngine
from cifi.pipeline import LogIntelligencePipeline
from cifi.exporter import JSONExporter

console = Console()


@click.group()
@click.version_option(version=__version__, prog_name="cifi")
def cli():
    """cifi — Failure Intelligence Engine.

    Pure deterministic 5-stage pipeline for diagnosing 80%+ of CI failures without AI.
    Log -> Language/Framework Detect -> Parser -> Normalizer -> Rule Engine (Fingerprints & Explainability) -> Report
    """
    pass


@cli.command(name="parse")
@click.argument("logfile", type=click.Path(exists=True, dir_okay=False), required=False)
@click.option("--json", "output_json", is_flag=True, help="Output normalized report in JSON format.")
@click.option("--ai-prompt", is_flag=True, help="Output compact LLM-optimized failure summary.")
@click.option("--output", "-o", type=click.Path(dir_okay=False), help="Save output to specified file path.")
@click.option("--parser", "parser_name", type=click.Choice(list(PARSER_REGISTRY.keys())), help="Force specific log parser engine.")
@click.option("--verbose", "-v", is_flag=True, help="Display extended stack context lines.")
def parse_cmd(logfile, output_json, ai_prompt, output, parser_name, verbose):
    """Parse a CI log file or stdin stream and generate diagnostic report."""
    if logfile:
        with open(logfile, "r", encoding="utf-8", errors="replace") as f:
            content = f.read()
        source_name = logfile
    elif not sys.stdin.isatty():
        content = sys.stdin.read()
        source_name = "stdin"
    else:
        console.print("[bold red]Error:[/bold red] Please provide a log file path or pipe log content via stdin.")
        sys.exit(1)

    # Execute Log Intelligence Pipeline
    pipeline = LogIntelligencePipeline()
    report = pipeline.run(content, source_name=source_name, parser_type=parser_name)

    exporter = JSONExporter()

    # Output Modes
    if output_json:
        result_text = exporter.export_json(report, pretty=True)
    elif ai_prompt:
        result_text = exporter.export_ai_prompt_format(report)
    else:
        # Pretty Rich Render
        _render_pretty_report(report, verbose=verbose)
        result_text = None

    if result_text:
        if output:
            with open(output, "w", encoding="utf-8") as f:
                f.write(result_text)
            console.print(f"[bold green]Saved output to {output}[/bold green]")
        else:
            click.echo(result_text)


@cli.command(name="rules")
def list_rules_cmd():
    """List all built-in deterministic failure classification rules."""
    engine = RuleEngine()
    table = Table(title="cifi Deterministic Failure Rules (80% Non-AI Coverage)", show_header=True, header_style="bold magenta")
    table.add_column("Rule ID", style="cyan", width=8)
    table.add_column("Name", style="bold yellow", width=26)
    table.add_column("Category", style="green", width=22)
    table.add_column("Deterministic Fix Remediation", style="white")

    for rule in engine.rules:
        remediation = getattr(rule, "remediation", rule.description)
        table.add_row(rule.rule_id, rule.name, rule.category.value, remediation)

    console.print(table)


def _render_pretty_report(report, verbose: bool = False):
    """Render interactive color terminal summary using Rich."""
    header = Panel(
        f"[bold white]Log Source:[/bold white] [cyan]{report.log_source}[/cyan] | "
        f"[bold white]Ecosystem:[/bold white] [bold yellow]{report.detected_language.value.upper()}[/bold yellow] ([cyan]{report.detected_framework.value.upper()}[/cyan]) | "
        f"[bold white]Benchmark:[/bold white] {report.execution_time_ms} ms | "
        f"[bold red]Failures:[/bold red] {report.failure_count}",
        title="[bold magenta]cifi — Failure Intelligence Engine Report (No-AI Engine)[/bold magenta]",
        border_style="magenta",
    )
    console.print(header)

    if not report.diagnostics:
        console.print("[bold green]✓ No CI failures or errors detected![/bold green]")
        return

    for idx, diag in enumerate(report.diagnostics, 1):
        color = "red" if diag.severity == "error" else "yellow"
        title = f"[{color}][{diag.severity.upper()}] #{idx}: {diag.summary}[/{color}]"

        loc_str = "Unknown"
        if diag.location:
            loc_str = f"{diag.location.file_path or 'unknown'}"
            if diag.location.line_number:
                loc_str += f":{diag.location.line_number}"
            if diag.location.function_name:
                loc_str += f" in {diag.location.function_name}()"

        rule_str = "None"
        if diag.rule_match:
            rule_str = f"{diag.rule_match.rule_id} ({diag.rule_match.rule_name})"

        fp_str = diag.fingerprint or "GENERIC-001"
        conf_str = diag.confidence_level.value
        exp_reason = diag.explainability.reason if diag.explainability else "Matched signature pattern."
        remediation_str = diag.suggested_remediation or "Inspect error trace logs below."

        body_lines = [
            f"[bold]Fingerprint:[/bold] [bold cyan]{fp_str}[/bold cyan]",
            f"[bold]Category:[/bold] [green]{diag.category.value}[/green]",
            f"[bold]Confidence:[/bold] [bold bright_green]{conf_str}[/bold bright_green]",
            f"[bold]Rule Match:[/bold] [cyan]{rule_str}[/cyan]",
            f"[bold]Location:[/bold] [yellow]{loc_str}[/yellow]",
            f"[bold]Why? (Reason):[/bold] {exp_reason}",
            f"[bold]Actionable Fix:[/bold] [bold bright_green]{remediation_str}[/bold bright_green]",
            "",
            "[bold]Raw Failure Trace:[/bold]",
            f"  {diag.message}",
        ]

        if verbose and diag.context and diag.context.raw_lines:
            body_lines.append("")
            body_lines.append("[bold]Log Context Window:[/bold]")
            for ctx_line in diag.context.raw_lines:
                body_lines.append(f"  │ {ctx_line}")

        panel = Panel("\n".join(body_lines), title=title, border_style=color)
        console.print(panel)


if __name__ == "__main__":
    cli()
