"""Generate the manuscript, supplement and Chinese abstract from result tables."""

from __future__ import annotations

import json
from pathlib import Path

import pandas as pd


def _pct(value: float) -> str:
    return f"{100 * float(value):.1f}%"


def _p(value: float) -> str:
    value = float(value)
    exponent = int(f"{value:e}".split("e")[-1])
    if exponent <= -4:
        mantissa, _ = f"{value:e}".split("e")
        return f"{float(mantissa):.2f} x 10^{exponent}"
    return f"{value:.4f}"


def _markdown_table(frame: pd.DataFrame) -> str:
    columns = list(frame.columns)
    lines = [
        "| " + " | ".join(columns) + " |",
        "|" + "|".join(["---"] * len(columns)) + "|",
    ]
    for row in frame.itertuples(index=False, name=None):
        lines.append("| " + " | ".join(str(value) for value in row) + " |")
    return "\n".join(lines)


def write_manuscript(project_dir: str | Path) -> None:
    project = Path(project_dir)
    results = project / "results"
    manuscript_dir = project / "manuscript"
    manuscript_dir.mkdir(parents=True, exist_ok=True)

    summary = json.loads((results / "audit_summary.json").read_text(encoding="utf-8"))
    primary = pd.read_csv(results / "primary_comparison_summary.csv")
    diagnostics = pd.read_csv(results / "cohort_effect_diagnostics.csv")
    reliability = pd.read_csv(results / "internal_split_half_reliability.csv")
    msigdb = pd.read_csv(results / "msigdb_module_audit.csv")
    pairwise = pd.read_csv(results / "tissue_pairwise_concordance.csv")
    pairwise_exact = pd.read_csv(
        results / "tissue_pairwise_concordance_exact.csv"
    )
    pairwise_compartment = pd.read_csv(
        results / "tissue_pairwise_concordance_compartment_matched.csv"
    )
    curated = pd.read_csv(results / "curated_module_audit.csv")
    donor_summary = pd.read_csv(results / "donor_sensitivity_summary.csv")
    donor_split = pd.read_csv(results / "donor_stratified_split_half.csv")
    effective_genes = pd.read_csv(results / "effective_gene_number.csv")
    expression_matched = pd.read_csv(
        results / "primary_expression_matched_null.csv"
    ).iloc[0]
    attenuation = pd.read_csv(results / "attenuation_simulation.csv")
    cross_half = pd.read_csv(results / "positive_control_cross_half_summary.csv")
    power_calibration = pd.read_csv(results / "power_calibration.csv")
    weighted_primary = pd.read_csv(results / "primary_weighted_concordance.csv").iloc[0]
    module_score_slopes = pd.read_csv(results / "primary_module_score_slopes.csv")
    probe_sensitivity = pd.read_csv(results / "probe_collapse_sensitivity.csv")
    probe_summary = json.loads(
        (results / "probe_collapse_sensitivity_summary.json").read_text(
            encoding="utf-8"
        )
    )
    gene_identity = json.loads(
        (results / "gene_identity_sensitivity_summary.json").read_text(
            encoding="utf-8"
        )
    )
    scale_sensitivity = json.loads(
        (results / "scale_invariance_sensitivity_summary.json").read_text(
            encoding="utf-8"
        )
    )
    family_sensitivity = json.loads(
        (results / "module_family_sensitivity_summary.json").read_text(
            encoding="utf-8"
        )
    )
    gse176205_summary = json.loads(
        (results / "GSE176205_NP_validation/GSE176205_summary.json").read_text(
            encoding="utf-8"
        )
    )
    gse176205_modules = pd.read_csv(
        results / "GSE176205_NP_validation/GSE176205_NP_direction.csv"
    )
    gse17077_summary = json.loads(
        (results / "GSE17077_senescence/GSE17077_summary.json").read_text(
            encoding="utf-8"
        )
    )
    gse17077_modules = pd.read_csv(
        results / "GSE17077_senescence/GSE17077_module_direction.csv"
    )
    literature_summary = json.loads(
        (
            results / "literature_audit/europepmc_scoping_summary.json"
        ).read_text(encoding="utf-8")
    )
    third_cohort_registry = pd.read_csv(
        results / "third_cohort_search/candidate_registry.csv"
    )
    blood_124272 = pd.read_csv(
        project.parent
        / "ldh_pipeline/data/processed/external_blood/GSE124272_metadata.csv"
    )
    blood_150408 = pd.read_csv(
        project.parent
        / "ldh_pipeline/data/processed/external_blood/GSE150408_metadata_all.csv"
    )
    blood_150408_untreated = pd.read_csv(
        project.parent
        / "ldh_pipeline/data/processed/external_blood/"
        "GSE150408_untreated_metadata.csv"
    )
    permutation_methods = ("stratified", "freedman_lane", "rotation")
    permutation_rows = []
    for method in permutation_methods:
        p_70362 = pd.read_csv(
            results / f"module_direction_permutation_{method}_GSE70362.csv"
        )
        p_23130 = pd.read_csv(
            results / f"module_direction_permutation_{method}_GSE23130.csv"
        )
        permutation_rows.append(
            {
                "Method": method,
                "GSE70362 p": float(
                    p_70362.loc[
                        p_70362["module"].eq("ECM remodelling"),
                        "p_two_sided",
                    ].iloc[0]
                ),
                "GSE23130 p": float(
                    p_23130.loc[
                        p_23130["module"].eq("ECM remodelling"),
                        "p_two_sided",
                    ].iloc[0]
                ),
            }
        )
    permutation_method_table = pd.DataFrame(permutation_rows)
    permutation_method_table["GSE70362 p"] = permutation_method_table[
        "GSE70362 p"
    ].map(_p)
    permutation_method_table["GSE23130 p"] = permutation_method_table[
        "GSE23130 p"
    ].map(_p)

    legacy = primary[primary["comparison"].str.startswith("all available")].iloc[0]
    strict = primary[primary["comparison"].str.startswith("grade I-IV")].iloc[0]
    strict_only = primary[
        primary["comparison"].str.contains("grade only")
    ].iloc[0]
    reliability_key = reliability.assign(
        key=reliability["cohort"] + "|" + reliability["gene_space"]
    ).set_index("key")
    rel_70362 = float(reliability_key.loc["GSE70362_AF_I_IV|ECM", "median_spearman"])
    rel_23130 = float(reliability_key.loc["GSE23130_LCM_all|ECM", "median_spearman"])

    top_pair = pairwise.sort_values("gene_concordance", ascending=False).iloc[0]
    low_pair = pairwise.sort_values("gene_concordance").iloc[0]
    replicated = msigdb[msigdb["gene_level_replicated"]].sort_values(
        ["gene_concordance", "n_genes"],
        ascending=False,
    )

    diagnostic_table = diagnostics.copy()
    diagnostic_table["cohort"] = diagnostic_table["cohort"].map(
        {
            "GSE70362_AF_all": "GSE70362 AF, all grades",
            "GSE70362_AF_I_IV": "GSE70362 AF, grade I-IV",
            "GSE23130_all": "GSE23130, all processing",
            "GSE23130_LCM_all": "GSE23130 LCM, grade I-IV",
            "GSE70362_AF_I_IV_grade_only": "GSE70362 AF, grade I-IV, grade only",
            "GSE23130_LCM_grade_only": "GSE23130 LCM, grade I-IV, grade only",
        }
    )
    diagnostic_table["n_donors"] = diagnostic_table["n_donors"].map(
        lambda value: "NA" if pd.isna(value) else str(int(value))
    )
    diagnostic_table["n_samples"] = diagnostic_table["n_samples"].astype(int)
    diagnostic_table["n_genes"] = diagnostic_table["n_genes"].astype(int)
    diagnostic_table["fraction_up"] = diagnostic_table["fraction_up"].map(_pct)
    diagnostic_table["median_effect"] = diagnostic_table["median_effect"].map(
        lambda value: f"{float(value):+.4f}"
    )
    diagnostic_table = diagnostic_table.rename(
        columns={
            "cohort": "Analysis set",
            "n_samples": "Samples",
            "n_donors": "Donors",
            "n_genes": "Genes",
            "fraction_up": "Up",
            "median_effect": "Median effect",
            "global_shift": "Global shift",
        }
    )

    primary_table = pd.DataFrame(
        [
            {
                "Comparison": "All available AF/LCM samples",
                "GSE70362 ECM up": _pct(legacy["gse70362_ecm_fraction_up"]),
                "GSE23130 ECM up": _pct(legacy["gse23130_ecm_fraction_up"]),
                "ECM gene concordance": _pct(legacy["ecm_sign_concordance"]),
                "Two-sided sign p": _p(
                    legacy["ecm_sign_concordance_p_two_sided"]
                ),
            },
            {
                "Comparison": "Strict grade I-IV AF/LCM, adjusted",
                "GSE70362 ECM up": _pct(strict["gse70362_ecm_fraction_up"]),
                "GSE23130 ECM up": _pct(strict["gse23130_ecm_fraction_up"]),
                "ECM gene concordance": _pct(strict["ecm_sign_concordance"]),
                "Two-sided sign p": _p(
                    strict["ecm_sign_concordance_p_two_sided"]
                ),
            },
            {
                "Comparison": "Strict grade I-IV AF/LCM, grade only",
                "GSE70362 ECM up": _pct(strict_only["gse70362_ecm_fraction_up"]),
                "GSE23130 ECM up": _pct(strict_only["gse23130_ecm_fraction_up"]),
                "ECM gene concordance": _pct(strict_only["ecm_sign_concordance"]),
                "Two-sided sign p": _p(
                    strict_only["ecm_sign_concordance_p_two_sided"]
                ),
            },
        ]
    )

    funnel_table = pd.DataFrame(
        [
            ("Modules tested", summary["msigdb"]["n_modules_tested"]),
            (
                "Significant in one cohort only",
                summary["msigdb"]["n_significant_one_sided"],
            ),
            (
                "Significant in both cohorts",
                summary["msigdb"]["n_significant_both"],
            ),
            (
                "Significant in opposite directions",
                summary["msigdb"]["n_discordant_significant"],
            ),
            (
                "Nominal module and gene-level gate",
                summary["msigdb"]["n_gene_level_replicated"],
            ),
            (
                "Passed exact-sign FDR gate",
                summary["msigdb"]["n_replicated_fdr"],
            ),
        ],
        columns=["Stage", "Modules"],
    )

    donor_table = donor_summary.copy()
    donor_table["mode"] = donor_table["mode"].map(
        {
            "one_sample_per_donor": "One sample per donor",
            "cluster_bootstrap": "Donor cluster bootstrap",
        }
    )
    for column in (
        "fraction_up_median",
        "fraction_up_lower",
        "fraction_up_upper",
        "concordance_median",
        "concordance_lower",
        "concordance_upper",
    ):
        donor_table[column] = donor_table[column].map(_pct)
    donor_table["effect_rho_median"] = donor_table["effect_rho_median"].map(
        lambda value: f"{float(value):.3f}"
    )
    donor_table = donor_table[
        [
            "mode",
            "n_replicates",
            "fraction_up_median",
            "fraction_up_lower",
            "fraction_up_upper",
            "concordance_median",
            "concordance_lower",
            "concordance_upper",
            "effect_rho_median",
        ]
    ].rename(
        columns={
            "mode": "Sensitivity model",
            "n_replicates": "Replicates",
            "fraction_up_median": "Fraction up",
            "fraction_up_lower": "Up 2.5%",
            "fraction_up_upper": "Up 97.5%",
            "concordance_median": "Concordance",
            "concordance_lower": "Conc 2.5%",
            "concordance_upper": "Conc 97.5%",
            "effect_rho_median": "Effect rho",
        }
    )

    attenuation_table = attenuation.copy()
    attenuation_table["true_correlation"] = attenuation_table[
        "true_correlation"
    ].map(lambda value: f"{float(value):.1f}")
    for column in ("mean", "lower_2_5", "upper_97_5"):
        attenuation_table[column] = attenuation_table[column].map(_pct)
    attenuation_table = attenuation_table[
        ["true_correlation", "mean", "lower_2_5", "upper_97_5"]
    ].rename(
        columns={
            "true_correlation": "Latent correlation",
            "mean": "Expected concordance",
            "lower_2_5": "2.5%",
            "upper_97_5": "97.5%",
        }
    )

    cross_half_table = cross_half.copy()
    for column in ("concordance_median", "concordance_lower", "concordance_upper"):
        cross_half_table[column] = cross_half_table[column].map(_pct)
    cross_half_table["effect_rho_median"] = cross_half_table[
        "effect_rho_median"
    ].map(lambda value: f"{float(value):.3f}")
    cross_half_table = cross_half_table.rename(
        columns={
            "cohort": "Cohort",
            "n_replicates": "Replicates",
            "concordance_median": "Concordance",
            "concordance_lower": "2.5%",
            "concordance_upper": "97.5%",
            "effect_rho_median": "Effect rho",
        }
    )

    power_table = power_calibration.copy()
    power_table["true_correlation"] = power_table["true_correlation"].map(
        lambda value: f"{float(value):.1f}"
    )
    power_table["mean_concordance"] = power_table["mean_concordance"].map(_pct)
    power_table["power_nominal_n"] = power_table["power_nominal_n"].map(_pct)
    power_table["power_effective_n"] = power_table["power_effective_n"].map(_pct)
    power_table = power_table.rename(
        columns={
            "true_correlation": "Latent correlation",
            "mean_concordance": "Mean concordance",
            "power_nominal_n": "Power, nominal n",
            "power_effective_n": "Power, effective n",
            "effective_n_genes": "Effective genes",
        }
    )

    module_score_table = module_score_slopes.copy()
    module_score_table["slope"] = module_score_table["slope"].map(
        lambda value: f"{float(value):+.4f}"
    )
    module_score_table = module_score_table.rename(
        columns={
            "cohort": "Cohort",
            "n_genes": "Genes",
            "slope": "Score slope",
        }
    )

    weighted_table = pd.DataFrame(
        [
            {
                "Metric": "Unweighted sign concordance",
                "Value": _pct(weighted_primary["unweighted"]),
            },
            {
                "Metric": "Effect-size weighted concordance",
                "Value": _pct(weighted_primary["weighted"]),
            },
            {
                "Metric": "Top-half effect concordance",
                "Value": _pct(weighted_primary["top_half"]),
            },
            {
                "Metric": "Effect-size Spearman rho",
                "Value": f"{float(weighted_primary['effect_rho']):.3f}",
            },
        ]
    )

    top_replicated = replicated.head(10)[
        ["module", "n_genes", "cohort_a_fraction_up", "cohort_b_fraction_up", "gene_concordance"]
    ].copy()
    for column in (
        "cohort_a_fraction_up",
        "cohort_b_fraction_up",
        "gene_concordance",
    ):
        top_replicated[column] = top_replicated[column].map(_pct)
    top_replicated = top_replicated.rename(
        columns={
            "module": "Module",
            "n_genes": "Genes",
            "cohort_a_fraction_up": "GSE70362 up",
            "cohort_b_fraction_up": "GSE23130 up",
            "gene_concordance": "Concordance",
        }
    )

    pairwise_display = pairwise.sort_values("gene_concordance", ascending=False).copy()
    pairwise_display["Pair"] = (
        pairwise_display["cohort_a"] + " vs " + pairwise_display["cohort_b"]
    )
    pairwise_display["Genes"] = pairwise_display["n_genes"]
    pairwise_display["Concordance"] = pairwise_display["gene_concordance"].map(_pct)
    pairwise_display["Exact p"] = pairwise_display["gene_concordance_p"].map(_p)
    pairwise_display = pairwise_display[["Pair", "Genes", "Concordance", "Exact p"]]

    def _pairwise_view(frame: pd.DataFrame) -> pd.DataFrame:
        output = frame.sort_values("gene_concordance", ascending=False).copy()
        output["Pair"] = output["cohort_a"] + " vs " + output["cohort_b"]
        output["Concordance"] = output["gene_concordance"].map(_pct)
        return output[["Pair", "n_genes", "Concordance"]].rename(
            columns={"n_genes": "Genes"}
        )

    pairwise_exact_display = _pairwise_view(pairwise_exact)
    pairwise_compartment_display = _pairwise_view(pairwise_compartment)

    third_cohort_summary = (
        third_cohort_registry.groupby("tier", as_index=False)
        .size()
        .rename(columns={"tier": "Tier", "size": "Datasets"})
        .sort_values("Tier")
    )

    literature_table = pd.DataFrame(
        [
            ("Open-access articles in scoping corpus", literature_summary["n_articles"]),
            ("Articles using more than one GSE", literature_summary["n_multi_cohort"]),
            (
                "Articles with consistency language",
                literature_summary["n_consistency_language"],
            ),
            (
                "Multi-cohort articles with consistency language",
                literature_summary["n_multi_cohort_with_consistency_language"],
            ),
            (
                "Articles describing gene-level concordance",
                literature_summary["n_gene_level_concordance_language"],
            ),
            ("Articles mentioning permutation", literature_summary["n_permutation"]),
            ("Articles mentioning FDR", literature_summary["n_fdr"]),
            ("Articles mentioning power", literature_summary["n_power"]),
        ],
        columns=["Scoping metric", "Articles"],
    )

    gse176205_display = gse176205_modules[
        [
            "module",
            "n_genes",
            "gse176205_centered_fraction_up",
            "gse176205_centered_median_effect",
            "gse70362_np_fraction_up",
            "gse70362_np_median_effect",
            "gene_concordance",
            "effect_rho",
        ]
    ].copy()
    for column in (
        "gse176205_centered_fraction_up",
        "gse70362_np_fraction_up",
        "gene_concordance",
    ):
        gse176205_display[column] = gse176205_display[column].map(_pct)
    for column in (
        "gse176205_centered_median_effect",
        "gse70362_np_median_effect",
        "effect_rho",
    ):
        gse176205_display[column] = gse176205_display[column].map(
            lambda value: f"{float(value):+.3f}"
        )
    gse176205_display = gse176205_display.rename(
        columns={
            "module": "Module",
            "n_genes": "Genes",
            "gse176205_centered_fraction_up": "GSE176205 up",
            "gse176205_centered_median_effect": "GSE176205 median",
            "gse70362_np_fraction_up": "GSE70362 NP up",
            "gse70362_np_median_effect": "GSE70362 median",
            "gene_concordance": "Concordance",
            "effect_rho": "Effect rho",
        }
    )

    gse17077_display = gse17077_modules.copy()
    gse17077_display["fraction_up"] = gse17077_display["fraction_up"].map(_pct)
    gse17077_display["median_effect"] = gse17077_display["median_effect"].map(
        lambda value: f"{float(value):+.3f}"
    )
    gse17077_display = gse17077_display.rename(
        columns={
            "module": "Module",
            "n_genes": "Genes",
            "fraction_up": "Senescent up",
            "median_effect": "Median effect",
            "sign_p_greater": "One-sided p",
        }
    )[["Module", "Genes", "Senescent up", "Median effect", "One-sided p"]]

    blood_table = pd.DataFrame(
        [
            {
                "Cohort": "GSE124272",
                "Design": "8 LDH vs 8 healthy",
                "Samples": len(blood_124272),
            },
            {
                "Cohort": "GSE150408",
                "Design": "42 IDD vs 17 healthy; 25 treatment",
                "Samples": len(blood_150408),
            },
            {
                "Cohort": "GSE150408 untreated",
                "Design": "17 untreated IDD vs 17 healthy",
                "Samples": len(blood_150408_untreated),
            },
        ]
    )

    def _probe_row(mode: str, label: str) -> dict[str, str]:
        row = probe_sensitivity[probe_sensitivity["mode"].eq(mode)].iloc[0]
        return {
            "Collapse rule": label,
            "GSE70362 ECM up": _pct(row["gse70362_fraction_up"]),
            "GSE23130 ECM up": _pct(row["gse23130_fraction_up"]),
            "ECM concordance": _pct(row["ecm_concordance"]),
            "Two-sided sign p": _p(row["ecm_concordance_p_two_sided"]),
        }

    probe_table = pd.DataFrame(
        [
            _probe_row("highest_mean", "Highest-mean probe (primary)"),
            _probe_row("first_probe", "First probe"),
            _probe_row("median_probe", "Median probe"),
            {
                "Collapse rule": "Random probe, median (2.5-97.5%)",
                "GSE70362 ECM up": _pct(
                    probe_summary["random_gse70362_fraction_up_median"]
                ),
                "GSE23130 ECM up": (
                    f"{_pct(probe_summary['random_gse23130_fraction_up_median'])} "
                    f"({_pct(probe_summary['random_gse23130_fraction_up_lower'])}-"
                    f"{_pct(probe_summary['random_gse23130_fraction_up_upper'])})"
                ),
                "ECM concordance": (
                    f"{_pct(probe_summary['random_ecm_concordance_median'])} "
                    f"({_pct(probe_summary['random_ecm_concordance_lower'])}-"
                    f"{_pct(probe_summary['random_ecm_concordance_upper'])})"
                ),
                "Two-sided sign p": (
                    f"{_p(probe_summary['random_ecm_concordance_p_two_sided_median'])} "
                    "(median)"
                ),
            },
        ]
    )

    gene_identity_table = pd.DataFrame(
        [
            {
                "Metric": "Platform gene symbols",
                "Primary mapping": gene_identity["platform_symbols"],
                "Alias-aware mapping": gene_identity["platform_symbols"],
            },
            {
                "Metric": "Current canonical symbols",
                "Primary mapping": gene_identity["canonical_symbols"],
                "Alias-aware mapping": gene_identity["canonical_symbols"],
            },
            {
                "Metric": "Alias-only symbols recovered",
                "Primary mapping": 0,
                "Alias-aware mapping": gene_identity["alias_only_symbols"],
            },
            {
                "Metric": "Unresolved symbols",
                "Primary mapping": gene_identity["unresolved_symbols"],
                "Alias-aware mapping": gene_identity["unresolved_symbols"],
            },
            {
                "Metric": "Ambiguous alias keys removed",
                "Primary mapping": gene_identity["ambiguous_alias_keys_removed"],
                "Alias-aware mapping": gene_identity["ambiguous_alias_keys_removed"],
            },
            {
                "Metric": "Modules tested",
                "Primary mapping": gene_identity["current_modules_tested"],
                "Alias-aware mapping": gene_identity["alias_modules_tested"],
            },
            {
                "Metric": "Significant in one cohort",
                "Primary mapping": gene_identity["current_significant_one_cohort"],
                "Alias-aware mapping": gene_identity["alias_significant_one_cohort"],
            },
            {
                "Metric": "Significant in both cohorts",
                "Primary mapping": gene_identity["current_significant_both"],
                "Alias-aware mapping": gene_identity["alias_significant_both"],
            },
            {
                "Metric": "Nominal gene-level results",
                "Primary mapping": gene_identity["current_nominal_gene_level"],
                "Alias-aware mapping": gene_identity["alias_nominal_gene_level"],
            },
            {
                "Metric": "Strict FDR results",
                "Primary mapping": gene_identity["current_replicated_fdr"],
                "Alias-aware mapping": gene_identity["alias_replicated_fdr"],
            },
        ]
    )

    scale_table = pd.DataFrame(
        [
            {
                "Analysis": "Adjusted OLS (primary)",
                "GSE70362 ECM up": _pct(strict["gse70362_ecm_fraction_up"]),
                "GSE23130 ECM up": _pct(strict["gse23130_ecm_fraction_up"]),
                "ECM concordance": _pct(strict["ecm_sign_concordance"]),
                "Two-sided sign p": _p(
                    strict["ecm_sign_concordance_p_two_sided"]
                ),
            },
            {
                "Analysis": "Unadjusted Spearman trend",
                "GSE70362 ECM up": _pct(
                    scale_sensitivity["unadjusted_spearman"][
                        "gse70362_fraction_up"
                    ]
                ),
                "GSE23130 ECM up": _pct(
                    scale_sensitivity["unadjusted_spearman"][
                        "gse23130_fraction_up"
                    ]
                ),
                "ECM concordance": _pct(
                    scale_sensitivity["unadjusted_spearman"]["ecm_concordance"]
                ),
                "Two-sided sign p": _p(
                    scale_sensitivity["unadjusted_spearman"][
                        "ecm_concordance_p_two_sided"
                    ]
                ),
            },
            {
                "Analysis": "Batch/source-stratified Spearman trend",
                "GSE70362 ECM up": _pct(
                    scale_sensitivity["stratum_adjusted_spearman"][
                        "gse70362_fraction_up"
                    ]
                ),
                "GSE23130 ECM up": _pct(
                    scale_sensitivity["stratum_adjusted_spearman"][
                        "gse23130_fraction_up"
                    ]
                ),
                "ECM concordance": _pct(
                    scale_sensitivity["stratum_adjusted_spearman"][
                        "ecm_concordance"
                    ]
                ),
                "Two-sided sign p": _p(
                    scale_sensitivity["stratum_adjusted_spearman"][
                        "ecm_concordance_p_two_sided"
                    ]
                ),
            },
        ]
    )

    family_table = pd.DataFrame(
        [
            {
                "Mapping": row["mapping"],
                "Collection": row["collection"],
                "Modules": row["modules"],
                "Nominal gene-level": row["nominal_gene_level"],
                "Collection-local FDR": row["local_fdr"],
            }
            for row in family_sensitivity["families"]
        ]
    )

    manuscript = f"""# Module-level agreement is not replication: a reporting and reproducibility gate for public human intervertebral disc transcriptomes

## Abstract

**Background.** Public transcriptome reanalyses in intervertebral disc (IVD)
research frequently interpret a pathway or module that is significant in one
cohort, or directionally concordant across cohorts, as evidence of
reproducibility. This interpretation ignores the possibility that the module
direction is driven by a different gene subset in each cohort.

**Methods.** We audited six public human IVD tissue transcriptome cohorts and
used the two largest graded annulus fibrosus cohorts, GSE70362 and GSE23130,
for a matched analysis. We compared all available samples with a strict
sample set restricted to Thompson grade I-IV, annulus fibrosus, and
laser-capture microdissection. Effects were estimated with linear models
adjusted for available technical variables. For every gene set we reported
the module direction in each cohort, exact and permutation p-values, and
gene-level sign concordance between cohorts. We additionally audited 1,554
Hallmark, KEGG and Reactome modules and 15 tissue cohort pairs. Internal
reproducibility was measured by repeated stratified split-half analyses;
for GSE70362, where donor identifiers were available, donor-level
one-sample and cluster-bootstrap analyses were used to assess within-donor
dependence; GSE23130 donor identifiers were unavailable. Global-shift,
processing-confound, multiple-testing and reliability-attenuation checks
were performed before interpretation.

**Results.** In the strict comparison, the ECM remodelling module increased in
{_pct(strict["gse23130_ecm_fraction_up"])} of measured genes in GSE23130
(sign-test p = {_p(strict["gse23130_ecm_sign_p"])}) but in only
{_pct(strict["gse70362_ecm_fraction_up"])} of genes in GSE70362
(p = {_p(strict["gse70362_ecm_sign_p"])}). Gene-level sign concordance was
{_pct(strict["ecm_sign_concordance"])} (two-sided exact sign p =
{_p(strict["ecm_sign_concordance_p_two_sided"])}), below the 50% expected
under independent directions. This below-chance level was specific to the
primary highest-mean-probe rule; alternative probe collapsing did not exceed
50% but was less extreme (random-probe median 36.7%). Donor-level resampling preserved a
median GSE70362 ECM fraction up near 50% and a median cross-cohort
concordance of approximately 30%. The ECM module showed moderate internal
reliability in both cohorts (split-half Spearman rho
{rel_70362:.2f} and {rel_23130:.2f}). Cross-half positive controls reached
median concordance values of 63.3% and 64.5%, above the cross-cohort value of
23.3%. Power calibration nevertheless showed that the nominal 30-gene test had
only 20.4% power at a latent correlation of 0.6. The result is a failure to
establish replication, not proof that shared biology is absent. Across 1,554
curated modules,
{summary["msigdb"]["n_significant_one_sided"]} were significant in only one
cohort and {summary["msigdb"]["n_significant_both"]} in both;
{summary["msigdb"]["n_gene_level_replicated"]} passed the additional gene-level
concordance gate at nominal p-values, but
{summary["msigdb"]["n_replicated_fdr"]} survived the exact sign-test FDR gate.
An alias-aware gene-identity sensitivity did not change the strict result.
Phenotype permutation and expression-matched nulls were retained as
sensitivity analyses. Across 15 IVD tissue cohort pairs, the median gene-level sign
concordance was {_pct(summary["pairwise_tissue"]["median_gene_concordance"])}
and the highest was {_pct(summary["pairwise_tissue"]["max_gene_concordance"])}.
No Tier A third AF severity cohort was identified despite targeted searching.
In a scoping corpus of {literature_summary["n_articles"]} open-access IVD
transcriptome articles, {literature_summary["n_multi_cohort"]} used more than
one GSE and {literature_summary["n_multi_cohort_with_consistency_language"]}
combined multi-cohort use with consistency language, whereas no article
described gene-level concordance using the prespecified text criteria.

**Conclusions.** In public human IVD transcriptomes, module-level significance
does not establish cross-cohort replication. A reproducible claim should
require the same prespecified gene set to move in the same direction in an
independent cohort at the gene level, not only at the module level. We
operationalise this distinction as a five-level claim ladder, from exploratory
single-cohort signals to FDR-controlled gene-level replication.

**Keywords.** intervertebral disc degeneration; transcriptomics;
reproducibility; cross-cohort validation; gene-set analysis; public data

## Significance statement

Public-data transcriptome studies often have too few independent cohorts for
biological replication, yet multi-cohort studies commonly use consistency
language. This audit shows that a module can be strongly significant,
internally reproducible, and still fail gene-level cross-cohort concordance.
The practical recommendation is simple: report module direction and
gene-level sign concordance together, and treat either layer alone as
hypothesis-generating.

## Introduction

Intervertebral disc degeneration is studied with many small human
transcriptome cohorts that differ in tissue compartment, RNA processing,
platform, degeneration scale, and clinical endpoint. In a scoping corpus of
{literature_summary["n_articles"]} open-access IVD transcriptome articles,
{literature_summary["n_multi_cohort"]} used more than one GSE and
{literature_summary["n_multi_cohort_with_consistency_language"]} combined
multi-cohort use with consistency language. None described gene-level
concordance using the prespecified text criteria. Reanalyses therefore may use
public cohorts to support a module by citing a significant enrichment in one
dataset and a directionally similar result in another without showing that the
same genes replicate. Comparable cross-omic and prognostic-signature audits
have shown that nominal gene-set recurrence and apparently good discrimination
can coexist with limited gene-level overlap or performance indistinguishable
from suitable null models [1,2]. These concerns align with long-standing
analyses of research validity [3] and systematic replication projects, where
most replication effect sizes were smaller than the original estimates [4].
The Open Science Collaboration similarly found replication effects about half
the magnitude of original effects [5].

That argument has a blind spot. A module may be enriched because 80% of its
genes move in one direction in cohort A and 55% move in the same direction in
cohort B, even while the individual genes that drive the signal differ.
Module membership is not evidence that the same biological programme is
active. Gene-level sign concordance is the missing check. This concern is
reinforced by transcriptomic benchmarking showing that marginal gene-by-gene
selection can be biased by coexpression structure, so aggregation may not
represent the gene-level behaviour required for replication [6].

We therefore built a reproducibility audit around public human IVD
transcriptomes. The audit asks four questions. First, are the compared
samples measuring the same tissue and endpoint? Second, could a global shift,
processing confound, or detection-depth difference explain the apparent
effect? Third, is the module internally reproducible? Fourth, do the same
genes move in the same direction in an independent cohort?

The audit is not a new pathway discovery study. It is a negative-control and
reporting framework for public-data claims, using gene sets that were fixed
before the cross-cohort comparison. It contributes three elements: a matched
IVD case study, a reusable gene-level reproducibility gate, and a claim ladder
that separates exploratory, internally stable, contextually concordant,
candidate-replicated and FDR-controlled claims. The contribution is not a new
statistical test or algorithm. It is the integration of domain-matched
evidence, operational claim gates, and sensitivity analyses spanning donor
dependence, probe selection, gene identity, scale and FDR-family structure.

## Methods

### Data sources

We used the public human IVD tissue cohorts already present in the analysis
workspace. The primary graded comparison used GSE70362 (annulus fibrosus and
nucleus pulposus; Thompson grades I-V) and GSE23130 (annulus fibrosus;
histological grades I-V). Additional tissue cohorts were GSE186542,
GSE167199, GSE146904 and GSE207176. The reproducibility analysis did not use
the blood cohorts because the question concerned tissue programme
transferability, not blood-versus-tissue generality. GEO is an international
public repository that archives raw data, processed data and metadata for
high-throughput functional genomic datasets [7]. GSE70362 was originally
reported by Kazezian et al. [8], GSE23130 by Gruber et al. [9], and
GSE167199 by Li et al. [10].

The strict primary analysis used 20 GSE70362 annulus fibrosus samples of
Thompson grade I-IV and 15 GSE23130 laser-capture samples of grade I-IV. The
all-sample comparison used 24 GSE70362 annulus fibrosus samples and all 23
GSE23130 samples.

### Analysis timing and prespecification

An internal analysis plan was frozen on 2026-09-16 before the final
permutation run. It is available as `Frozen Analysis Plan.md` and
`docs/analysis_plan_v2.md`. It was not publicly preregistered. In this
manuscript, "prespecified" therefore means that the final sensitivity
analyses and claim language were fixed before that run, not that the whole
investigation was prospective, blinded or registered in advance. Earlier
exploratory work informed cohort and endpoint selection. The audit should
therefore be read as a transparent retrospective analysis with an internal
freeze rather than a publicly registered prospective study.

### Harmonisation and effect estimation

GEO series matrices were parsed directly. Probes were mapped to Entrez or
gene symbols using the supplied platform annotations and the human gene_info
table. When multiple probes mapped to one symbol, the probe with the highest
mean expression was retained as the primary rule. Sensitivity analyses also
used the first probe, the median across probes, and repeated random-probe
selection. The primary gene-identity rule retained supplied platform symbols;
an alias-aware sensitivity additionally mapped historical symbols through
current synonyms and nomenclature-authority symbols.

For each cohort we fitted gene-wise linear models to the normalized
expression matrix. Direction was defined as increasing with degeneration
grade. The strict GSE70362 model included grade and batch; the strict
GSE23130 model included grade and tissue source. The all-sample GSE23130
model also included processing method. The all-sample GSE70362 model used the
annulus fibrosus subset to reduce tissue heterogeneity. We used an in-house
ordinary least-squares implementation rather than the limma package itself;
limma provides the reference framework for gene-wise linear models of
high-throughput expression data [11].

Grade was used only as a strictly increasing ordinal score: I = 1, I-II =
1.5, II = 2, III = 3 and IV = 4. The reported direction is the sign of a
gene-wise monotone trend. Any strictly increasing recoding of the same grade
order preserves that sign; coefficient magnitudes are scale-dependent and are
not interpreted as equal-step dose responses. The analysis does not test
arbitrary non-monotonic differences among grades.

### Reproducibility gates

Gene-set analysis was introduced to interpret genome-wide profiles through
coordinated gene sets rather than isolated genes [12]. For each gene set we
calculated the fraction of measured genes with positive
effects in each cohort, the median effect, and exact sign-test p-values. A
nominal module gate required same-direction significance in both cohorts and
gene-level sign concordance greater than 50% at p < 0.05. We then added a
strict gate: exact two-sided sign tests with Benjamini-Hochberg FDR across
the 1,554 modules [13]. Cohort-specific direction was also evaluated with
stratified label permutation, Freedman-Lane residual permutation and
rotation-based residual nulls [14]. Gene concordance was evaluated with
size-matched and expression-matched empirical nulls. A module was called
replicated only if the exact FDR gate passed. This does not require every gene
to agree; it asks whether module membership carries information across
cohorts.

We applied the gate to seven prespecified mechanism modules and to 1,554
Hallmark, KEGG and Reactome modules with at least 10 measured genes.

The claim ladder was operationalised as follows. Level 2 required nominal
same-direction significance in both matched cohorts. Level 3 (candidate
gene-level replication) additionally required greater than 50% shared-gene
sign concordance, a one-sided exact sign-test p < 0.05, and a one-sided
size-matched empirical-null p < 0.05. Level 4 (strong cross-cohort
replication) required both the cohort-direction tests and the gene-level
concordance test, both based on two-sided exact sign tests, to survive
Benjamini-Hochberg FDR across the prespecified module family. No module was
written as replicated unless Level 4 was reached.

### Technical diagnostics

We calculated the fraction of genes moving in each direction and the median
gene effect within each cohort. A directional fraction outside 30-70% or an
absolute median effect above 0.2 was flagged as a possible global shift. We
cross-tabulated grade against tissue, batch, processing method and source.
We did not use sva directly; known batch or source variables were included in
the design. The sva framework highlights the broader concern that latent
variation can bias high-throughput experiments [15]. Empirical-Bayes batch
adjustment methods such as ComBat address a related class of problems [16].
The GSE23130 grade V samples occurred only in homogenized tissue; the strict
analysis therefore restricted GSE23130 to laser-capture samples.

Internal reproducibility was measured by 100 repeated grade-stratified
split-half analyses. Within each repeat, gene effects were estimated
independently in the two halves, and the Spearman correlation of the two
effect vectors was recorded. The median split-half correlation was reported
for all genes and for the ECM module.

To address within-donor dependence in GSE70362, we repeated the ECM analysis
using one randomly selected sample per donor and using donor-level cluster
bootstrap. Split-half reliability was also repeated by splitting donors
rather than samples. We estimated the effective number of independent ECM
genes from the correlation spectrum and used expression-matched random gene
sets in addition to size-matched nulls. GSE23130 metadata did not include
donor identifiers, so donor-level resampling was not possible for that
cohort; residual within-donor dependence cannot be excluded. The effective-test
adjustment follows the eigenvalue-based approach of Li and Ji [17].

Finally, we estimated full-sample reliability from split-half correlations
with the Spearman-Brown formula and simulated expected sign concordance under
latent correlations from 0 to 0.8. This tests whether the observed 23.3%
concordance can be explained by reliability attenuation alone.

### Pair comparability and interpretive ceiling

Cohort pairs were classified by how closely their measurement context was
matched. Class A pairs shared tissue compartment, endpoint, processing method
and platform family. Class B pairs shared tissue compartment and endpoint but
differed in processing method or platform family. Class C pairs differed in
tissue compartment or endpoint and were retained as contextual comparisons
only.

The primary GSE70362-GSE23130 comparison is Class B: tissue compartment and
degeneration-grade endpoint are matched, but platform and processing method
are not. Platform identity is structurally confounded with cohort identity,
because each platform is represented by one cohort. No statistical model can
therefore separate platform-specific effects from cohort biology. The audit
can test transfer of a prespecified module signal across the observed
cohorts, but it cannot establish platform-independent biology. This ceiling
applies even if a module passes Level 4.
The MAQC project showed that microarray platforms can be concordant at the
differential-expression level, but that result does not resolve the present
cohort-platform identifiability problem [18].

Grade was also partially non-identifiable within cohorts: source or batch
cells were empty for some grade levels. Adjustment therefore reduces obvious
technical confounding but cannot establish a causal grade effect or remove
all residual confounding.

### Software and code availability

The audit is implemented as a standalone Python project. All tables and
figures are regenerated by `run_audit.py`; statistical tests use exact
binomial tails and do not depend on additional statistical libraries beyond
NumPy and pandas. The code is available in the project repository.

## Results

### Cohort diagnostics

{_markdown_table(diagnostic_table)}

None of the four primary analysis sets showed a global shift. The strict
GSE70362 and GSE23130 sets had fractions up of 43.6% and 55.0%, with median
effects within 0.01 log units. The remaining between-cohort differences were
therefore not explained by a matrix-wide loading difference.

The donor count for GSE23130 is shown as not available because donor
identifiers were not provided in the series metadata. Its 15 strict samples
are therefore sample-level measurements, not validated independent donors.

The grade-processing crosstab showed why the unrestricted GSE23130 analysis
is not sufficient for a replication claim: grade V occurred only in
homogenized samples. Restricting to laser capture removed that specific
confound and left a grade I-IV comparison.

The remaining crosstabs showed partial non-identifiability rather than a
clean crossed design. In the strict GSE23130 subset, grade I occurred only in
CHTN specimens and grade IV only in surgical specimens. In GSE70362, grade II
occurred only in batch 1 and batch 2 did not contain grades III-IV. Adjusted
models are therefore interpreted as nuisance-adjusted associations, not as
fully identified causal grade effects. Grade-only sensitivity models retained
the primary ECM cross-cohort concordance at 23.3% and produced similar
directional estimates, so the principal audit conclusion did not depend on
the adjustment choice.

### ECM module significance does not imply gene-level replication

{_markdown_table(primary_table)}

In the all-sample comparison, the ECM module was strongly positive in
GSE23130 ({_pct(legacy["gse23130_ecm_fraction_up"])} up,
p = {_p(legacy["gse23130_ecm_sign_p"])}) and absent in GSE70362
({_pct(legacy["gse70362_ecm_fraction_up"])} up,
p = {_p(legacy["gse70362_ecm_sign_p"])}). Gene-level concordance was
{_pct(legacy["ecm_sign_concordance"])}, without evidence of concordance above
chance.

The strict grade I-IV laser-capture comparison preserved the contradiction.
GSE23130 remained positive ({_pct(strict["gse23130_ecm_fraction_up"])} up,
p = {_p(strict["gse23130_ecm_sign_p"])}), while GSE70362 remained
non-reproducible at the gene level. The cross-cohort concordance was
{_pct(strict["ecm_sign_concordance"])} (two-sided exact sign p =
{_p(strict["ecm_sign_concordance_p_two_sided"])}).
The same module was therefore a strong result in one cohort and a
non-concordant direction match in the other.

The prespecified highest-mean-probe rule gave 23.3% ECM concordance
(two-sided exact p = 0.0052). Probe-collapsing sensitivity analyses gave
30.0% for the first probe, 33.3% for the median probe, and a median of 36.7%
(2.5-97.5%: 23.3-48.4%) across 100 random-probe selections. No rule exceeded
50%, but the below-chance significance was not robust to probe selection.
The defensible conclusion is therefore failure to exceed chance, not evidence
of statistically significant anti-concordance.

{_markdown_table(probe_table)}

Scale-invariant rank-trend analyses also failed to support cross-cohort
concordance. Unadjusted gene-wise Spearman trends gave 33.3% ECM concordance
(p = 0.0987), and averaging trends within batch or source strata gave 36.7%
(p = 0.2005). In the stratified rank-trend analysis, GSE23130 retained a
positive ECM signal (74.2% up, p = 0.0053), whereas GSE70362 remained
non-directional (53.3% up, p = 0.4278). The result therefore remains below
50% without providing significant evidence of anti-concordance.

{_markdown_table(scale_table)}

Internal split-half analyses showed that both strict datasets contained
moderate gene-level reliability (median Spearman rho {rel_70362:.2f} and
{rel_23130:.2f} for the ECM module). This rules out the simplest explanation
that GSE23130 was pure noise. The evidence supports failure to establish
cross-cohort gene-level replication, not a claim that biological programmes
in the two patient populations are categorically different.

Donor-level sensitivity analyses preserved the negative result.

{_markdown_table(donor_table)}

The effective number of independent ECM genes was low:
{float(effective_genes.loc[effective_genes['cohort'].eq('GSE70362_AF_I_IV'), 'effective_genes'].iloc[0]):.1f}
in GSE70362 and
{float(effective_genes.loc[effective_genes['cohort'].eq('GSE23130_LCM_all'), 'effective_genes'].iloc[0]):.1f}
in GSE23130. We therefore did not treat the binomial sign test as the final
test. An expression-matched null gave an empirical lower-tail probability of
{_p(expression_matched['empirical_p_less'])} for the primary ECM comparison.

Reliability attenuation did not explain the result. With the observed
split-half reliabilities, simulated concordance under zero latent correlation
remained near 50%, whereas the observed concordance was
{_pct(strict["ecm_sign_concordance"])}. The observed ECM effect-size
correlation was
{float(attenuation['observed_ecm_effect_rho'].iloc[0]):.3f}; after
disattenuation it was
{float(attenuation['disattenuated_effect_rho'].iloc[0]):.3f}.

{_markdown_table(attenuation_table)}

The result was not limited to the unweighted sign metric.

{_markdown_table(weighted_table)}

Within-cohort cross-half analyses provided a positive control. Two independent
halves of the same cohort were analyzed with the same models and compared with
the same concordance metric.

{_markdown_table(cross_half_table)}

The donor-level ECM module score also changed in opposite directions:

{_markdown_table(module_score_table)}

Power calibration showed the expected resolution of the gene-level sign test.
With the observed reliabilities, the nominal 30-gene test had limited power,
and the effective-n sensitivity analysis was deliberately conservative.

{_markdown_table(power_table)}

The three permutation schemes agreed on the direction of the ECM result. No
method made GSE70362 nominally directional, while GSE23130 ranged from
borderline to nominally positive.

{_markdown_table(permutation_method_table)}

### A broad module audit produces the same pattern

{_markdown_table(funnel_table)}

Of 1,554 modules, 673 were significant in only one cohort. Thirty-one were
significant in both cohorts; 14 of those also passed the gene-level
concordance gate at nominal p-values. After exact sign-test FDR control,
with permutation and size-matched empirical nulls as sensitivity checks,
{summary["msigdb"]["n_replicated_fdr"]} modules passed the strict gate. No
module was nominally significant in opposite directions in both cohorts,
which is expected for modest correlation: discordance appears as chance-level
gene concordance rather than as a clean sign reversal.
In the terms of Box 1, 14 modules reached Level 3 (candidate gene-level
replication) and 0 reached Level 4 (strong cross-cohort replication).

Gene-identity sensitivity gave the same qualitative result. Mapping 1,098
alias-only platform symbols to current canonical symbols expanded the tested
set from 1,554 to 1,572 modules and increased nominal Level 3 results from 14
to 15. The number significant in both cohorts remained 31, and 0 modules
survived the strict FDR gate.

FDR-family sensitivity also preserved the strict null. Applying
Benjamini-Hochberg separately within Hallmark, KEGG and Reactome yielded 0
collection-local FDR results under both primary and alias-aware mappings.
Nominal gene-level results were 0, 3 and 11 in the primary mapping and 0, 3
and 12 after alias mapping. The module sets were not independent: 1,636 pairs
had Jaccard similarity above 0.5 and 94 above 0.8. The strict result is
therefore not caused only by pooling overlapping collections into one large
FDR family, but the overlap structure limits any interpretation of FDR as
independent evidence across modules.

The module-level directional imbalance and gene-level concordance were
essentially uncorrelated (Spearman rho approximately -0.05). A stronger
module direction in one or both cohorts therefore did not predict that the
same genes would agree in the other cohort.

The nominally replicated modules were not interpreted as mechanisms. Their
names clustered around protein targeting, chaperones, glycosylation,
ER-Golgi transport, autophagy and interferon-related processes, but most did
not survive multiple-testing control. The nominal list is therefore a
hypothesis-generating shortlist, not a biological conclusion.

{_markdown_table(top_replicated)}

### Pairwise tissue cohorts remain close to chance

{_markdown_table(pairwise_display)}

Across 15 tissue cohort pairs, the median gene-level sign concordance was
{_pct(summary["pairwise_tissue"]["median_gene_concordance"])}. This broad
summary is contextual only because the pairs differ in tissue compartment and
endpoint. Large gene counts can make even modest deviations from 50%
statistically significant, which is why effect size is reported alongside the
p-value.

Exact tissue-and-endpoint matches were rare. The complete exact-contrast set
contained {summary["pairwise_tissue_exact"]["n_pairs"]} pair:

{_markdown_table(pairwise_exact_display)}

Relaxing the requirement to the same compartment and endpoint class added
{summary["pairwise_tissue_compartment_matched"]["n_pairs"]} further pairs:

{_markdown_table(pairwise_compartment_display)}

The full 15-pair table is retained in the supplement as exploratory context.
The exact-contrast result is not pooled with the broader set.

### No comparable third AF severity cohort was identified

We maintained a third-cohort registry with explicit eligibility tiers. The
current public-data landscape does not contain a Tier A cohort matching the
primary AF I-IV comparison.

{_markdown_table(third_cohort_summary)}

`GSE176205` is an NP bulk RNA-seq cohort (3 controls and 6 degeneration
samples), but its raw group contrast shows a severe global shift: only
{_pct(gse176205_summary["gse176205_diagnostics"]["fraction_up"])} of genes move
upward, with median effect
{gse176205_summary["gse176205_diagnostics"]["median_effect"]:+.3f}. Per-sample
median centering removes the global shift, after which the ECM direction has
only {_pct([row for row in gse176205_modules.to_dict("records") if row["module"] == "ECM remodelling"][0]["gse176205_centered_fraction_up"])}
positive genes and concordance with the GSE70362 NP effect of
{_pct([row for row in gse176205_modules.to_dict("records") if row["module"] == "ECM remodelling"][0]["gene_concordance"])}.
This is retained as a contrast-specific sensitivity analysis, not a third
severity cohort.

{_markdown_table(gse176205_display)}

`GSE17077` was corrected from a secondary-paper label of normal versus
degenerated AF to its official design: senescent versus non-senescent
laser-capture annulus cells. Eight donors had paired senescent and
non-senescent samples. The global paired effect showed no shift, but the ECM
module was not enriched in senescent cells
({_pct([row for row in gse17077_modules.to_dict("records") if row["module"] == "ECM remodelling"][0]["fraction_up"])}
positive).

{_markdown_table(gse17077_display)}

### Scoping audit of multi-cohort language

To test whether the reporting issue is plausible in the accessible IVD
literature, we performed a language-level scoping audit of the open-access
full-text corpus. This is not a systematic review and cannot establish
prevalence.

{_markdown_table(literature_table)}

The strongest defensible interpretation is that multi-cohort analyses and
consistency language are common in the scoping corpus, while explicit
gene-level concordance language was not detected. The absence of a phrase is
not proof that an analysis was absent, but it identifies a reporting gap.

### Blood cohorts were reproduced but excluded from the tissue claim

The two external blood cohorts were successfully reconstructed from raw
archives. They are retained as exploratory cross-compartment context only.

{_markdown_table(blood_table)}

## Discussion

### Novelty and relationship to prior work

Several components of this audit are established. Random-signature studies
show that biologically unrelated gene sets can appear significant [19],
marginal selection can be biased by coexpression [6], batch and latent
variation can distort high-throughput data [15,16], and cross-platform
concordance depends strongly on analysis choices [18]. Reporting frameworks
such as STROBE and FAIR address adjacent transparency and reuse problems
[20,21]. The novel contribution of this paper is therefore not a new
statistic or algorithm. It is the integrated, domain-matched IVD audit that
combines gene-level sign concordance, an operational claim ladder and a
sensitivity battery spanning donor dependence, probe selection, gene
identity, scale and FDR-family structure.

### Principal finding

Module-level agreement is not replication. In the clearest matched comparison,
the same ECM module was significant and moderately internally reliable in GSE23130
but its gene-level direction was not supported in GSE70362. The result
persisted under donor-level resampling and did not arise from reliability
attenuation. Alternative probe-collapsing rules remained below 50%
concordance but showed that the exact below-chance magnitude was not robust.
The broad audit found hundreds of one-cohort module signals; no
module survived the strict exact-sign FDR gate. This pattern aligns with a
cross-omic sCJD analysis, where FDR-controlled gene-set overlap was absent and
nominal overlap remained exploratory [1], and with a glioma audit in which a
well-calibrated signature was indistinguishable from random-signature and
clinical-reference benchmarks in external validation [2].
Random-signature studies further show that gene sets unrelated to the
clinical outcome can appear significant [19].

### Why this matters

Public IVD transcriptomes are heterogeneous. They differ in tissue
compartment, dissection or digestion, platform, grade scale, sample size and
clinical context. A module score integrates those differences into a single
direction, which can make two cohorts look more similar than their underlying
genes. Gene-level concordance is a direct check on that aggregation.
Benchmarking studies also show that gene-gene dependencies can bias marginal
selection, so aggregation should be explicitly validated rather than assumed
to preserve gene-level signal [6].

The audit also shows why technical checks alone are insufficient. The primary
cohorts passed the global-shift screen, and the strict comparison removed the
known grade-processing confound. The failure occurred after those checks, at
the cross-cohort gene level. The comparison is nevertheless Class B rather
than Class A: cohort and platform remain structurally confounded, so even a
positive result could support only statistical transfer across the observed
cohorts, not platform-independent biology.

Context dependence is not unique to IVD. A compact sepsis blood signature
discriminated in one clinically distinct validation contrast but was near-null
for infection source and short-term survival in other Day 1 settings [22],
whereas an exploratory ICU sepsis transcriptomic score was sensitive to
cell-composition adjustment and was explicitly framed as an observational
state rather than target engagement [23]. These examples support matching each
reproducibility claim to the tissue, endpoint, processing method and clinical
context in which it is made.

Recent IVD single-cell and spatial studies provide biological context for
fibrotic NP cell states and matrix-integrin programmes, including
WNT/FN1-CD44 and integrin/N-glycosylation axes [24,25]. Such findings support
plausibility but do not imply that the bulk ECM module investigated here is
replicated across cohorts; biological relevance and reproducibility are
separate claims.

**Box 1. Claim ladder for public-data module reproducibility.**

| Level | Claim | Minimum evidence | Permitted language |
|---|---|---|---|
| 0 | Exploratory module signal | Significant module in one cohort | exploratory or hypothesis-generating |
| 1 | Internally reproducible module | Repeated split-half or permutation supports within-cohort direction | internally stable, not independently replicated |
| 2 | Contextually concordant module | Same prespecified module direction in matched independent cohorts | consistency in this matched context |
| 3 | Candidate gene-level replication | Same-direction significance in both cohorts; >50% shared-gene sign concordance; one-sided exact and size-matched empirical-null p < 0.05 | candidate replication requiring confirmation |
| 4 | Strong cross-cohort replication | Both two-sided exact module-direction tests and gene-level concordance survive FDR across the prespecified family | statistically replicated across the observed cohorts in the matched tissue and endpoint context, not platform-independent |

Claim level does not override pair comparability. A Level 4 finding in a
Class B pair supports statistical transfer across the observed cohorts only;
platform-independent or mechanistic replication requires Class A data,
additional independent cohorts or experimental validation.

### Reporting recommendation

The recommendation below follows the claim ladder in Box 1. For public-data
IVD studies, we recommend a four-line reproducibility statement for every
claimed module:

1. Report the module direction and exact sign-test p-value in each cohort.
2. Report the proportion of shared genes moving in the same direction and its
   exact and empirical p-value.
3. Report an internal reliability estimate and state whether the comparison is
   matched by tissue, endpoint and processing.
4. For multiple modules, report multiplicity control and state whether the
   result survives FDR.

Words such as "replicated" or "consistent" should be reserved for findings
that pass all four layers. A one-cohort module is exploratory even when its
p-value is small.

Where cell-resolved data are available, the same reporting logic should be
applied at donor and cell-state level. Annotation should be independently
validated or consensus-based [26], and cross-cohort classification should be
evaluated on held-out donors using pseudobulk or comparable aggregation rather
than treating individual cells as independent samples [27]. Machine-readable
metadata and executable workflow descriptions should accompany the analysis
to make provenance and parameter choices traceable [28]. When cell-resolved
designs use hashtag-assisted pooling, the trade-off between batch-effect
mitigation and demultiplexing cell loss should be reported explicitly, because
pooled designs can remove cells required for downstream pseudobulk comparisons
[29]. Established reporting statements such as STROBE provide a broader
framework for transparent observational research reporting [20].

### Limitations

The audit is retrospective and uses public cohorts with different platforms
and processing methods. The strict comparison has 20 and 15 samples, limited
power for small gene sets, and cannot eliminate all platform-specific effects.
This limitation defines the claim: the observed data do not establish
cross-cohort gene-level replication. They do not prove that the underlying
biology is absent or opposite.

No Tier A third AF severity cohort was identified, so the strongest domain
statement is that the current public-data landscape does not provide the
independent evidence needed for such a claim. The literature component is a
scoping language audit rather than a systematic review. The results therefore
identify a reporting and data gap, not a prevalence estimate across all IVD
studies.

Because the primary cohorts differ in platform and processing method, cohort
and platform effects are not identifiable separately. The negative primary
result is therefore a failure to establish cross-cohort gene-level
transferability, not proof that a shared biological programme is absent. A
future positive result would require the same qualification.

The analysis was not publicly preregistered. The internal freeze limits, but
does not eliminate, concern that the primary comparison or sensitivity
analyses were selected after exploratory inspection.

Donor identifiers were available only for GSE70362. GSE23130 was analysed at
the sample level because its GEO metadata did not identify donors, so
residual within-donor dependence in that cohort remains unresolved.

Grade, batch, source and processing method were not fully crossed. Some grade
levels occurred in only one nuisance stratum, so the adjusted grade
coefficients are not fully identified causal effects. The grade-only
sensitivity analysis reproduced the primary ECM concordance, but residual
confounding remains a limitation.

Grade was modelled as an ordinal trend rather than as a categorical exposure.
This choice preserves the sign of monotonic gene-level associations under any
strictly increasing coding, but it does not capture non-monotonic differences
among grades and does not justify interpreting coefficient magnitudes as
linear dose-response effects.

The primary probe rule retained the highest-mean probe per gene. Alternative
first-probe, median-probe and random-probe rules remained below 50% ECM
concordance, but the exact below-chance magnitude depended on probe
selection. The study therefore does not claim statistically significant
anti-concordance.

Gene identity was also imperfect. Of 22,107 platform symbols, 1,098 were
mapped only through historical aliases, 3,305 remained unresolved, and 4,434
ambiguous alias keys were removed to avoid conflicting mappings. The
alias-aware sensitivity did not change the primary ECM comparison or the FDR
conclusion, but broad module counts were mapping-sensitive.

The scale-invariant rank-trend analysis preserved direction in GSE23130 but
gave only 33.3-36.7% cross-cohort ECM concordance, with two-sided p-values
between 0.0987 and 0.2005. The primary below-chance p-value is therefore not
treated as robust evidence of anti-concordance.

The module family was operationally defined as one global
Hallmark/KEGG/Reactome family. Collection-local FDR analyses also produced
zero strict results, but module overlap was substantial: 1,636 pairs exceeded
Jaccard 0.5 and 94 exceeded 0.8. FDR therefore should not be interpreted as
evidence from thousands of independent hypotheses.

The nominally replicated modules require independent cohorts and, where
possible, experimental validation. Recent single-cell evidence for fibrotic NP
states and matrix-integrin programmes [24,25] does not remove the need for an
independent bulk severity cohort or experimental validation, and it does not
establish causality for the present module result. No result in this study
establishes a causal mechanism.

## Data availability

All source cohorts are public GEO series: GSE70362, GSE23130, GSE186542,
GSE167199, GSE146904 and GSE207176. MSigDB 2024.1 files were used for the
module audit. The derived effect tables, audit results, figures and
manuscript are generated by the code in this project, which is available at
https://github.com/wdsve/ivd-repro-audit and archived at
https://doi.org/10.5281/zenodo.23133983. Machine-readable
metadata and executable workflow descriptions would make the analysis easier
to reuse and audit [28]. The FAIR principles provide the underlying standard
for findable, accessible, interoperable and reusable data and metadata [21].

## Figure legends

**Figure 1. A reproducibility gate for cross-cohort omics claims.** The
workflow moves from cohort inventory to harmonisation, technical diagnostics,
independent-unit re-estimation, module and gene-level testing, and reporting.
Each gate can stop a claim before it is written as replication.

**Figure 2. ECM module significance does not reproduce at the gene level.**
(A) Fraction of ECM genes increasing with degeneration in GSE23130 and
GSE70362 under all-sample and strict grade I-IV analyses. (B) Gene-level sign
concordance between the two cohorts. The dashed reference is 50%. The strict
comparison is below 50%, but the exact below-chance magnitude depends on the
probe-collapsing rule. Internal split-half correlations show that both
cohorts contain moderate ECM reliability, so the failure is not explained by
the absence of within-cohort signal.

**Figure 3. Broad MSigDB module audit.** Each point is a Hallmark, KEGG or
Reactome module with at least 10 measured genes. The x-axis is the maximum
absolute deviation from 50% directional balance in either cohort; the y-axis
is gene-level sign concordance. The bar panel summarises the audit funnel.

**Figure 4. Pairwise tissue cohort concordance.** Gene-level sign concordance
for 15 pairs of public human IVD tissue cohorts. The vertical reference at
50% denotes chance. Most pairs cluster near chance, and the highest pair
remains below 60%.

**Figure 5. Donor-level sensitivity and reliability attenuation.** (A)
One-sample-per-donor and donor cluster-bootstrap distributions for the
GSE70362 ECM directional fraction. (B) The corresponding cross-cohort
gene-level concordance. (C) Simulated sign concordance under latent
correlations from 0 to 0.8 using the observed split-half reliabilities. The
red line is the observed ECM concordance.

**Figure 6. Positive controls and power calibration.** (A) Cross-cohort ECM
concordance compared with within-cohort cross-half positive controls. (B)
Power of the nominal 30-gene sign test across simulated latent correlations.
(C) Unweighted, effect-size-weighted and top-half effect concordance.

## References

1. Oberoi RK, Gurung D, Harris LK. Cross-Omic Comparative Analysis Identifies Transcriptomic Signatures and Exploratory Gene Set-Level Signals in Sporadic Creutzfeldt-Jakob Disease. *International Journal of Molecular Sciences*. 2026;27:6560. doi:10.3390/ijms27156560

2. Yasar S, Yagin B, Alzakari SA, et al. Evaluating a Glioma Transcriptomic Signature Against a Clinical Reference Model and a Random-Signature Null Distribution: A Leakage-Controlled Internal Audit and a Survey of the Field. *Diagnostics*. 2026;16:2803. doi:10.3390/diagnostics16172803

3. Ioannidis JPA. Why most published research findings are false. *PLoS Medicine*. 2005;2:e124. doi:10.1371/journal.pmed.0020124

4. Errington TM, et al. Investigating the replicability of preclinical cancer biology. *eLife*. 2021;10:e71601. doi:10.7554/eLife.71601

5. Open Science Collaboration. Estimating the reproducibility of psychological science. *Science*. 2015;349:aac4716. doi:10.1126/science.aac4716

6. Yu D, Li C, Yan S, et al. Comparative evaluation of gene selection approaches in transcriptomics: bias correction and visualization with TransPro. *GigaScience*. 2026;15:giag057. doi:10.1093/gigascience/giag057

7. Barrett T, et al. NCBI GEO: archive for functional genomics data sets: update. *Nucleic Acids Research*. 2013;41:D991-D995. doi:10.1093/nar/gks1193

8. Kazezian Z, Gawri R, Haglund L, et al. Gene Expression Profiling Identifies Interferon Signalling Molecules and IGFBP3 in Human Degenerative Annulus Fibrosus. *Scientific Reports*. 2015;5:15662. doi:10.1038/srep15662

9. Gruber HE, Hoelscher GL, Ingram JA, Hanley EN. Genome-wide analysis of pain-, nerve- and neurotrophin-related gene expression in the degenerating human annulus. *Molecular Pain*. 2012;8:63. doi:10.1186/1744-8069-8-63

10. Li Z, Sun Y, He M, Liu J. Differentially-expressed mRNAs, microRNAs and long noncoding RNAs in intervertebral disc degeneration identified by RNA-sequencing. *Bioengineered*. 2021;12:1026-1039. doi:10.1080/21655979.2021.1899533

11. Ritchie ME, et al. limma powers differential expression analyses for RNA-sequencing and microarray studies. *Nucleic Acids Research*. 2015;43:e47. doi:10.1093/nar/gkv007

12. Subramanian A, et al. Gene set enrichment analysis: a knowledge-based approach for interpreting genome-wide expression profiles. *PNAS*. 2005;102:15545-15550. doi:10.1073/pnas.0506580102

13. Benjamini Y, Hochberg Y. Controlling the false discovery rate: a practical and powerful approach to multiple testing. *Journal of the Royal Statistical Society Series B*. 1995;57:289-300. doi:10.1111/j.2517-6161.1995.tb02031.x

14. Freedman D, Lane D. A nonstochastic interpretation of reported significance levels. *Journal of Business & Economic Statistics*. 1983;1:292-298. doi:10.1080/07350015.1983.10509354

15. Leek JT, et al. The sva package for removing batch effects and other unwanted variation in high-throughput experiments. *Bioinformatics*. 2012;28:882-883. doi:10.1093/bioinformatics/bts034

16. Johnson WE, Li C, Rabinovic A. Adjusting batch effects in microarray expression data using empirical Bayes methods. *Biostatistics*. 2007;8:118-127. doi:10.1093/biostatistics/kxj037

17. Li J, Ji L. Adjusting multiple testing in multilocus analyses using the eigenvalues of a correlation matrix. *Heredity*. 2005;95:221-227. doi:10.1038/sj.hdy.6800717

18. MAQC Consortium. The MicroArray Quality Control (MAQC) project shows inter- and intraplatform reproducibility of gene expression measurements. *Nature Biotechnology*. 2006;24:1151-1161. doi:10.1038/nbt1239

19. Venet D, Dumont JE, Detours V. Most random gene expression signatures are significantly associated with breast cancer outcome. *PLoS Computational Biology*. 2011;7:e1002240. doi:10.1371/journal.pcbi.1002240

20. von Elm E, Altman DG, Egger M, et al. The Strengthening the Reporting of Observational Studies in Epidemiology (STROBE) statement: guidelines for reporting observational studies. *Lancet*. 2007;370:1453-1457. doi:10.1016/S0140-6736(07)61602-X

21. Wilkinson MD, Dumontier M, Aalbersberg IJ, et al. The FAIR Guiding Principles for scientific data management and stewardship. *Scientific Data*. 2016;3:160018. doi:10.1038/sdata.2016.18

22. Qin C, Wang W, Du Q, et al. An 11-gene blood transcriptomic signature reflects a sepsis-associated host-response pattern across public cohorts. *Frontiers in Medicine*. 2026;13:1844619. doi:10.3389/fmed.2026.1844619

23. Yang X, Hu T, Wang J, et al. An NLRP3 inflammasome-anchored Astragalus mechanistic prior yields a mortality-associated transcriptomic signal in ICU sepsis: a secondary analysis with exploratory cross-cohort assessment. *Inflammation Research*. 2026;75:201. doi:10.1007/s00011-026-02352-0

24. Li Q, Liang G, Bo K, et al. Single-cell and spatial transcriptomics characterisation of RSPO2+ nucleus pulposus cells reveals a WNT/FN1-CD44 degenerative axis and therapeutic targets in IVDD. *Journal of Orthopaedic Translation*. 2026;60:101203. doi:10.1016/j.jot.2026.101203

25. Qiang S, Liu Y, Dong Y, et al. ITGBL1 and RPN1 Mark a Fibrotic NP Subpopulation with Coupled Integrin Signaling and N-Glycosylation Programs in IVDD. *Journal of Inflammation Research*. 2026;19:629922. doi:10.2147/JIR.S629922

26. Sun L, Ma L, Chen L, et al. Annotation of cell types in single-cell sequencing for cardiovascular disease: concepts, workflows, challenges, and best practices. *International Journal of Biochemistry and Cell Biology*. 2026;201:107027. doi:10.1016/j.biocel.2026.107027

27. Marchi A, Anwer D, Kerkhoven E, et al. Cell-Type-Resolved Pseudobulk Classification Across Independent Cohorts Identifies Microglial PTPRG as a Transcriptional Hub in Alzheimer's Disease. *bioRxiv*. 2026. Preprint. doi:10.64898/2026.04.07.717029

28. Dörpholz H, Simon R, Usadel B, Kranz A. Integrating cross-omics research through FAIR Digital Objects with DataPLANT. *Journal of Integrative Bioinformatics*. 2025;22(4):20250056. doi:10.1515/jib-2025-0056

29. Chatterjee B, Gorga K, Blair C, et al. Moderated designs can balance between batch-effect mitigation and cell loss due to hashtag-assisted pooling in single-cell experiments. *Genome Research*. 2026. Published online July 30, 2026. doi:10.1101/gr.281624.125
"""

    (manuscript_dir / "manuscript.md").write_text(manuscript, encoding="utf-8")

    abstract_zh = f"""# 中文摘要

**标题：** 模块层面一致不等于复制：公共人椎间盘转录组的报告与可复现性门槛

**背景：** 公共椎间盘转录组研究常把单队列中显著的模块，或两个队列中
方向相似的模块，写成“一致”或“验证”。但模块方向可以由不同基因子集
驱动；如果不检查基因级方向一致率，模块层面的相似性无法证明同一个
生物学程序被复制。

**方法：** 审计 6 个公共人椎间盘组织转录组队列，并对两个最大的分级纤维环
队列 GSE70362 与 GSE23130 做匹配分析。严格比较限定为 Thompson I-IV 级、
纤维环、LCM 样本；效应量使用校正批次或组织来源的线性模型估计。对每个
基因集同时报告队列内方向、精确符号检验和跨队列基因级方向一致率。还审计
1,554 个 Hallmark、KEGG 和 Reactome 模块，并用 100 次分层 split-half
评估队列内部可靠性；同时加入供者单样本、供者 cluster bootstrap、
phenotype permutation、表达匹配零模型和 FDR 控制。

**结果：** 严格比较中，GSE23130 的 ECM 重塑模块有
{_pct(strict["gse23130_ecm_fraction_up"])} 个基因上调
（p = {_p(strict["gse23130_ecm_sign_p"])}），GSE70362 仅
{_pct(strict["gse70362_ecm_fraction_up"])} 个基因上调
（p = {_p(strict["gse70362_ecm_sign_p"])}）。但两队列 ECM 基因级方向
一致率只有 {_pct(strict["ecm_sign_concordance"])}
（双侧符号检验 p = {_p(strict["ecm_sign_concordance_p_two_sided"])}），
低于随机的 50%。
两个队列内部 split-half 相关系数分别为 {rel_70362:.2f} 和
{rel_23130:.2f}。供者单样本和 cluster bootstrap 分析也维持约 50% 的
GSE70362 ECM 方向和约 30% 的跨队列一致率，说明失败并非单纯由单队列
噪声或供者重复采样造成。

在 1,554 个模块中，{summary["msigdb"]["n_significant_one_sided"]} 个只在
一个队列显著，{summary["msigdb"]["n_significant_both"]} 个在双队列显著，
只有 {summary["msigdb"]["n_gene_level_replicated"]} 个通过名义基因级复核；
加入 permutation 和 FDR 后为 {summary["msigdb"]["n_replicated_fdr"]} 个。
15 对组织队列的中位基因级方向一致率为
{_pct(summary["pairwise_tissue"]["median_gene_concordance"])}，最高仅
{_pct(summary["pairwise_tissue"]["max_gene_concordance"])}。

**结论：** 椎间盘公共转录组中的模块级“一致性”不能替代基因级跨队列
复制。任何“replicated”或“consistent”表述，都应同时给出模块方向、
基因级方向一致率和内部可靠性；单队列模块只能写作探索性发现。
"""
    (manuscript_dir / "abstract_zh.md").write_text(abstract_zh, encoding="utf-8")

    supplement = f"""# Supplementary material

## Table S1. Primary comparison

{_markdown_table(primary_table)}

## Table S2. Cohort effect diagnostics

{_markdown_table(diagnostic_table)}

## Table S3. Internal split-half reliability

{_markdown_table(reliability)}

## Table S4. Full MSigDB audit

The complete audit of {len(msigdb)} modules is provided as
`results/msigdb_module_audit.csv`.

## Table S5. Pairwise tissue cohort concordance

{_markdown_table(pairwise_display)}

## Table S6. Prespecified mechanism modules

The complete comparison is provided as
`results/curated_module_audit.csv`.

## Table S7. Donor-level sensitivity

{_markdown_table(donor_table)}

## Table S8. Reliability attenuation

{_markdown_table(attenuation_table)}

## Table S9. Effective independent genes

{_markdown_table(effective_genes)}

## Table S10. Expression-matched ECM null

{_markdown_table(pd.DataFrame([expression_matched]).rename(columns={"index": "module"}))}

## Table S11. Cross-half positive controls

{_markdown_table(cross_half_table)}

## Table S12. Weighted concordance

{_markdown_table(weighted_table)}

## Table S13. Power calibration

{_markdown_table(power_table)}

## Table S14. Module score slopes

{_markdown_table(module_score_table)}

## Table S15. Permutation-method sensitivity

{_markdown_table(permutation_method_table)}

## Table S16. Exact-contrast cohort pairs

{_markdown_table(pairwise_exact_display)}

## Table S17. Compartment-matched cohort pairs

{_markdown_table(pairwise_compartment_display)}

## Table S18. GSE176205 NP directional validation

{_markdown_table(gse176205_display)}

## Table S19. GSE17077 paired senescence analysis

{_markdown_table(gse17077_display)}

## Table S20. Third-cohort registry summary

{_markdown_table(third_cohort_summary)}

## Table S21. Literature scoping audit

{_markdown_table(literature_table)}

## Table S22. Reproduced blood cohorts

{_markdown_table(blood_table)}

## Table S23. Probe-to-symbol collapsing sensitivity

{_markdown_table(probe_table)}

The primary analysis used the highest-mean probe per gene. Alternative
collapsing rules and 100 random-probe selections did not exceed 50% ECM
concordance, but they showed that the exact below-chance level in the primary
analysis was sensitive to probe selection.

## Table S24. Gene-identity sensitivity

{_markdown_table(gene_identity_table)}

The primary mapping retained supplied platform symbols. The alias-aware
mapping additionally used current synonyms and nomenclature-authority symbols
from human gene_info. It recovered 1,098 alias-only symbols but left 3,305
unresolved and removed 4,434 ambiguous alias keys. The strict FDR conclusion
remained zero modules, while broader nominal counts changed modestly.

## Table S25. Scale-invariant trend sensitivity

{_markdown_table(scale_table)}

Spearman trends are invariant to any strictly increasing transformation of
each gene across samples and therefore test whether the direction call is
driven by platform-specific scale assumptions. The stratified analysis
averages gene-wise Spearman trends within batch or source strata with at least
four samples and three observed grades.

## Table S26. Module-family FDR and overlap sensitivity

{_markdown_table(family_table)}

The module sets were not independent. Among 1,554 tested modules, 243,830
pairs had nonzero Jaccard overlap, 1,636 exceeded Jaccard 0.5 and 94 exceeded
0.8. Collection-local FDR was zero for Hallmark, KEGG and Reactome under both
primary and alias-aware mappings.

## Technical diagnostic tables

The grade, batch, processing-method and source crosstabs are provided in
`results/confound_*.csv`. These tables are part of the stopping rules: the
unrestricted GSE23130 comparison is not used as the primary replication test
because grade V occurs only in homogenized samples.
"""
    (manuscript_dir / "supplement.md").write_text(supplement, encoding="utf-8")

    cover = f"""# Cover letter

Dear Editor,

We submit a methodological audit and reporting framework for cross-cohort
reproducibility in public human intervertebral disc transcriptomes. The
central finding is that module-level significance is not replication. In a
strictly matched grade I-IV annulus fibrosus comparison, the ECM remodelling
module was significant and internally reproducible in GSE23130 but had only
{_pct(strict["ecm_sign_concordance"])} gene-level directional concordance with
GSE70362. This result persisted in donor-level one-sample and cluster-bootstrap
analyses.

The manuscript provides a reusable audit workflow and a reporting standard
for public-data studies in this field. It does not claim a new disease
mechanism and does not overstate the limited causal value of public
transcriptomes. Its contribution is not a new statistical test, but an
integrated IVD-specific audit that links a matched cross-cohort comparison to
an operational claim ladder and a broad sensitivity battery.

Sincerely,

The submitting author

22. Qin C, Wang W, Du Q, et al. An 11-gene blood transcriptomic signature reflects a sepsis-associated host-response pattern across public cohorts. *Frontiers in Medicine*. 2026;13:1844619. doi:10.3389/fmed.2026.1844619

23. Yang X, Hu T, Wang J, et al. An NLRP3 inflammasome-anchored Astragalus mechanistic prior yields a mortality-associated transcriptomic signal in ICU sepsis: a secondary analysis with exploratory cross-cohort assessment. *Inflammation Research*. 2026;75:201. doi:10.1007/s00011-026-02352-0

24. Li Q, Liang G, Bo K, et al. Single-cell and spatial transcriptomics characterisation of RSPO2+ nucleus pulposus cells reveals a WNT/FN1-CD44 degenerative axis and therapeutic targets in IVDD. *Journal of Orthopaedic Translation*. 2026;60:101203. doi:10.1016/j.jot.2026.101203

25. Qiang S, Liu Y, Dong Y, et al. ITGBL1 and RPN1 Mark a Fibrotic NP Subpopulation with Coupled Integrin Signaling and N-Glycosylation Programs in IVDD. *Journal of Inflammation Research*. 2026;19:629922. doi:10.2147/JIR.S629922

26. Sun L, Ma L, Chen L, et al. Annotation of cell types in single-cell sequencing for cardiovascular disease: concepts, workflows, challenges, and best practices. *International Journal of Biochemistry and Cell Biology*. 2026;201:107027. doi:10.1016/j.biocel.2026.107027

27. Marchi A, Anwer D, Kerkhoven E, et al. Cell-Type-Resolved Pseudobulk Classification Across Independent Cohorts Identifies Microglial PTPRG as a Transcriptional Hub in Alzheimer's Disease. *bioRxiv*. 2026. Preprint. doi:10.64898/2026.04.07.717029

28. Dörpholz H, Simon R, Usadel B, Kranz A. Integrating cross-omics research through FAIR Digital Objects with DataPLANT. *Journal of Integrative Bioinformatics*. 2025;22(4):20250056. doi:10.1515/jib-2025-0056

29. Chatterjee B, Gorga K, Blair C, et al. Moderated designs can balance between batch-effect mitigation and cell loss due to hashtag-assisted pooling in single-cell experiments. *Genome Research*. 2026. Published online July 30, 2026. doi:10.1101/gr.281624.125
"""
    (manuscript_dir / "cover_letter.md").write_text(cover, encoding="utf-8")
