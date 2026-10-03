import tempfile
import unittest
from pathlib import Path

from ivd_audit.data import read_gmt


class GmtReaderTests(unittest.TestCase):
    def test_read_gmt_returns_gene_sets_without_description(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "sets.gmt"
            path.write_text("SET_A\tdesc\t1\t2\t3\nSET_B\tdesc\t3\t4\n", encoding="utf-8")

            gene_sets = read_gmt(path)

        self.assertEqual(gene_sets["SET_A"], {"1", "2", "3"})
        self.assertEqual(gene_sets["SET_B"], {"3", "4"})


if __name__ == "__main__":
    unittest.main()
