"""Plain text report generation helpers."""

from __future__ import annotations

from pathlib import Path

from file_organizer.organizer import OrganizeResult


def generate_report(result: OrganizeResult, *, include_actions: bool = False) -> str:
    """Build a plain-text report from an organization result."""
    mode = "dry-run" if result.dry_run else "live"

    lines = [
        "Python File Organizer Report",
        "============================",
        f"Source folder: {result.source_dir}",
        f"Output folder: {result.output_dir}",
        f"Mode: {mode}",
        f"Recursive scan: {'yes' if result.recursive else 'no'}",
        "",
        "Summary",
        "-------",
        f"Processed files: {result.processed_files}",
        f"Moved files: {result.moved_files}",
        f"Skipped files: {result.skipped_files}",
        f"Errors: {len(result.errors)}",
        "",
        "Category summary",
        "----------------",
    ]

    if result.category_summary:
        for category in sorted(result.category_summary):
            lines.append(f"{category}: {result.category_summary[category]}")
    else:
        lines.append("No categorized files.")

    if result.errors:
        lines.extend(["", "Errors", "------", *result.errors])

    if include_actions and result.actions:
        lines.extend(["", "Action log", "----------"])
        for action in result.actions:
            lines.append(f"[{action.status}] {action.message}")

    return "\n".join(lines)


def write_report(report_text: str, destination: str | Path) -> Path:
    """Write a report to disk and return the report path."""
    report_path = Path(destination)
    report_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.write_text(report_text + "\n", encoding="utf-8")
    return report_path
