#!/usr/bin/env python
"""Run the cross-cohort reproducibility audit and write all result tables."""

from __future__ import annotations

import argparse
import hashlib
import json
import platform
from datetime import datetime, timezone
from pathlib import Path

import numpy as np
import pandas as pd

from ivd_audit.audit import (
    MECHANISM_SETS,
    add_size_matched_concordance_p,
    cross_half_concordance,
    donor_effect_sensitivity,
    effect_diagnostics,
    expression_matched_concordance_p,
    fit_effect_model,
    module_table,
    module_score_slope,
    paired_module_audit,
    pairwise_concordance,
    permutation_module_directions,
    prepare_gse70362,
    prepare_gse23130,
    read_msigdb_symbol_sets,
    sign_concordance_power,
    split_half_reliability,
    weighted_sign_concordance,
)
from ivd_audit.core import (
    benjamini_hochberg,
    disattenuate_correlation,
    effective_gene_number,
    sign_concordance,
    simulate_sign_concordance,
    spearman_brown,
    spearman_correlation,
    summarise_gene_set,
)
from ivd_audit.figures import (
    draw_calibration,
    draw_ecm_paradox,
    draw_msigdb_audit,
    draw_pairwise_concordance,
    draw_sensitivity,
    draw_workflow,
)
from ivd_audit.report import write_manuscript


