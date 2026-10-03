import unittest
import gzip
import tempfile
from pathlib import Path

from ivd_audit.data import parse_series_matrix_text, read_series_matrix


class SeriesMatrixParserTests(unittest.TestCase):
    def test_parse_series_matrix_extracts_metadata_and_expression(self):
        text = "\n".join(
            [
                '!Sample_title\t"sample one"\t"sample two"',
                '!Sample_geo_accession\t"GSM1"\t"GSM2"',
                '!Sample_characteristics_ch1\t"grade: I"\t"grade: II"',
                '!Sample_characteristics_ch1\t"method: LCM"\t"method: LCM"',
                "!series_matrix_table_begin",
                '"ID_REF"\t"GSM1"\t"GSM2"',
                '"100_at"\t2.5\t3.5',
                '"200_at"\t4.0\t5.0',
                "!series_matrix_table_end",
            ]
        )

        expression, metadata = parse_series_matrix_text(text)

        self.assertEqual(expression.shape, (2, 2))
        self.assertEqual(list(expression.columns), ["GSM1", "GSM2"])
        self.assertEqual(metadata.loc["GSM1", "grade"], "I")
        self.assertEqual(metadata.loc["GSM2", "method"], "LCM")
        self.assertEqual(metadata.loc["GSM1", "title"], "sample one")

    def test_read_series_matrix_supports_gzip_files(self):
        text = "\n".join(
            [
                '!Sample_geo_accession\t"GSM1"',
                '!Sample_characteristics_ch1\t"grade: I"',
                "!series_matrix_table_begin",
                '"ID_REF"\t"GSM1"',
                '"100_at"\t2.5',
                "!series_matrix_table_end",
            ]
        )
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "matrix.txt.gz"
            with gzip.open(path, "wt", encoding="utf-8") as handle:
                handle.write(text)
            expression, metadata = read_series_matrix(path)

        self.assertEqual(expression.loc["100_at", "GSM1"], 2.5)
        self.assertEqual(metadata.loc["GSM1", "grade"], "I")


if __name__ == "__main__":
    unittest.main()
