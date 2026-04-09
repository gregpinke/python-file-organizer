"""Core file organization logic."""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from shutil import move

from file_organizer.utils import generate_safe_destination, make_relative_display, normalize_extension


@dataclass(slots=True)
class FileAction:
    """Represents the result of handling a single file."""

    source: Path
    destination: Path
    category: str
    status: str
    message: str


@dataclass(slots=True)
class OrganizeResult:
    """Structured organization result suitable for reporting."""

    source_dir: Path
    output_dir: Path
    dry_run: bool
    recursive: bool
    processed_files: int = 0
    moved_files: int = 0
    skipped_files: int = 0
    errors: list[str] = field(default_factory=list)
    category_summary: dict[str, int] = field(default_factory=dict)
    actions: list[FileAction] = field(default_factory=list)


def organize_files(
    source_dir: str | Path,
    rules: dict[str, str],
    output_dir: str | Path | None = None,
    *,
    dry_run: bool = False,
    recursive: bool = False,
) -> OrganizeResult:
    """Organize files from source into category folders."""
    source_path = Path(source_dir).expanduser().resolve()
    destination_root = Path(output_dir).expanduser().resolve() if output_dir else source_path

    if not source_path.exists():
        raise FileNotFoundError(f"Source directory not found: {source_path}")
    if not source_path.is_dir():
        raise NotADirectoryError(f"Source path is not a directory: {source_path}")

    if output_dir is not None and destination_root.exists() and not destination_root.is_dir():
        raise NotADirectoryError(f"Output path is not a directory: {destination_root}")

    files = list(_scan_files(source_path, recursive=recursive))
    result = OrganizeResult(
        source_dir=source_path,
        output_dir=destination_root,
        dry_run=dry_run,
        recursive=recursive,
    )

    category_names = set(rules.values()) | {"others"}

    for file_path in files:
        if _should_skip_file(file_path, source_path, destination_root, category_names, recursive):
            result.skipped_files += 1
            result.actions.append(
                FileAction(
                    source=file_path,
                    destination=file_path,
                    category="skipped",
                    status="skipped",
                    message="Skipped file already inside a category folder.",
                )
            )
            continue

        result.processed_files += 1
        category = _resolve_category(file_path, rules)
        target_dir = destination_root / category
        destination = generate_safe_destination(target_dir, file_path.name)

        action = FileAction(
            source=file_path,
            destination=destination,
            category=category,
            status="planned" if dry_run else "moved",
            message=(
                f"Would move {make_relative_display(file_path, source_path)} -> "
                f"{make_relative_display(destination, destination_root)}"
                if dry_run
                else f"Moved {make_relative_display(file_path, source_path)} -> "
                f"{make_relative_display(destination, destination_root)}"
            ),
        )

        try:
            if not dry_run:
                target_dir.mkdir(parents=True, exist_ok=True)
                move(str(file_path), str(destination))
                result.moved_files += 1
            else:
                result.moved_files += 1
        except OSError as exc:
            action.status = "error"
            action.message = f"Failed to move {file_path.name}: {exc}"
            result.errors.append(action.message)
        else:
            result.category_summary[category] = result.category_summary.get(category, 0) + 1

        result.actions.append(action)

    return result


def _scan_files(source_dir: Path, *, recursive: bool) -> list[Path]:
    if recursive:
        return sorted(path for path in source_dir.rglob("*") if path.is_file())
    return sorted(path for path in source_dir.iterdir() if path.is_file())


def _resolve_category(file_path: Path, rules: dict[str, str]) -> str:
    extension = normalize_extension(file_path.suffix)
    return rules.get(extension, "others")


def _should_skip_file(
    file_path: Path,
    source_dir: Path,
    output_dir: Path,
    category_names: set[str],
    recursive: bool,
) -> bool:
    if not recursive:
        return False

    try:
        relative_to_output = file_path.relative_to(output_dir)
    except ValueError:
        return False

    parts = relative_to_output.parts
    if not parts:
        return False

    if parts[0] not in category_names:
        return False

    if output_dir != source_dir:
        return True

    return len(parts) >= 2
