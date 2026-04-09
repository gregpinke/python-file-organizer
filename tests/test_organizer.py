from __future__ import annotations

from file_organizer.organizer import organize_files
from file_organizer.utils import generate_safe_destination


def test_unknown_extensions_go_to_others(tmp_path):
    source = tmp_path / "source"
    source.mkdir()
    (source / "archive.xyz").write_text("data", encoding="utf-8")

    result = organize_files(source, rules={".jpg": "images"})

    assert result.moved_files == 1
    assert (source / "others" / "archive.xyz").exists()


def test_generate_safe_destination_appends_counter(tmp_path):
    target_dir = tmp_path / "images"
    target_dir.mkdir()
    (target_dir / "photo.jpg").write_text("existing", encoding="utf-8")
    (target_dir / "photo_1.jpg").write_text("existing", encoding="utf-8")

    destination = generate_safe_destination(target_dir, "photo.jpg")

    assert destination == target_dir / "photo_2.jpg"


def test_dry_run_does_not_move_files(tmp_path):
    source = tmp_path / "source"
    source.mkdir()
    original_file = source / "picture.JPG"
    original_file.write_text("image", encoding="utf-8")

    result = organize_files(source, rules={".jpg": "images"}, dry_run=True)

    assert result.moved_files == 1
    assert original_file.exists()
    assert not (source / "images" / "picture.JPG").exists()


def test_live_mode_moves_files_and_handles_duplicates(tmp_path):
    source = tmp_path / "source"
    source.mkdir()
    (source / "photo.jpg").write_text("incoming", encoding="utf-8")
    images_dir = source / "images"
    images_dir.mkdir()
    (images_dir / "photo.jpg").write_text("existing", encoding="utf-8")

    result = organize_files(source, rules={".jpg": "images"}, recursive=True)

    assert result.moved_files == 1
    assert not (source / "photo.jpg").exists()
    assert (images_dir / "photo.jpg").read_text(encoding="utf-8") == "existing"
    assert (images_dir / "photo_1.jpg").read_text(encoding="utf-8") == "incoming"


def test_recursive_mode_skips_files_already_in_category_folders(tmp_path):
    source = tmp_path / "source"
    source.mkdir()
    images_dir = source / "images"
    images_dir.mkdir()
    (images_dir / "photo.jpg").write_text("existing", encoding="utf-8")
    (source / "notes.txt").write_text("hello", encoding="utf-8")

    result = organize_files(source, rules={".jpg": "images", ".txt": "documents"}, recursive=True)

    assert result.skipped_files == 1
    assert (source / "documents" / "notes.txt").exists()
    assert (images_dir / "photo.jpg").exists()
