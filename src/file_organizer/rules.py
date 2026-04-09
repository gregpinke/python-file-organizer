"""Rule loading and validation."""

from __future__ import annotations

import json
from pathlib import Path

from file_organizer.utils import normalize_extension


class RulesError(ValueError):
    """Raised when a rules file is missing or invalid."""


def load_rules(path: str | Path) -> dict[str, str]:
    """Load extension rules from a JSON file."""
    rules_path = Path(path)

    if not rules_path.exists():
        raise RulesError(f"Rules file not found: {rules_path}")
    if not rules_path.is_file():
        raise RulesError(f"Rules path is not a file: {rules_path}")

    try:
        content = json.loads(rules_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise RulesError(f"Invalid JSON in rules file: {rules_path}") from exc
    except OSError as exc:
        raise RulesError(f"Could not read rules file: {rules_path}") from exc

    if not isinstance(content, dict):
        raise RulesError("Rules file must contain a JSON object mapping extensions to categories.")

    normalized: dict[str, str] = {}
    for extension, category in content.items():
        if not isinstance(extension, str) or not isinstance(category, str):
            raise RulesError("All rule keys and values must be strings.")

        normalized_extension = normalize_extension(extension)
        normalized_category = category.strip().lower()

        if not normalized_extension:
            raise RulesError("Rule extensions cannot be empty.")
        if normalized_category in {"", ".", ".."}:
            raise RulesError("Rule categories must be valid non-empty folder names.")

        normalized[normalized_extension] = normalized_category

    return normalized
