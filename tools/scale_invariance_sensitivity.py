"""Rank-trend sensitivity to monotone cross-platform scale differences."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd

PROJECT = Path(__file__).resolve().parents[1]
if str(PROJECT) not in sys.path:
    sys.path.insert(0, str(PROJECT))

from ivd_audit.audit import (  # noqa: E402
    MECHANISM_SETS,
    prepare_gse23130,
    prepare_gse70362,
)
from ivd_audit.core import sign_concordance, summarise_gene_set  # noqa: E402


def _rank_effects(
    expression: pd.DataFrame,
    grade: pd.Series,
) -> pd.Series:
    aligned_grade = grade.reindex(expression.columns).astype(float)
    valid_samples = aligned_grade.notna().to_numpy()
    values = expression.loc[:, valid_samples].astype(float)
    grade_values = aligned_grade.loc[valid_samples].rank().to_numpy()
    gene_ranks = values.rank(axis=1)
    centered_genes = gene_ranks.sub(gene_ranks.mean(axis=1), axis=0)
    centered_grade = grade_values - grade_values.mean()
    numerator = centered_genes.to_numpy() @ centered_grade
    denominator = np.sqrt(
        np.square(centered_genes.to_numpy()).sum(axis=1)
        * np.square(centered_grade).sum()
    )
    return pd.Series(
        np.divide(
            numerator,
            denominator,
            out=np.full(len(expression), np.nan),
            where=denominator != 0,
        ),
        index=expression.index,
    )


def _stratified_rank_effects(
    expression: pd.DataFrame,
    metadata: pd.DataFrame,
    stratum: str,
) -> pd.Series:
    estimates: list[pd.Series] = []
    for positions in metadata.groupby(stratum, sort=True).groups.values():
        index = list(positions)
        if len(index) < 4 or metadata.loc[index, "grade"].nunique() < 3:
            continue
        subset = expression.iloc[:, index]
        grade = pd.Series(
            metadata.loc[index, "grade"].to_numpy(),
            index=subset.columns,
        )
        estimates.append(_rank_effects(subset, grade))
    if not estimates:
        return pd.Series(np.nan, index=expression.index)
    return pd.concat(estimates, axis=1).mean(axis=1)


def _summary(
    effects_70362: pd.Series,
    effects_23130: pd.Series,
) -> dict[str, object]:
    ecm = MECHANISM_SETS["ECM remodelling"]
    summary_70362 = summarise_gene_set(effects_70362, ecm)
    summary_23130 = summarise_gene_set(effects_23130, ecm)
    shared = [
        gene
        for gene in ecm
        if gene in effects_70362.index and gene in effects_23130.index
    ]
    concordance = sign_concordance(
        effects_70362.reindex(shared),
        effects_23130.reindex(shared),
    )
    return {
        "shared_ecm_genes": len(shared),
        "gse70362_fraction_up": summary_70362["fraction_up"],
        "gse70362_sign_p": summary_70362["sign_p_greater"],
        "gse23130_fraction_up": summary_23130["fraction_up"],
        "gse23130_sign_p": summary_23130["sign_p_greater"],
        "ecm_concordance": concordance["fraction"],
        "ecm_concordance_p": concordance["binomial_p_greater"],
        "ecm_concordance_p_less": concordance["binomial_p_less"],
        "ecm_concordance_p_two_sided": concordance["binomial_p_two_sided"],
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--project-root",
        type=Path,
        default=Path(__file__).resolve().parents[2],
    )
    args = parser.parse_args()
    root = args.project_root.resolve()
    output = PROJECT / "results"
    output.mkdir(parents=True, exist_ok=True)

    expression_70362, metadata_70362 = prepare_gse70362(root)
    expression_23130, metadata_23130 = prepare_gse23130(root)
    af = (
        metadata_70362["tissue"].eq("Annulus fibrosus")
        & metadata_70362["grade"].between(1, 4)
    )
    lcm = metadata_23130["method"].eq("LCM")
    expression_70362 = expression_70362.loc[:, af]
    metadata_70362 = metadata_70362.loc[af].reset_index(drop=True)
    expression_23130 = expression_23130.loc[:, lcm]
    metadata_23130 = metadata_23130.loc[lcm].reset_index(drop=True)

    unadjusted_70362 = _rank_effects(
        expression_70362,
        pd.Series(
            metadata_70362["grade"].to_numpy(),
            index=expression_70362.columns,
        ),
    )
    unadjusted_23130 = _rank_effects(
        expression_23130,
        pd.Series(
            metadata_23130["grade"].to_numpy(),
            index=expression_23130.columns,
        ),
    )
    stratified_70362 = _stratified_rank_effects(
        expression_70362,
        metadata_70362,
        "batch",
    )
    stratified_23130 = _stratified_rank_effects(
        expression_23130,
        metadata_23130,
        "source",
    )

    rows = [
        {"method": "unadjusted_spearman", **_summary(unadjusted_70362, unadjusted_23130)},
        {
            "method": "stratum_adjusted_spearman",
            **_summary(stratified_70362, stratified_23130),
        },
    ]
    frame = pd.DataFrame(rows)
    frame.to_csv(output / "scale_invariance_sensitivity.csv", index=False)
    summary = frame.set_index("method").to_dict(orient="index")
    (output / "scale_invariance_sensitivity_summary.json").write_text(
        json.dumps(summary, indent=2),
        encoding="utf-8",
    )
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
