"""
baseline.py
-----------
The "baseline" is the trusted snapshot: a JSON file that maps every
watched file's path -> its hash, taken at a moment we trust the
system was clean. All future scans are compared against this snapshot.
"""

import json
import os
from datetime import datetime, timezone

from fim.config import BASELINE_FILE, IGNORE_NAMES
from fim.hasher import hash_file


def _iter_files(directory: str):
    """Yield every file path under `directory`, skipping ignored names."""
    for root, dirs, files in os.walk(directory):
        # Skip ignored directories in-place so os.walk doesn't descend into them
        dirs[:] = [d for d in dirs if d not in IGNORE_NAMES]
        for name in files:
            if name in IGNORE_NAMES:
                continue
            yield os.path.join(root, name)


def build_baseline(directory: str) -> dict:
    """
    Walk `directory` recursively and hash every file inside it.

    Returns:
        dict with structure:
        {
            "created_at": "<ISO timestamp>",
            "root": "<absolute path scanned>",
            "files": { "<filepath>": "<hash>", ... }
        }
    """
    directory = os.path.abspath(directory)
    file_hashes = {}
    for filepath in _iter_files(directory):
        try:
            file_hashes[filepath] = hash_file(filepath)
        except OSError:
            # File may have been deleted/locked while scanning -- skip it
            continue

    return {
        "created_at": datetime.now(timezone.utc).isoformat(),
        "root": directory,
        "files": file_hashes,
    }


def save_baseline(baseline: dict, path: str = BASELINE_FILE) -> None:
    """Persist the baseline dict to disk as pretty-printed JSON."""
    with open(path, "w", encoding="utf-8") as f:
        json.dump(baseline, f, indent=2)


def load_baseline(path: str = BASELINE_FILE) -> dict:
    """
    Load a previously saved baseline from disk.

    Raises:
        FileNotFoundError if no baseline has been created yet.
    """
    if not os.path.exists(path):
        raise FileNotFoundError(
            f"No baseline found at '{path}'. Run 'python main.py init <folder>' first."
        )
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)
