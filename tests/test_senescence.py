import unittest

import pandas as pd

from ivd_audit.senescence import derive_donor_id, paired_senescence_effects


class SenescenceAnalysisTests(unittest.TestCase):
    def test_derive_donor_id_for_paired_titles(self):
        self.assertEqual(derive_donor_id("Disc Tissue 4-347s"), "4-347")
        self.assertEqual(derive_donor_id("Disc Tissue 4-347ts"), "4-347")
        self.assertEqual(derive_donor_id("Disc Tissue 1- 271"), "1-271")

    def test_paired_senescence_effects_use_donor_differences(self):
        expression = pd.DataFrame(
            [[1.0, 3.0, 4.0, 6.0], [5.0, 5.0, 7.0, 7.0]],
            index=["GENE1", "GENE2"],
            columns=["S1_s", "S1_ns", "S2_s", "S2_ns"],
        )
        metadata = pd.DataFrame(
            {
                "sample": ["S1_s", "S1_ns", "S2_s", "S2_ns"],
                "title": [
                    "Disc Tissue 1-100s",
                    "Disc Tissue 1-100ts",
                    "Disc Tissue 2-200s",
                    "Disc Tissue 2-200ts",
                ],
                "status": ["senescent", "non-senescent", "senescent", "non-senescent"],
                "grade": [3.0, 3.0, 4.0, 4.0],
            }
        ).set_index("sample")

        effects, donor_scores = paired_senescence_effects(expression, metadata)

        self.assertAlmostEqual(effects["GENE1"], -2.0)
        self.assertAlmostEqual(effects["GENE2"], 0.0)
        self.assertEqual(list(donor_scores.index), ["1-100", "2-200"])


if __name__ == "__main__":
    unittest.main()
