import re
import unittest
from pathlib import Path


class SplContentTests(unittest.TestCase):
    def test_detection_pack_has_documented_queries(self):
        files = list(Path("splunk/detections").glob("*.spl"))
        self.assertGreaterEqual(len(files), 6)
        for path in files:
            query = path.read_text(encoding="utf-8")
            self.assertIn("index=", query, path.name)
            self.assertRegex(query, re.compile(r"\|\s*(stats|tstats|table|eval|where)"), path.name)
            self.assertNotIn("YOUR_INDEX", query, path.name)


if __name__ == "__main__":
    unittest.main()

