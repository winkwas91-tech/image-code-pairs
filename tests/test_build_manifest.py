import csv
import tempfile
import unittest
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from build_manifest import main, rows_from


class ManifestTests(unittest.TestCase):
    def test_samples_detect_complete_and_incomplete(self):
        rows = {row["id"]: row for row in rows_from(ROOT / "samples")}
        self.assertEqual(rows["ring_18"]["status"], "complete")
        self.assertEqual(rows["band_wide"]["status"], "incomplete")
        self.assertTrue(rows["ring_18"]["image"].endswith("ring_18.png"))

    def test_cli_writes_csv(self):
        with tempfile.TemporaryDirectory() as tmp:
            out = Path(tmp) / "manifest.csv"
            code = main([str(ROOT / "samples"), "--out", str(out)])
            self.assertEqual(code, 0)
            with out.open(encoding="utf-8") as handle:
                table = list(csv.DictReader(handle))
            self.assertGreaterEqual(len(table), 2)


if __name__ == "__main__":
    unittest.main()
