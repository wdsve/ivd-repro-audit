import unittest

import numpy as np
import pandas as pd

from ivd_audit.audit import (
    cluster_bootstrap_indices,
    cross_half_concordance,
    group_stratified_half,
    permutation_module_directions,
    random_one_per_group,
    weighted_sign_concordance,
)


class DonorSamplingTests(unittest.TestCase):
    def setUp(self):
        self.metadata = pd.DataFrame(
            {
                "donor": ["D1", "D1", "D2", "D2", "D3", "D3", "D4", "D4"],
                "grade": [1, 2, 1, 2, 3, 4, 3, 4],
            }
        )

    def test_random_one_per_group_uses_every_donor_once(self):
        selected = random_one_per_group(
            self.metadata,
            group_column="donor",
            rng=np.random.default_rng(1),
        )

        self.assertEqual(len(selected), 4)
        self.assertEqual(
            set(self.metadata.loc[selected, "donor"]),
            {"D1", "D2", "D3", "D4"},
        )

    def test_group_stratified_half_does_not_split_a_donor(self):
        selected = group_stratified_half(
            self.metadata,
            group_column="donor",
            stratum_column="grade",
            rng=np.random.default_rng(1),
        )
        selected_donors = set(self.metadata.loc[selected, "donor"])

        self.assertEqual(len(selected_donors), 2)
        self.assertTrue(
            self.metadata.loc[self.metadata["donor"].isin(selected_donors)]
            .groupby("donor")
            .size()
            .eq(2)
            .all()
        )

    def test_cluster_bootstrap_resamples_whole_donors(self):
        selected = cluster_bootstrap_indices(
            self.metadata,
            group_column="donor",
            rng=np.random.default_rng(2),
        )
        counts = self.metadata.loc[selected, "donor"].value_counts()

        self.assertEqual(len(selected), 8)
        self.assertTrue(counts.ge(2).all())

    def test_permutation_module_directions_returns_bounded_p_values(self):
        expression = pd.DataFrame(
            np.arange(40, dtype=float).reshape(5, 8),
            index=list("ABCDE"),
            columns=[f"S{i}" for i in range(8)],
        )
        metadata = pd.DataFrame({"grade": [1, 1, 2, 2, 3, 3, 4, 4]})
        gene_sets = {"SET1": {"A", "B"}, "SET2": {"D", "E"}}

        for method in ("label", "stratified", "freedman_lane", "rotation"):
            result = permutation_module_directions(
                expression,
                metadata,
                gene_sets,
                continuous=["grade"],
                categorical=[],
                n_perm=20,
                seed=1,
                method=method,
            )

            self.assertEqual(set(result["module"]), {"SET1", "SET2"})
            self.assertTrue(result["p_two_sided"].between(0, 1).all())

    def test_cross_half_concordance_is_high_for_stable_shared_effects(self):
        grade = np.tile(np.arange(1, 5), 3)
        expression = pd.DataFrame(
            [grade * 0.4, grade * 0.7, grade * 1.1],
            index=["A", "B", "C"],
            columns=[f"S{i}" for i in range(len(grade))],
        )
        metadata = pd.DataFrame({"grade": grade})

        result = cross_half_concordance(
            expression,
            metadata,
            genes={"A", "B", "C"},
            continuous=["grade"],
            categorical=[],
            n_rep=5,
            seed=1,
        )

        self.assertEqual(result["gene_concordance"].median(), 1.0)

    def test_weighted_sign_concordance_prioritises_large_effects(self):
        a = pd.Series({"A": 10.0, "B": -0.01, "C": 0.01})
        b = pd.Series({"A": 10.0, "B": 0.01, "C": -0.01})

        result = weighted_sign_concordance(a, b)

        self.assertAlmostEqual(result["unweighted"], 1 / 3)
        self.assertGreater(result["weighted"], 0.99)


if __name__ == "__main__":
    unittest.main()
