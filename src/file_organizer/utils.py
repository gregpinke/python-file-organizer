"""Small utility helpers for file organization."""

from __future__ import annotations

from pathlib import Path


def normalize_extension(extension: str) -> str:
    """Normalize an extension to lowercase dotted form."""
    cleaned = extension.strip().lower()
    if not cleaned:
        return ""
    if not cleaned.startswith("."):
        cleaned = f".{cleaned}"
    return cleaned


def make_relative_display(path: Path, base: Path) -> str:
    """Return a readable relative path when possible."""
    try:
        return str(path.relative_to(base))
    except ValueError:
        return str(path)


def generate_safe_destination(destination_dir: Path, filename: str) -> Path:
    """Create a non-conflicting destination path inside a directory."""
    candidate = destination_dir / filename
    if not candidate.exists():
        return candidate

    stem = candidate.stem
    suffix = candidate.suffix
    counter = 1

    while True:
        renamed = destination_dir / f"{stem}_{counter}{suffix}"
        if not renamed.exists():
            return renamed
        counter += 1
