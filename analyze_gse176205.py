#!/usr/bin/env python
"""Analyze GSE176205 as a directional NP (not AF severity) validation set."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import numpy as np
import pandas as pd

from ivd_audit.audit import (
    MECHANISM_SETS,
    effect_diagnostics,
    fit_effect_model,
    prepare_gse70362,
)
from ivd_audit.core import (
    collapse_by_symbols,
    ols_effects,
    sign_concordance,
    spearman_correlation,
    summarise_gene_set,
)
from ivd_audit.data import read_series_matrix


def prepare_gse176205(
    count_path: Path,
    metadata_path: Path,
) -> tuple[pd.DataFrame, pd.DataFrame]:
    counts = pd.read_csv(count_path, sep="\t", low_memory=False)
    count_columns = [column for column in counts.columns if column.endswith("_count")]
    sample_names = [column.removesuffix("_count") for column in count_columns]
    matrix = counts[count_columns].apply(pd.to_numeric, errors="coerce")
    matrix.columns = sample_names
    cpm = matrix / matrix.sum(axis=0, skipna=True) * 1e6
    log_cpm = np.log2(cpm + 1)
    symbols = counts["gene_short_name"]
    expression = collapse_by_symbols(log_cpm, symbols)

    _, metadata = read_series_matrix(metadata_path)
    metadata["sample"] = metadata["title"]
    metadata["group"] = metadata["classification"].str.strip().str.lower()
    metadata = metadata.set_index("sample")
    missing = sorted(set(expression.columns) - set(metadata.index))
    if missing:
        raise ValueError(f"missing metadata for samples: {missing}")
    metadata = metadata.loc[expression.columns]
    return expression, metadata


def group_effect(expression: pd.DataFrame, metadata: pd.DataFrame) -> pd.Series:
    case = metadata["group"].eq("degeneration").astype(float).to_numpy()
    design = np.column_stack([np.ones(len(metadata)), case])
    effects = ols_effects(expression, design, coefficient=1)
    effects.name = "effect"
    return effects


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--project-root", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    args = parser.parse_args()
    args.output_dir.mkdir(parents=True, exist_ok=True)

    root = args.project_root.resolve()
    expression_176205, metadata_176205 = prepare_gse176205(
        root
        / "ldh_pipeline/data/raw/GSE176205/GSE176205_mRNA_Expression_Profiling_upload.txt.gz",
        root / "ldh_pipeline/data/raw/GSE176205/GSE176205_series_matrix.txt.gz",
    )
    effects_176205 = group_effect(expression_176205, metadata_176205)
    expression_176205_centered = expression_176205.sub(
        expression_176205.median(axis=0),
        axis=1,
    )
    effects_176205_centered = group_effect(
        expression_176205_centered,
        metadata_176205,
    )

    expression_70362, metadata_70362 = prepare_gse70362(root)
    np_mask = metadata_70362["tissue"].eq("Nucleus pulposus") & metadata_70362[
        "grade"
    ].between(1, 4)
    expression_70362_np = expression_70362.loc[:, np_mask]
    metadata_70362_np = metadata_70362.loc[np_mask].reset_index(drop=True)
    effects_70362_np = fit_effect_model(
        expression_70362_np,
        metadata_70362_np,
        continuous=["grade"],
        categorical=["batch"],
    )

    rows = []
    for module, genes in MECHANISM_SETS.items():
        summary_176205 = summarise_gene_set(effects_176205_centered, genes)
        summary_70362 = summarise_gene_set(effects_70362_np, genes)
        concordance = sign_concordance(
            effects_176205_centered.reindex(genes),
            effects_70362_np.reindex(genes),
        )
        rows.append(
            {
                "module": module,
                "n_genes": concordance["n"],
                "gse176205_centered_fraction_up": summary_176205["fraction_up"],
                "gse176205_centered_median_effect": summary_176205["median_effect"],
                "gse176205_centered_sign_p": summary_176205["sign_p_greater"],
                "gse70362_np_fraction_up": summary_70362["fraction_up"],
                "gse70362_np_median_effect": summary_70362["median_effect"],
                "gse70362_np_sign_p": summary_70362["sign_p_greater"],
                "gene_concordance": concordance["fraction"],
                "gene_concordance_p": concordance["binomial_p_greater"],
                "effect_rho": spearman_correlation(
                    effects_176205_centered.reindex(genes),
                    effects_70362_np.reindex(genes),
                ),
            }
        )
    modules = pd.DataFrame(rows).sort_values("gene_concordance", ascending=False)

    summary = {
        "cohorts": {
            "GSE176205": "NP, control vs degeneration, n=9 (3 vs 6)",
            "GSE70362_NP_I_IV": f"NP grade I-IV, n={len(metadata_70362_np)}",
        },
        "gse176205_diagnostics": effect_diagnostics(effects_176205),
        "gse176205_centered_diagnostics": effect_diagnostics(
            effects_176205_centered
        ),
        "gse70362_np_diagnostics": effect_diagnostics(effects_70362_np),
        "interpretation": (
            "Directional NP context only. This is not a third AF severity "
            "cohort and does not enter the primary replication gate."
        ),
    }

    effects_176205.rename("effect").to_csv(
        args.output_dir / "GSE176205_gene_effects.csv",
        index_label="gene",
    )
    effects_176205_centered.rename("effect").to_csv(
        args.output_dir / "GSE176205_centered_gene_effects.csv",
        index_label="gene",
    )
    effects_70362_np.rename("effect").to_csv(
        args.output_dir / "GSE70362_NP_I_IV_gene_effects.csv",
        index_label="gene",
    )
    modules.to_csv(
        args.output_dir / "GSE176205_NP_direction.csv",
        index=False,
    )
    (args.output_dir / "GSE176205_summary.json").write_text(
        json.dumps(summary, indent=2),
        encoding="utf-8",
    )
    print(json.dumps(summary, indent=2))
    print("\nModule comparison:")
    print(modules.to_string(index=False))


if __name__ == "__main__":
    main()
