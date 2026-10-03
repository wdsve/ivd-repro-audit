import math
import unittest

import numpy as np
import pandas as pd

from ivd_audit.core import (
    benjamini_hochberg,
    binomial_p_greater,
    binomial_p_less,
    binomial_p_two_sided,
    collapse_by_symbols,
    disattenuate_correlation,
    effective_gene_number,
    empirical_p_greater,
    ols_effects,
    sign_concordance,
    simulate_sign_concordance,
    spearman_correlation,
    spearman_brown,
    summarise_gene_set,
)
from ivd_audit.audit import split_half_reliability, stratified_half


class CoreStatisticsTests(unittest.TestCase):
    def test_binomial_p_greater_uses_exact_upper_tail(self):
        observed = binomial_p_greater(8, 10, 0.5)
        expected = (math.comb(10, 8) + math.comb(10, 9) + math.comb(10, 10)) / 2**10
        self.assertAlmostEqual(observed, expected, places=12)

    def test_binomial_p_less_uses_exact_lower_tail(self):
        observed = binomial_p_less(2, 10, 0.5)
        expected = sum(math.comb(10, k) for k in range(3)) / 2**10
        self.assertAlmostEqual(observed, expected, places=12)

    def test_binomial_p_two_sided_is_capped_at_one(self):
        observed = binomial_p_two_sided(5, 10, 0.5)
        self.assertEqual(observed, 1.0)

    def test_sign_concordance_excludes_zero_effects(self):
        cohort_a = pd.Series({"A": 0.4, "B": -0.8, "C": 0.0, "D": 0.2})
        cohort_b = pd.Series({"A": 0.5, "B": 0.1, "C": -0.3, "D": -0.2})

        result = sign_concordance(cohort_a, cohort_b)

        self.assertEqual(result["n"], 3)
        self.assertEqual(result["n_concordant"], 1)
        self.assertAlmostEqual(result["fraction"], 1 / 3)

    def test_collapse_by_symbols_keeps_highest_mean_probe(self):
        expression = pd.DataFrame(
            [[1.0, 1.0], [3.0, 3.0], [2.0, 2.0]],
            index=["probe_low", "probe_high", "probe_other"],
            columns=["s1", "s2"],
        )
        symbols = pd.Series(
            {"probe_low": "GENE1", "probe_high": "GENE1", "probe_other": "GENE2"}
        )

        collapsed = collapse_by_symbols(expression, symbols)

        self.assertEqual(list(collapsed.index), ["GENE1", "GENE2"])
        np.testing.assert_allclose(collapsed.loc["GENE1"], [3.0, 3.0])

    def test_ols_effects_recovers_linear_coefficient(self):
        expression = pd.DataFrame(
            [[1.0, 3.0, 5.0, 7.0], [5.5, 6.0, 6.5, 7.0]],
            index=["GENE1", "GENE2"],
        )
        design = np.column_stack([np.ones(4), [0.0, 1.0, 2.0, 3.0]])

        effects = ols_effects(expression, design, coefficient=1)

        self.assertAlmostEqual(effects["GENE1"], 2.0)
        self.assertAlmostEqual(effects["GENE2"], 0.5)

    def test_summarise_gene_set_excludes_zero_for_sign_test(self):
        effects = pd.Series({"A": 0.4, "B": 0.2, "C": -0.1, "D": 0.0})

        summary = summarise_gene_set(effects, ["A", "B", "C", "D"])

        self.assertEqual(summary["n_genes"], 3)
        self.assertEqual(summary["n_up"], 2)
        self.assertAlmostEqual(summary["fraction_up"], 2 / 3)
        self.assertTrue(0 <= summary["sign_p_two_sided"] <= 1)

    def test_stratified_half_returns_two_samples_from_each_grade(self):
        metadata = pd.DataFrame({"grade": [1, 1, 2, 2]})

        selected = stratified_half(metadata, "grade", np.random.default_rng(1))

        self.assertEqual(len(selected), 2)
        self.assertEqual(metadata.loc[selected, "grade"].value_counts().to_dict(), {1: 1, 2: 1})

    def test_spearman_correlation_is_rank_based(self):
        a = pd.Series([1.0, 2.0, 3.0, 4.0])
        b = pd.Series([1.0, 4.0, 9.0, 16.0])

        self.assertAlmostEqual(spearman_correlation(a, b), 1.0)
        self.assertAlmostEqual(spearman_correlation(a, -b), -1.0)

    def test_split_half_reliability_supports_small_gene_sets(self):
        rng = np.random.default_rng(2)
        grade = np.tile(np.arange(1, 5), 3)
        expression = pd.DataFrame(
            [grade * slope for slope in (0.2, 0.4, 0.6, 0.8, 1.0)],
            index=[f"G{i}" for i in range(5)],
            columns=[f"S{i}" for i in range(len(grade))],
        )
        metadata = pd.DataFrame({"grade": grade})

        result = split_half_reliability(
            expression,
            metadata,
            continuous=["grade"],
            categorical=[],
            n_rep=5,
            seed=int(rng.integers(1, 10_000)),
        )

        self.assertGreater(result["n_splits"], 0)

    def test_empirical_p_greater_uses_add_one_correction(self):
        null = np.array([0.4, 0.5, 0.6, 0.7])

        self.assertAlmostEqual(empirical_p_greater(0.55, null), 3 / 5)
        self.assertEqual(empirical_p_greater(0.8, null), 1 / 5)

    def test_benjamini_hochberg_preserves_order_and_monotonicity(self):
        p_values = np.array([0.01, 0.04, 0.03, 0.2])

        q_values = benjamini_hochberg(p_values)

        self.assertEqual(len(q_values), 4)
        self.assertAlmostEqual(q_values[0], 0.04)
        self.assertAlmostEqual(q_values[-1], 0.2)
        self.assertTrue(np.all(np.diff(q_values[np.argsort(p_values)]) >= 0))

    def test_effective_gene_number_is_one_for_perfect_correlation(self):
        expression = pd.DataFrame(
            [[1.0, 2.0, 3.0], [2.0, 4.0, 6.0], [3.0, 6.0, 9.0]],
            index=["A", "B", "C"],
        )

        self.assertAlmostEqual(effective_gene_number(expression), 1.0, places=6)

    def test_spearman_brown_and_disattenuation(self):
        full_reliability = spearman_brown(0.4)
        self.assertAlmostEqual(full_reliability, 0.5714285714, places=9)
        self.assertAlmostEqual(
            disattenuate_correlation(0.3, 0.5, 0.5),
            0.6,
            places=9,
        )

    def test_simulated_sign_concordance_is_near_one_for_identical_latent_effects(self):
        simulated = simulate_sign_concordance(
            true_correlation=1.0,
            reliability_a=0.8,
            reliability_b=0.8,
            n_genes=50,
            n_rep=200,
            seed=3,
        )

        self.assertGreater(simulated["mean"], 0.75)
        self.assertLess(simulated["mean"], 1.0)


if __name__ == "__main__":
    unittest.main()
