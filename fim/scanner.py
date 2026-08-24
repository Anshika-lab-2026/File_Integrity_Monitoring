"""
scanner.py
----------
Core detection logic: takes a current snapshot of a directory and
compares it against the stored baseline to classify every file as
UNCHANGED, MODIFIED, ADDED, or DELETED.
"""

from dataclasses import dataclass, field
from typing import List

from fim.baseline import build_baseline


@dataclass
class ScanResult:
    added: List[str] = field(default_factory=list)
    modified: List[str] = field(default_factory=list)
    deleted: List[str] = field(default_factory=list)
    unchanged_count: int = 0

    @property
    def has_changes(self) -> bool:
        return bool(self.added or self.modified or self.deleted)

    def summary(self) -> str:
        lines = []
        lines.append(f"Unchanged files: {self.unchanged_count}")
        lines.append(f"Added files:     {len(self.added)}")
        lines.append(f"Modified files:  {len(self.modified)}")
        lines.append(f"Deleted files:   {len(self.deleted)}")
        return "\n".join(lines)


def scan_against_baseline(baseline: dict) -> ScanResult:
    """
    Re-hash the directory recorded in `baseline["root"]` and compare
    the fresh hashes against the ones stored in the baseline.

    Args:
        baseline: dict previously produced by build_baseline()/load_baseline()

    Returns:
        ScanResult describing every detected change.
    """
    root = baseline["root"]
    old_files = baseline["files"]

    current_snapshot = build_baseline(root)
    new_files = current_snapshot["files"]

    result = ScanResult()

    old_paths = set(old_files.keys())
    new_paths = set(new_files.keys())

    # Files present now but not in the baseline -> newly added
    result.added = sorted(new_paths - old_paths)

    # Files present in baseline but missing now -> deleted
    result.deleted = sorted(old_paths - new_paths)

    # Files present in both -> check whether the hash changed
    for path in old_paths & new_paths:
        if old_files[path] != new_files[path]:
            result.modified.append(path)
        else:
            result.unchanged_count += 1

    result.modified.sort()
    return result
