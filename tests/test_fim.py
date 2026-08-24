"""
test_fim.py
-----------
Basic unit tests for the FIM project. Run with:
    python -m pytest tests/
or simply:
    python tests/test_fim.py
"""

import os
import sys
import shutil
import tempfile
import unittest

# Allow importing the fim package when running this file directly
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from fim.hasher import hash_file
from fim.baseline import build_baseline
from fim.scanner import scan_against_baseline


class TestHasher(unittest.TestCase):
    def setUp(self):
        self.tmpdir = tempfile.mkdtemp()
        self.filepath = os.path.join(self.tmpdir, "sample.txt")
        with open(self.filepath, "w") as f:
            f.write("hello world")

    def tearDown(self):
        shutil.rmtree(self.tmpdir)

    def test_hash_is_deterministic(self):
        h1 = hash_file(self.filepath)
        h2 = hash_file(self.filepath)
        self.assertEqual(h1, h2)

    def test_hash_changes_when_content_changes(self):
        h1 = hash_file(self.filepath)
        with open(self.filepath, "a") as f:
            f.write(" - modified")
        h2 = hash_file(self.filepath)
        self.assertNotEqual(h1, h2)


class TestScanner(unittest.TestCase):
    def setUp(self):
        self.tmpdir = tempfile.mkdtemp()
        self.file_a = os.path.join(self.tmpdir, "a.txt")
        self.file_b = os.path.join(self.tmpdir, "b.txt")
        with open(self.file_a, "w") as f:
            f.write("content A")
        with open(self.file_b, "w") as f:
            f.write("content B")

        self.baseline = build_baseline(self.tmpdir)

    def tearDown(self):
        shutil.rmtree(self.tmpdir)

    def test_no_changes_detected_when_untouched(self):
        result = scan_against_baseline(self.baseline)
        self.assertFalse(result.has_changes)
        self.assertEqual(result.unchanged_count, 2)

    def test_modified_file_is_detected(self):
        with open(self.file_a, "a") as f:
            f.write(" extra text")
        result = scan_against_baseline(self.baseline)
        self.assertIn(self.file_a, result.modified)
        self.assertTrue(result.has_changes)

    def test_added_file_is_detected(self):
        new_file = os.path.join(self.tmpdir, "c.txt")
        with open(new_file, "w") as f:
            f.write("new content")
        result = scan_against_baseline(self.baseline)
        self.assertIn(new_file, result.added)

    def test_deleted_file_is_detected(self):
        os.remove(self.file_b)
        result = scan_against_baseline(self.baseline)
        self.assertIn(self.file_b, result.deleted)


if __name__ == "__main__":
    unittest.main()
