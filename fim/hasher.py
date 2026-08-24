"""
hasher.py
---------
Responsible for turning a file's contents into a fixed-length
"fingerprint" (hash). If even a single byte of the file changes,
the resulting hash changes completely -- this is what lets us
detect tampering.
"""

import hashlib
from fim.config import HASH_ALGORITHM, CHUNK_SIZE


def hash_file(filepath: str) -> str:
    """
    Compute the hash of a single file's contents.

    Args:
        filepath: Absolute or relative path to the file.

    Returns:
        A hex-string digest (e.g. "3f786850e387550f...") representing
        the file's contents at the moment it was read.

    Raises:
        OSError if the file cannot be read (permissions, deleted mid-scan, etc).
    """
    hasher = hashlib.new(HASH_ALGORITHM)
    with open(filepath, "rb") as f:
        while True:
            chunk = f.read(CHUNK_SIZE)
            if not chunk:
                break
            hasher.update(chunk)
    return hasher.hexdigest()
