from __future__ import annotations

import json

import pytest

from file_organizer.rules import RulesError, load_rules


def test_load_rules_normalizes_extensions_and_categories(tmp_path):
    rules_path = tmp_path / "rules.json"
    rules_path.write_text(json.dumps({"JPG": "Images", ".PDF": "DOCUMENTS"}), encoding="utf-8")

    rules = load_rules(rules_path)

    assert rules == {".jpg": "images", ".pdf": "documents"}


def test_load_rules_raises_for_missing_file(tmp_path):
    missing_path = tmp_path / "missing.json"

    with pytest.raises(RulesError, match="Rules file not found"):
        load_rules(missing_path)


def test_load_rules_raises_for_invalid_structure(tmp_path):
    rules_path = tmp_path / "rules.json"
    rules_path.write_text(json.dumps([".jpg", "images"]), encoding="utf-8")

    with pytest.raises(RulesError, match="JSON object"):
        load_rules(rules_path)
