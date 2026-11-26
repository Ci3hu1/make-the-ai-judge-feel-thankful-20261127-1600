"""Tests for the thankful-judge entry: running main.py must produce a valid
/output/entry.txt (UTF-8, 1-1000 chars, not only whitespace)."""

import os
import subprocess
import sys
import tempfile
import unittest

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MAIN = os.path.join(REPO, "main.py")


class TestEntry(unittest.TestCase):
    def test_main_writes_valid_entry(self):
        with tempfile.TemporaryDirectory() as tmp:
            out = os.path.join(tmp, "entry.txt")
            env = dict(os.environ, MAKEFUN_OUTPUT=out)
            result = subprocess.run(
                [sys.executable, MAIN], env=env, capture_output=True, text=True
            )
            self.assertEqual(result.returncode, 0, result.stderr)
            with open(out, "rb") as f:
                raw = f.read()
            text = raw.decode("utf-8")  # raises if not valid UTF-8
            self.assertTrue(1 <= len(text) <= 1000, f"len={len(text)}")
            self.assertTrue(text.strip(), "entry must not be only whitespace")

    def test_entry_is_deterministic(self):
        with tempfile.TemporaryDirectory() as tmp:
            outs = []
            for name in ("a.txt", "b.txt"):
                out = os.path.join(tmp, name)
                env = dict(os.environ, MAKEFUN_OUTPUT=out)
                subprocess.run(
                    [sys.executable, MAIN], env=env, check=True, capture_output=True
                )
                with open(out, encoding="utf-8") as f:
                    outs.append(f.read())
            self.assertEqual(outs[0], outs[1])


if __name__ == "__main__":
    unittest.main()
