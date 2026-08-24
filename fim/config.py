"""
config.py
---------
Central configuration for the File Integrity Monitor (FIM).
Keeping all constants in one place makes the project easy to
customize without touching the core logic.
"""

import os

# Root directory of the project (folder containing this file's parent)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Where the "baseline" (the trusted snapshot of hashes) is stored
DATA_DIR = os.path.join(BASE_DIR, "data")
BASELINE_FILE = os.path.join(DATA_DIR, "baseline.json")

# Where logs / alert history are stored
LOGS_DIR = os.path.join(BASE_DIR, "logs")
LOG_FILE = os.path.join(LOGS_DIR, "fim.log")

# Hashing algorithm used to fingerprint files.
# SHA-256 is collision-resistant and fast enough for this use case.
HASH_ALGORITHM = "sha256"

# Chunk size (bytes) used while reading files for hashing.
# Reading in chunks avoids loading huge files entirely into memory.
CHUNK_SIZE = 65536  # 64 KB

# Files/folders to ignore while scanning (e.g. OS/system junk files)
IGNORE_NAMES = {".DS_Store", "Thumbs.db", "__pycache__", ".git"}

# Default folder that will be monitored if the user doesn't specify one
DEFAULT_WATCH_DIR = os.path.join(BASE_DIR, "watched_folder")

# Default polling interval (seconds) for continuous "watch" mode
DEFAULT_WATCH_INTERVAL = 5

# Ensure required directories exist as soon as config is imported
os.makedirs(DATA_DIR, exist_ok=True)
os.makedirs(LOGS_DIR, exist_ok=True)
os.makedirs(DEFAULT_WATCH_DIR, exist_ok=True)
