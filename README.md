# File Integrity Monitor (FIM)

A lightweight, dependency-free File Integrity Monitoring tool written in
Python. It protects a folder by fingerprinting every file inside it
(SHA-256 hash) and alerting you the moment any file is **added**,
**modified**, or **deleted** — the same core idea behind commercial
tools like Tripwire, OSSEC, and Windows File Integrity Monitoring.

## How it works

1. **`init`** — Recursively hashes every file in a folder you choose and
   saves the result as a trusted "baseline" (`data/baseline.json`).
2. **`check`** — Re-hashes the same folder right now and compares it
   against the baseline, reporting any differences.
3. **`watch`** — Repeats `check` automatically every N seconds so changes
   are caught in near real-time.

Because even a 1-byte change to a file completely changes its SHA-256
hash, this reliably detects tampering, malware dropping files,
unauthorized edits, or accidental deletions.

## Project structure

```
file-integrity-monitor/
├── main.py                # CLI entry point
├── fim/
│   ├── config.py          # Paths & settings
│   ├── hasher.py          # SHA-256 file hashing
│   ├── baseline.py        # Create/save/load the trusted snapshot
│   ├── scanner.py         # Compares current state vs baseline
│   ├── monitor.py         # Continuous "watch" loop
│   └── logger_setup.py    # Logging to console + file
├── tests/
│   └── test_fim.py        # Unit tests
├── data/                  # baseline.json is stored here (auto-created)
├── logs/                  # fim.log is stored here (auto-created)
├── watched_folder/        # Example folder to try the tool on
├── requirements.txt
└── README.md
```

## Requirements

- Python 3.8 or newer
- No external libraries required to run the tool itself (only stdlib)
- `pytest` (optional, only needed to run the test suite)

## Setup (VS Code / any machine)

```bash
# 1. Clone your GitHub repo (after you push this project to it)
git clone https://github.com/<your-username>/file-integrity-monitor.git
cd file-integrity-monitor

# 2. (Recommended) create a virtual environment
python -m venv .venv
source .venv/bin/activate      # on Windows: .venv\Scripts\activate

# 3. Install optional dev dependency (pytest)
pip install -r requirements.txt
```

Open the folder in VS Code (`code .`). It will auto-detect the Python
interpreter; select the `.venv` interpreter if prompted.

## Usage

```bash
# Step 1: Create a baseline of the folder you want to protect
python main.py init ./watched_folder

# Step 2: Make some changes inside watched_folder (edit/add/delete a file)

# Step 3: Run a one-time check
python main.py check

# OR: continuously monitor every 5 seconds (Ctrl+C to stop)
python main.py watch --interval 5
```

### Example output

```
2026-08-24 10:00:01 [WARNING] CHANGES DETECTED!
2026-08-24 10:00:01 [WARNING]   [MODIFIED] /path/watched_folder/notes.txt
2026-08-24 10:00:01 [WARNING]   [ADDED]    /path/watched_folder/new_file.txt
2026-08-24 10:00:01 [WARNING]   [DELETED]  /path/watched_folder/old_file.txt
```

All scan activity is also written to `logs/fim.log` for a permanent
audit trail.

## Running the tests

```bash
python -m pytest tests/ -v
```

## Ideas to extend this project

- Email/Slack/webhook alerts instead of just console + log output
- A simple web dashboard (Flask) to visualize scan history
- Support for watching multiple folders at once
- Use OS-level file system events (e.g. `watchdog` library) instead of
  polling, for instant detection
- Store baseline hash history in SQLite for long-term audit trails
- Add file permission / ownership checks alongside hash checks

## Why this project is a good cybersecurity portfolio piece

File Integrity Monitoring is a real, widely-used defensive security
control (mapped to compliance frameworks like PCI-DSS 11.5 and CIS
Controls). Building one from scratch demonstrates understanding of
cryptographic hashing, the CIA triad (specifically **Integrity**), and
practical detection engineering — while staying simple enough to fully
explain, test, and demo in a short viva or interview.

## License

MIT — free to use, modify, and share.