def _primary_comparison(
    effects_a: pd.Series,
    effects_b: pd.Series,
    label: str,
) -> dict[str, object]:
    module = summarise_gene_set(effects_a, MECHANISM_SETS["ECM remodelling"])
    module_b = summarise_gene_set(effects_b, MECHANISM_SETS["ECM remodelling"])
    concordance = sign_concordance(effects_a, effects_b)
    shared_ecm = [
        gene
        for gene in MECHANISM_SETS["ECM remodelling"]
        if gene in effects_a.index and gene in effects_b.index
    ]
    ecm_concordance = sign_concordance(
        effects_a.reindex(shared_ecm),
        effects_b.reindex(shared_ecm),
    )
    return {
        "comparison": label,
        "cohort_a": "GSE70362",
        "cohort_b": "GSE23130",
        "gse70362_ecm_n": module["n_genes"],
        "gse70362_ecm_fraction_up": module["fraction_up"],
        "gse70362_ecm_median_effect": module["median_effect"],
        "gse70362_ecm_sign_p": module["sign_p_greater"],
        "gse23130_ecm_n": module_b["n_genes"],
        "gse23130_ecm_fraction_up": module_b["fraction_up"],
        "gse23130_ecm_median_effect": module_b["median_effect"],
        "gse23130_ecm_sign_p": module_b["sign_p_greater"],
        "genome_sign_concordance": concordance["fraction"],
        "genome_sign_concordance_p": concordance["binomial_p_greater"],
        "genome_sign_concordance_p_less": concordance["binomial_p_less"],
        "genome_sign_concordance_p_two_sided": concordance[
            "binomial_p_two_sided"
        ],
        "ecm_sign_concordance": ecm_concordance["fraction"],
        "ecm_sign_concordance_p": ecm_concordance["binomial_p_greater"],
        "ecm_sign_concordance_p_less": ecm_concordance["binomial_p_less"],
        "ecm_sign_concordance_p_two_sided": ecm_concordance[
            "binomial_p_two_sided"
        ],
    }


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--project-root",
        type=Path,
        default=Path(__file__).resolve().parents[1],
    )
    parser.add_argument("--phenotype-permutations", type=int, default=199)
    parser.add_argument("--concordance-permutations", type=int, default=5000)
    parser.add_argument("--donor-bootstrap", type=int, default=300)
    parser.add_argument("--split-half-repetitions", type=int, default=100)
    parser.add_argument(
        "--skip-manuscript",
        action="store_true",
        help="Write statistical outputs without regenerating the manuscript.",
    )
    args = parser.parse_args()
    root = args.project_root.resolve()
    output = Path(__file__).resolve().parent / "results"
    output.mkdir(parents=True, exist_ok=True)
    figure_output = Path(__file__).resolve().parent / "figures"
    figure_output.mkdir(parents=True, exist_ok=True)

    expression_70362, metadata_70362 = prepare_gse70362(root)
    expression_23130, metadata_23130 = prepare_gse23130(root)

    af_all = metadata_70362["tissue"].eq("Annulus fibrosus").to_numpy()
    af_i_iv = af_all & metadata_70362["grade"].between(1, 4).to_numpy()
    lcm_all = metadata_23130["method"].eq("LCM").to_numpy()

    subsets = {
        "GSE70362_AF_all": (
            expression_70362.loc[:, af_all],
            metadata_70362.loc[af_all].reset_index(drop=True),
            ["grade"],
            ["batch"],
        ),
        "GSE70362_AF_I_IV": (
            expression_70362.loc[:, af_i_iv],
            metadata_70362.loc[af_i_iv].reset_index(drop=True),
            ["grade"],
            ["batch"],
        ),
        "GSE23130_all": (
            expression_23130,
            metadata_23130.reset_index(drop=True),
            ["grade"],
            ["method", "source"],
        ),
        "GSE23130_LCM_all": (
            expression_23130.loc[:, lcm_all],
            metadata_23130.loc[lcm_all].reset_index(drop=True),
            ["grade"],
            ["source"],
        ),
        "GSE70362_AF_I_IV_grade_only": (
            expression_70362.loc[:, af_i_iv],
            metadata_70362.loc[af_i_iv].reset_index(drop=True),
            ["grade"],
            [],
        ),
        "GSE23130_LCM_grade_only": (
            expression_23130.loc[:, lcm_all],
            metadata_23130.loc[lcm_all].reset_index(drop=True),
            ["grade"],
            [],
        ),
    }

    effects: dict[str, pd.Series] = {}
    diagnostic_rows: list[dict[str, object]] = []
    reliability_rows: list[dict[str, object]] = []
    for name, (expression, metadata, continuous, categorical) in subsets.items():
        model_effects = fit_effect_model(
            expression,
            metadata,
            continuous=continuous,
            categorical=categorical,
        )
        effects[name] = model_effects
        diagnostics = effect_diagnostics(model_effects)
        diagnostic_rows.append(
            {
                "cohort": name,
                "n_samples": len(metadata),
                "n_donors": metadata["donor"].nunique() if "donor" in metadata else np.nan,
                **diagnostics,
            }
        )
        all_reliability = split_half_reliability(
            expression,
            metadata,
            continuous=continuous,
            categorical=categorical,
            n_rep=args.split_half_repetitions,
        )
        ecm_genes = [
            gene for gene in MECHANISM_SETS["ECM remodelling"] if gene in expression.index
        ]
        ecm_reliability = split_half_reliability(
            expression.loc[ecm_genes],
            metadata,
            continuous=continuous,
            categorical=categorical,
            n_rep=args.split_half_repetitions,
        )
        reliability_rows.extend(
            [
                {"cohort": name, "gene_space": "all", **all_reliability},
                {"cohort": name, "gene_space": "ECM", **ecm_reliability},
            ]
        )
        pd.DataFrame({"effect": model_effects}).to_csv(
            output / f"{name}_gene_effects.csv",
            index_label="gene",
        )

    pd.DataFrame(diagnostic_rows).to_csv(
        output / "cohort_effect_diagnostics.csv",
        index=False,
    )
    pd.DataFrame(reliability_rows).to_csv(
        output / "internal_split_half_reliability.csv",
        index=False,
    )

    strict_70362 = subsets["GSE70362_AF_I_IV"]
    strict_23130 = subsets["GSE23130_LCM_all"]
    ecm_set = MECHANISM_SETS["ECM remodelling"]
    ecm_genes_70362 = [
        gene for gene in ecm_set if gene in strict_70362[0].index
    ]
    ecm_genes_23130 = [
        gene for gene in ecm_set if gene in strict_23130[0].index
    ]

    donor_sensitivity = donor_effect_sensitivity(
        strict_70362[0],
        strict_70362[1],
        ecm_set,
        effects["GSE23130_LCM_all"],
        continuous=strict_70362[2],
        categorical=strict_70362[3],
        n_rep=args.donor_bootstrap,
    )
    donor_sensitivity.to_csv(output / "donor_effect_sensitivity.csv", index=False)
    donor_summary = (
        donor_sensitivity.groupby("mode")
        .agg(
            n_replicates=("replicate", "count"),
            fraction_up_median=("fraction_up", "median"),
            fraction_up_lower=("fraction_up", lambda values: values.quantile(0.025)),
            fraction_up_upper=("fraction_up", lambda values: values.quantile(0.975)),
            concordance_median=("gene_concordance", "median"),
            concordance_lower=("gene_concordance", lambda values: values.quantile(0.025)),
            concordance_upper=("gene_concordance", lambda values: values.quantile(0.975)),
            effect_rho_median=("effect_rho", "median"),
            effect_rho_lower=("effect_rho", lambda values: values.quantile(0.025)),
            effect_rho_upper=("effect_rho", lambda values: values.quantile(0.975)),
        )
        .reset_index()
    )
    donor_summary.to_csv(output / "donor_sensitivity_summary.csv", index=False)

    cross_half_70362 = cross_half_concordance(
        strict_70362[0],
        strict_70362[1],
        ecm_set,
        continuous=strict_70362[2],
        categorical=strict_70362[3],
        group_column="donor",
        n_rep=args.donor_bootstrap,
    )
    cross_half_23130 = cross_half_concordance(
        strict_23130[0],
        strict_23130[1],
        ecm_set,
        continuous=strict_23130[2],
        categorical=strict_23130[3],
        n_rep=args.donor_bootstrap,
    )
    cross_half_70362.to_csv(
        output / "positive_control_cross_half_GSE70362.csv",
        index=False,
    )
    cross_half_23130.to_csv(
        output / "positive_control_cross_half_GSE23130.csv",
        index=False,
    )
    cross_half_summary = pd.DataFrame(
        [
            {
                "cohort": "GSE70362_AF_I_IV",
                "n_replicates": len(cross_half_70362),
                "concordance_median": cross_half_70362["gene_concordance"].median(),
                "concordance_lower": cross_half_70362["gene_concordance"].quantile(0.025),
                "concordance_upper": cross_half_70362["gene_concordance"].quantile(0.975),
                "effect_rho_median": cross_half_70362["effect_rho"].median(),
            },
            {
                "cohort": "GSE23130_LCM_all",
                "n_replicates": len(cross_half_23130),
                "concordance_median": cross_half_23130["gene_concordance"].median(),
                "concordance_lower": cross_half_23130["gene_concordance"].quantile(0.025),
                "concordance_upper": cross_half_23130["gene_concordance"].quantile(0.975),
                "effect_rho_median": cross_half_23130["effect_rho"].median(),
            },
        ]
    )
    cross_half_summary.to_csv(
        output / "positive_control_cross_half_summary.csv",
        index=False,
    )

    donor_ecm_reliability = split_half_reliability(
        strict_70362[0].loc[ecm_genes_70362],
        strict_70362[1],
        continuous=strict_70362[2],
        categorical=strict_70362[3],
        n_rep=args.split_half_repetitions,
        group_column="donor",
    )
    pd.DataFrame([{"gene_space": "ECM", **donor_ecm_reliability}]).to_csv(
        output / "donor_stratified_split_half.csv",
        index=False,
    )

    effective_genes = pd.DataFrame(
        [
            {
                "cohort": "GSE70362_AF_I_IV",
                "gene_space": "ECM",
                "effective_genes": effective_gene_number(
                    strict_70362[0].loc[ecm_genes_70362]
                ),
            },
            {
                "cohort": "GSE23130_LCM_all",
                "gene_space": "ECM",
                "effective_genes": effective_gene_number(
                    strict_23130[0].loc[ecm_genes_23130]
                ),
            },
        ]
    )
    effective_genes.to_csv(output / "effective_gene_number.csv", index=False)

    strict_effects_a = effects["GSE70362_AF_I_IV"]
    strict_effects_b = effects["GSE23130_LCM_all"]
    shared_ecm = [
        gene
        for gene in ecm_set
        if gene in strict_effects_a.index and gene in strict_effects_b.index
    ]
    observed_ecm_rho = spearman_correlation(
        strict_effects_a.reindex(shared_ecm),
        strict_effects_b.reindex(shared_ecm),
    )
    reliability_frame = pd.DataFrame(reliability_rows)
    split_a = float(
        reliability_frame[
            reliability_frame["cohort"].eq("GSE70362_AF_I_IV")
            & reliability_frame["gene_space"].eq("ECM")
        ]["median_spearman"].iloc[0]
    )
    split_b = float(
        reliability_frame[
            reliability_frame["cohort"].eq("GSE23130_LCM_all")
            & reliability_frame["gene_space"].eq("ECM")
        ]["median_spearman"].iloc[0]
    )
    full_reliability_a = spearman_brown(split_a)
    full_reliability_b = spearman_brown(split_b)
    attenuation_rows = []
    for true_correlation in (0.0, 0.2, 0.4, 0.6, 0.8):
        simulated = simulate_sign_concordance(
            true_correlation=true_correlation,
            reliability_a=full_reliability_a,
            reliability_b=full_reliability_b,
            n_genes=len(shared_ecm),
            n_rep=5000,
            seed=2026,
        )
        attenuation_rows.append(
            {
                "true_correlation": true_correlation,
                **simulated,
            }
        )
    attenuation = pd.DataFrame(attenuation_rows)
    attenuation["observed_ecm_sign_concordance"] = float(
        sign_concordance(
            strict_effects_a.reindex(shared_ecm),
            strict_effects_b.reindex(shared_ecm),
        )["fraction"]
    )
    attenuation["observed_ecm_effect_rho"] = observed_ecm_rho
    attenuation["full_reliability_GSE70362"] = full_reliability_a
    attenuation["full_reliability_GSE23130"] = full_reliability_b
    attenuation["disattenuated_effect_rho"] = disattenuate_correlation(
        observed_ecm_rho,
        full_reliability_a,
        full_reliability_b,
    )
    attenuation.to_csv(output / "attenuation_simulation.csv", index=False)

    weighted_primary = weighted_sign_concordance(
        strict_effects_a.reindex(shared_ecm),
        strict_effects_b.reindex(shared_ecm),
    )
    pd.DataFrame([{"module": "ECM remodelling", **weighted_primary}]).to_csv(
        output / "primary_weighted_concordance.csv",
        index=False,
    )

    module_scores = pd.DataFrame(
        [
            {
                "cohort": "GSE70362_AF_I_IV",
                **module_score_slope(
                    strict_70362[0],
                    strict_70362[1],
                    ecm_set,
                    continuous=strict_70362[2],
                    categorical=strict_70362[3],
                ),
            },
            {
                "cohort": "GSE23130_LCM_all",
                **module_score_slope(
                    strict_23130[0],
                    strict_23130[1],
                    ecm_set,
                    continuous=strict_23130[2],
                    categorical=strict_23130[3],
                ),
            },
        ]
    )
    module_scores.to_csv(output / "primary_module_score_slopes.csv", index=False)

    effective_n_min = int(
        min(
            effective_genes["effective_genes"].to_numpy(dtype=float)
        )
    )
    power_calibration = sign_concordance_power(
        true_correlations=(0.0, 0.2, 0.4, 0.6),
        reliability_a=full_reliability_a,
        reliability_b=full_reliability_b,
        n_genes=len(shared_ecm),
        effective_n_genes=effective_n_min,
        n_rep=5000,
        alpha=0.05,
        seed=2026,
    )
    power_calibration.to_csv(output / "power_calibration.csv", index=False)

    legacy = _primary_comparison(
        effects["GSE70362_AF_all"],
        effects["GSE23130_all"],
        "all available samples, tissue-strict but confounded",
    )
    strict = _primary_comparison(
        effects["GSE70362_AF_I_IV"],
        effects["GSE23130_LCM_all"],
        "grade I-IV, annulus fibrosus, LCM-only, adjusted",
    )
    strict_grade_only = _primary_comparison(
        effects["GSE70362_AF_I_IV_grade_only"],
        effects["GSE23130_LCM_grade_only"],
        "grade I-IV, annulus fibrosus, LCM-only, grade only",
    )
    pd.DataFrame([legacy, strict, strict_grade_only]).to_csv(
        output / "primary_comparison_summary.csv",
        index=False,
    )

    module_legacy = paired_module_audit(
        effects["GSE70362_AF_all"],
        effects["GSE23130_all"],
        MECHANISM_SETS,
    )
    module_legacy.insert(0, "comparison", "all available samples")
    module_strict = paired_module_audit(
        effects["GSE70362_AF_I_IV"],
        effects["GSE23130_LCM_all"],
        MECHANISM_SETS,
    )
    module_strict.insert(0, "comparison", "grade I-IV LCM-only")
    module_audit = pd.concat([module_legacy, module_strict], ignore_index=True)
    module_audit.to_csv(output / "curated_module_audit.csv", index=False)

    msigdb_sets = read_msigdb_symbol_sets(
        root,
        collection_names=(
            "h.all.v2024.1.Hs.entrez.gmt",
            "c2.cp.kegg_legacy.v2024.1.Hs.entrez.gmt",
            "c2.cp.reactome.v2024.1.Hs.entrez.gmt",
        ),
    )
    msigdb_audit = paired_module_audit(
        effects["GSE70362_AF_I_IV"],
        effects["GSE23130_LCM_all"],
        msigdb_sets,
        min_genes=10,
    )
    msigdb_audit = add_size_matched_concordance_p(
        msigdb_audit,
        effects["GSE70362_AF_I_IV"],
        effects["GSE23130_LCM_all"],
        n_perm=args.concordance_permutations,
    )
    msigdb_audit["gene_level_replicated"] = (
        msigdb_audit["gene_level_replicated"]
        & msigdb_audit["concordance_empirical_p_greater"].lt(0.05)
    )
    permutation_sets = MECHANISM_SETS
    permutation_genes = sorted(set().union(*permutation_sets.values()))
    permutation_expression_70362 = strict_70362[0].loc[
        [gene for gene in permutation_genes if gene in strict_70362[0].index]
    ]
    permutation_expression_23130 = strict_23130[0].loc[
        [gene for gene in permutation_genes if gene in strict_23130[0].index]
    ]
    permutation_methods = ("stratified", "freedman_lane", "rotation")
    permutation_a: dict[str, pd.Series] = {}
    permutation_b: dict[str, pd.Series] = {}
    for method_index, method in enumerate(permutation_methods):
        frame_a = permutation_module_directions(
            permutation_expression_70362,
            strict_70362[1],
            permutation_sets,
            continuous=strict_70362[2],
            categorical=strict_70362[3],
            n_perm=args.phenotype_permutations,
            seed=2026 + method_index,
            method=method,
        )
        frame_b = permutation_module_directions(
            permutation_expression_23130,
            strict_23130[1],
            permutation_sets,
            continuous=strict_23130[2],
            categorical=strict_23130[3],
            n_perm=args.phenotype_permutations,
            seed=2030 + method_index,
            method=method,
        )
        frame_a.to_csv(
            output / f"module_direction_permutation_{method}_GSE70362.csv",
            index=False,
        )
        frame_b.to_csv(
            output / f"module_direction_permutation_{method}_GSE23130.csv",
            index=False,
        )
        permutation_a[method] = frame_a.set_index("module")["p_two_sided"]
        permutation_b[method] = frame_b.set_index("module")["p_two_sided"]
    conservative_a = pd.concat(permutation_a, axis=1).max(axis=1)
    conservative_b = pd.concat(permutation_b, axis=1).max(axis=1)
    perm_a = conservative_a.rename("direction_p_gse70362").reset_index()
    perm_b = conservative_b.rename("direction_p_gse23130").reset_index()
    perm_a.to_csv(
        output / "module_direction_permutation_conservative_GSE70362.csv",
        index=False,
    )
    perm_b.to_csv(
        output / "module_direction_permutation_conservative_GSE23130.csv",
        index=False,
    )
    msigdb_audit = msigdb_audit.merge(
        perm_a[["module", "direction_p_gse70362"]],
        on="module",
        how="left",
    ).merge(
        perm_b[["module", "direction_p_gse23130"]],
        on="module",
        how="left",
    )
    msigdb_audit["direction_q_gse70362"] = benjamini_hochberg(
        msigdb_audit["direction_p_gse70362"].to_numpy()
    )
    msigdb_audit["direction_q_gse23130"] = benjamini_hochberg(
        msigdb_audit["direction_p_gse23130"].to_numpy()
    )
    msigdb_audit["direction_q_both"] = np.maximum(
        msigdb_audit["direction_q_gse70362"],
        msigdb_audit["direction_q_gse23130"],
    )
    msigdb_audit["direction_exact_q_gse70362"] = benjamini_hochberg(
        msigdb_audit["cohort_a_sign_p_two_sided"].to_numpy()
    )
    msigdb_audit["direction_exact_q_gse23130"] = benjamini_hochberg(
        msigdb_audit["cohort_b_sign_p_two_sided"].to_numpy()
    )
    msigdb_audit["direction_exact_q_both"] = np.maximum(
        msigdb_audit["direction_exact_q_gse70362"],
        msigdb_audit["direction_exact_q_gse23130"],
    )
    msigdb_audit["concordance_exact_q"] = benjamini_hochberg(
        msigdb_audit["gene_concordance_p_two_sided"].to_numpy()
    )
    msigdb_audit["replicated_fdr"] = (
        msigdb_audit["same_direction"]
        & msigdb_audit["direction_exact_q_both"].lt(0.05)
        & msigdb_audit["concordance_exact_q"].lt(0.05)
    )
    msigdb_audit.insert(0, "collection_rank", np.arange(1, len(msigdb_audit) + 1))
    msigdb_audit.to_csv(output / "msigdb_module_audit.csv", index=False)

    primary_expression_matched = expression_matched_concordance_p(
        effects["GSE70362_AF_I_IV"],
        effects["GSE23130_LCM_all"],
        strict_70362[0],
        strict_23130[0],
        ecm_set,
        n_perm=args.concordance_permutations,
    )
    pd.DataFrame(
        [{"module": "ECM remodelling", **primary_expression_matched}]
    ).to_csv(output / "primary_expression_matched_null.csv", index=False)

    confound_tables = {
        "GSE70362_tissue_by_batch": pd.crosstab(
            metadata_70362["tissue"],
            metadata_70362["batch"],
        ),
        "GSE70362_AF_grade_by_batch": pd.crosstab(
            metadata_70362.loc[af_i_iv, "grade"],
            metadata_70362.loc[af_i_iv, "batch"],
        ),
        "GSE23130_grade_by_method": pd.crosstab(
            metadata_23130["grade"],
            metadata_23130["method"],
        ),
        "GSE23130_LCM_grade_by_source": pd.crosstab(
            metadata_23130.loc[lcm_all, "grade"],
            metadata_23130.loc[lcm_all, "source"],
        ),
    }
    for name, table in confound_tables.items():
        table.to_csv(output / f"confound_{name}.csv", index_label="stratum")

    pairwise_effects = pd.read_csv(
        root / "ldh_pipeline/data/results/reproducibility/full_effects.csv",
        index_col=0,
    )
    pairwise_metadata = pd.DataFrame(
        [
            {
                "cohort": "GSE70362",
                "compartment": "tissue",
                "tissue": "AF_NP",
                "endpoint_class": "grade",
            },
            {
                "cohort": "GSE23130",
                "compartment": "tissue",
                "tissue": "AF",
                "endpoint_class": "grade",
            },
            {
                "cohort": "GSE186542",
                "compartment": "tissue",
                "tissue": "NP",
                "endpoint_class": "case_control",
            },
            {
                "cohort": "GSE167199",
                "compartment": "tissue",
                "tissue": "NP",
                "endpoint_class": "case_control",
            },
            {
                "cohort": "GSE146904",
                "compartment": "tissue",
                "tissue": "NP",
                "endpoint_class": "clinical_context",
            },
            {
                "cohort": "GSE207176",
                "compartment": "tissue",
                "tissue": "NP_cells",
                "endpoint_class": "case_control",
            },
        ]
    )
    pairwise = pairwise_concordance(pairwise_effects, pairwise_metadata)
    pairwise["comparability_tier"] = np.select(
        [
            pairwise["same_tissue"] & pairwise["same_endpoint_class"],
            pairwise["same_compartment"] & pairwise["same_endpoint_class"],
            pairwise["same_compartment"] | pairwise["same_endpoint_class"],
        ],
        [1, 2, 3],
        default=4,
    )
    pairwise.to_csv(output / "tissue_pairwise_concordance.csv", index=False)
    pairwise_exact = pairwise[pairwise["comparability_tier"].eq(1)].copy()
    pairwise_compartment = pairwise[pairwise["comparability_tier"].eq(2)].copy()
    pairwise_context = pairwise[pairwise["comparability_tier"].gt(2)].copy()
    pairwise_exact.to_csv(
        output / "tissue_pairwise_concordance_exact.csv",
        index=False,
    )
    pairwise_compartment.to_csv(
        output / "tissue_pairwise_concordance_compartment_matched.csv",
        index=False,
    )
    pairwise_context.to_csv(
        output / "tissue_pairwise_concordance_context.csv",
        index=False,
    )

    significant_one_sided = msigdb_audit[
        (
            msigdb_audit["significant_in_cohort_a"]
            != msigdb_audit["significant_in_cohort_b"]
        )
    ]
    significant_both = msigdb_audit[
        msigdb_audit["significant_in_cohort_a"]
        & msigdb_audit["significant_in_cohort_b"]
    ]
    discordant_significant = msigdb_audit[
        msigdb_audit["significant_in_cohort_a"]
        & msigdb_audit["significant_in_cohort_b"]
        & ~msigdb_audit["same_direction"]
    ]
    replicated = msigdb_audit[msigdb_audit["gene_level_replicated"]]
    replicated_fdr = msigdb_audit[msigdb_audit["replicated_fdr"]]
    donor_summary_records = donor_summary.to_dict(orient="records")
    attenuation_record = attenuation.iloc[0].to_dict()
    summary = {
        "cohorts": {
            "GSE70362_AF_all": int(len(subsets["GSE70362_AF_all"][1])),
            "GSE70362_AF_I_IV": int(len(subsets["GSE70362_AF_I_IV"][1])),
            "GSE23130_all": int(len(subsets["GSE23130_all"][1])),
            "GSE23130_LCM_all": int(len(subsets["GSE23130_LCM_all"][1])),
        },
        "legacy": legacy,
        "strict": strict,
        "strict_grade_only": strict_grade_only,
        "msigdb": {
            "n_modules_tested": int(len(msigdb_audit)),
            "n_significant_one_sided": int(len(significant_one_sided)),
            "n_significant_both": int(len(significant_both)),
            "n_discordant_significant": int(len(discordant_significant)),
            "n_gene_level_replicated": int(len(replicated)),
            "n_replicated_fdr": int(len(replicated_fdr)),
            "median_gene_concordance": float(msigdb_audit["gene_concordance"].median()),
            "phenotype_permutations": int(args.phenotype_permutations),
            "concordance_permutations": int(args.concordance_permutations),
            "permutation_methods": list(permutation_methods),
        },
        "donor_sensitivity": donor_summary_records,
        "effective_gene_number": effective_genes.to_dict(orient="records"),
        "primary_expression_matched_null": primary_expression_matched,
        "primary_weighted_concordance": weighted_primary,
        "primary_module_score_slopes": module_scores.to_dict(orient="records"),
        "cross_half_positive_control": cross_half_summary.to_dict(
            orient="records"
        ),
        "power_calibration": power_calibration.to_dict(orient="records"),
        "attenuation_example": attenuation_record,
        "pairwise_tissue": {
            "n_pairs": int(len(pairwise)),
            "median_gene_concordance": float(pairwise["gene_concordance"].median()),
            "max_gene_concordance": float(pairwise["gene_concordance"].max()),
            "min_gene_concordance": float(pairwise["gene_concordance"].min()),
        },
        "pairwise_tissue_exact": {
            "n_pairs": int(len(pairwise_exact)),
            "median_gene_concordance": float(
                pairwise_exact["gene_concordance"].median()
            ),
            "max_gene_concordance": float(
                pairwise_exact["gene_concordance"].max()
            ),
            "min_gene_concordance": float(
                pairwise_exact["gene_concordance"].min()
            ),
        },
        "pairwise_tissue_compartment_matched": {
            "n_pairs": int(len(pairwise_compartment)),
            "median_gene_concordance": float(
                pairwise_compartment["gene_concordance"].median()
            ),
            "max_gene_concordance": float(
                pairwise_compartment["gene_concordance"].max()
            ),
            "min_gene_concordance": float(
                pairwise_compartment["gene_concordance"].min()
            ),
        },
    }
    (output / "audit_summary.json").write_text(
        json.dumps(summary, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )
    input_paths = {
        "GSE70362_series_matrix": root
        / "ldh_pipeline/data/raw/GSE70362/GSE70362_series_matrix.txt.gz",
        "GSE23130_series_matrix": root
        / "ldh_pipeline/data/raw/GSE23130/GSE23130_series_matrix.txt.gz",
        "GSE23130_platform_annotation": root
        / "ldh_pipeline/data/raw/GSE23130/GPL1352.annot.gz",
        "human_gene_info": root
        / "ldh_pipeline/data/raw/annotation/Homo_sapiens.gene_info.gz",
        "hallmark": root
        / "ldh_pipeline/data/raw/msigdb/h.all.v2024.1.Hs.entrez.gmt",
        "kegg": root
        / "ldh_pipeline/data/raw/msigdb/c2.cp.kegg_legacy.v2024.1.Hs.entrez.gmt",
        "reactome": root
        / "ldh_pipeline/data/raw/msigdb/c2.cp.reactome.v2024.1.Hs.entrez.gmt",
        "legacy_tissue_effects": root
        / "ldh_pipeline/data/results/reproducibility/full_effects.csv",
    }
    provenance = {
        "generated_utc": datetime.now(timezone.utc).isoformat(),
        "python": platform.python_version(),
        "numpy": np.__version__,
        "pandas": pd.__version__,
        "parameters": {
            "phenotype_permutations": args.phenotype_permutations,
            "concordance_permutations": args.concordance_permutations,
            "donor_bootstrap": args.donor_bootstrap,
            "split_half_repetitions": args.split_half_repetitions,
        },
        "inputs": {
            name: {"path": str(path.relative_to(root)), "sha256": _sha256(path)}
            for name, path in input_paths.items()
        },
        "code": {
            "run_audit.py": _sha256(Path(__file__).resolve()),
            "audit.py": _sha256(Path(__file__).resolve().parent / "ivd_audit/audit.py"),
            "core.py": _sha256(Path(__file__).resolve().parent / "ivd_audit/core.py"),
        },
    }
    (output / "provenance.json").write_text(
        json.dumps(provenance, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )
    reliability_frame = pd.DataFrame(reliability_rows)
    draw_workflow(figure_output / "fig1_workflow")
    draw_ecm_paradox(
        pd.DataFrame([legacy, strict]),
        reliability_frame,
        figure_output / "fig2_ecm_paradox",
    )
    draw_msigdb_audit(
        msigdb_audit,
        summary["msigdb"],
        figure_output / "fig3_msigdb_audit",
    )
    draw_pairwise_concordance(
        pairwise,
        figure_output / "fig4_pairwise_concordance",
    )
    draw_sensitivity(
        donor_summary,
        attenuation,
        figure_output / "fig5_sensitivity",
    )
    draw_calibration(
        cross_half_summary,
        power_calibration,
        pd.Series(weighted_primary),
        figure_output / "fig6_calibration",
    )
    if not args.skip_manuscript:
        write_manuscript(Path(__file__).resolve().parent)
    print(json.dumps(summary, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
