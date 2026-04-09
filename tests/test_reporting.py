from __future__ import annotations

from file_organizer.organizer import organize_files
from file_organizer.reporting import generate_report


def test_generate_report_includes_key_summary_fields(tmp_path):
    source = tmp_path / "source"
    source.mkdir()
    (source / "document.txt").write_text("hello", encoding="utf-8")

    result = organize_files(source, rules={".txt": "documents"}, dry_run=True)
    report = generate_report(result, include_actions=True)

    assert "Source folder:" in report
    assert "Output folder:" in report
    assert "Mode: dry-run" in report
    assert "Processed files: 1" in report
    assert "Moved files: 1" in report
    assert "Category summary" in report
    assert "documents: 1" in report
    assert "Action log" in report
