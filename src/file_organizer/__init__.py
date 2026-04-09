"""Public package interface for python-file-organizer."""

from file_organizer.organizer import OrganizeResult, organize_files
from file_organizer.reporting import generate_report, write_report
from file_organizer.rules import RulesError, load_rules

__all__ = [
    "OrganizeResult",
    "RulesError",
    "generate_report",
    "load_rules",
    "organize_files",
    "write_report",
]

__version__ = "0.1.0"
