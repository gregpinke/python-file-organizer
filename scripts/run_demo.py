"""Small demo helper for the python-file-organizer project."""

from __future__ import annotations

from pathlib import Path

from file_organizer.organizer import organize_files
from file_organizer.reporting import generate_report, write_report
from file_organizer.rules import load_rules


def main() -> int:
    project_root = Path(__file__).resolve().parents[1]
    source_dir = project_root / "examples" / "sample_input"
    rules_path = project_root / "config" / "rules.json"
    report_path = project_root / "examples" / "sample_report.txt"

    rules = load_rules(rules_path)
    result = organize_files(source_dir=source_dir, rules=rules, dry_run=True)
    report_text = generate_report(result, include_actions=True)
    write_report(report_text, report_path)

    print(generate_report(result, include_actions=False))
    print(f"\nDemo report written to: {report_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
