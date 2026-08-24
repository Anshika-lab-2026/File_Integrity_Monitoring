#!/usr/bin/env python3
"""
main.py
-------
Command-line interface for the File Integrity Monitor (FIM).

Usage:
    python main.py init  <folder>          Create a trusted baseline of a folder
    python main.py check                   Run one comparison scan against the baseline
    python main.py watch [--interval N]    Continuously monitor (default every 5s)

Example workflow:
    python main.py init ./watched_folder
    python main.py check
    python main.py watch --interval 10
"""

import argparse
import sys

from fim.baseline import build_baseline, save_baseline, load_baseline
from fim.scanner import scan_against_baseline
from fim.monitor import run_watch, log_scan_result
from fim.logger_setup import get_logger
from fim.config import DEFAULT_WATCH_INTERVAL

logger = get_logger()


def cmd_init(args):
    logger.info("Building baseline for: %s", args.folder)
    baseline = build_baseline(args.folder)
    save_baseline(baseline)
    logger.info("Baseline saved with %d files tracked.", len(baseline["files"]))


def cmd_check(args):
    try:
        baseline = load_baseline()
    except FileNotFoundError as e:
        logger.error(str(e))
        sys.exit(1)

    result = scan_against_baseline(baseline)
    log_scan_result(result)
    print("\n--- Summary ---")
    print(result.summary())

    # Exit code 1 if changes were found -- useful for CI/CD or cron scripting
    sys.exit(1 if result.has_changes else 0)


def cmd_watch(args):
    try:
        run_watch(interval=args.interval)
    except FileNotFoundError as e:
        logger.error(str(e))
        sys.exit(1)


def build_parser():
    parser = argparse.ArgumentParser(
        description="File Integrity Monitor (FIM) - detect unauthorized file changes."
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    p_init = subparsers.add_parser("init", help="Create a trusted baseline for a folder")
    p_init.add_argument("folder", help="Path to the folder to protect")
    p_init.set_defaults(func=cmd_init)

    p_check = subparsers.add_parser("check", help="Run a single scan against the baseline")
    p_check.set_defaults(func=cmd_check)

    p_watch = subparsers.add_parser("watch", help="Continuously monitor for changes")
    p_watch.add_argument(
        "--interval", type=int, default=DEFAULT_WATCH_INTERVAL,
        help=f"Seconds between scans (default: {DEFAULT_WATCH_INTERVAL})"
    )
    p_watch.set_defaults(func=cmd_watch)

    return parser


def main():
    parser = build_parser()
    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
