"""
monitor.py
----------
Implements continuous ("watch") mode: repeatedly re-scans the
watched directory at a fixed interval and raises alerts the moment
a change is detected, until the user stops the program (Ctrl+C).
"""

import time

from fim.baseline import load_baseline
from fim.scanner import scan_against_baseline
from fim.logger_setup import get_logger

logger = get_logger()


def log_scan_result(result) -> None:
    if not result.has_changes:
        logger.info("Scan complete - no changes detected. (%d files OK)", result.unchanged_count)
        return

    logger.warning("CHANGES DETECTED!")
    for path in result.added:
        logger.warning("  [ADDED]    %s", path)
    for path in result.modified:
        logger.warning("  [MODIFIED] %s", path)
    for path in result.deleted:
        logger.warning("  [DELETED]  %s", path)


def run_watch(interval: int) -> None:
    """
    Continuously scan the directory recorded in the baseline every
    `interval` seconds, logging/alerting on any detected change.
    """
    baseline = load_baseline()
    logger.info("Starting continuous monitoring of: %s", baseline["root"])
    logger.info("Polling every %d seconds. Press Ctrl+C to stop.", interval)

    try:
        while True:
            result = scan_against_baseline(baseline)
            log_scan_result(result)
            time.sleep(interval)
    except KeyboardInterrupt:
        logger.info("Monitoring stopped by user.")
