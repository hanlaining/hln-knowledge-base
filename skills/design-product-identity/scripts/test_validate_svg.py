#!/usr/bin/env python3

from __future__ import annotations

import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest


SCRIPT = Path(__file__).resolve().parent / "validate_svg.py"


class SvgValidationTest(unittest.TestCase):
    def run_validation(self, content: str, expected: int) -> dict[str, object]:
        with tempfile.TemporaryDirectory() as temporary:
            svg = Path(temporary) / "logo.svg"
            svg.write_text(content, encoding="utf-8")
            result = subprocess.run([sys.executable, str(SCRIPT), str(svg)], capture_output=True, text=True, check=False)
            self.assertEqual(result.returncode, expected, result.stdout + result.stderr)
            return json.loads(result.stdout)

    def test_clean_vector(self) -> None:
        result = self.run_validation('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 32 32" width="32" height="32"><path d="M0 0h32v32H0z"/></svg>', 0)
        self.assertTrue(result["ok"])

    def test_rejects_script_and_raster(self) -> None:
        result = self.run_validation('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 32 32"><script>alert(1)</script><image href="https://example.com/a.png"/></svg>', 1)
        self.assertFalse(result["ok"])
        self.assertTrue(any("script" in item for item in result["errors"]))
        self.assertTrue(any("raster" in item for item in result["errors"]))


if __name__ == "__main__":
    unittest.main()
