"""Command-line interface for python-file-organizer."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from file_organizer.organizer import organize_files
from file_organizer.reporting import generate_report, write_report
from file_organizer.rules import RulesError, load_rules


def build_parser() -> argparse.ArgumentParser:
    """Create the argument parser for the CLI."""
    project_root = Path(__file__).resolve().parents[2]
    default_rules = project_root / "config" / "rules.json"

    parser = argparse.ArgumentParser(description="Organize files into category folders by extension.")
    parser.add_argument("--source", required=True, help="Source directory to scan.")
    parser.add_argument("--output", help="Output directory. Defaults to organizing in place.")
    parser.add_argument("--rules", default=str(default_rules), help="Path to a JSON rules file.")
    parser.add_argument("--dry-run", action="store_true", help="Simulate actions without moving files.")
    parser.add_argument("--report", help="Optional path for a plain text report.")
    parser.add_argument("--recursive", action="store_true", help="Scan subdirectories recursively.")
    parser.add_argument("--verbose", action="store_true", help="Print per-file actions.")
    return parser


def main(argv: list[str] | None = None) -> int:
    """Run the CLI and return a process exit code."""
    parser = build_parser()
    args = parser.parse_args(argv)

    try:
        rules = load_rules(args.rules)
        result = organize_files(
            source_dir=args.source,
            output_dir=args.output,
            rules=rules,
            dry_run=args.dry_run,
            recursive=args.recursive,
        )
    except (RulesError, FileNotFoundError, NotADirectoryError) as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 2

    report_text = generate_report(result, include_actions=args.verbose)

    print(_build_terminal_summary(result))
    if args.verbose:
        for action in result.actions:
            print(f"[{action.status}] {action.message}")

    if args.report:
        report_path = write_report(report_text, args.report)
        print(f"Report written to: {report_path}")

    return 1 if result.errors else 0


def _build_terminal_summary(result) -> str:
    mode = "DRY-RUN" if result.dry_run else "LIVE"
    return (
        f"{mode} summary | processed: {result.processed_files} | moved: {result.moved_files} | "
        f"skipped: {result.skipped_files} | errors: {len(result.errors)}"
    )


if __name__ == "__main__":
    raise SystemExit(main())
