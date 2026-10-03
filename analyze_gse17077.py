#!/usr/bin/env python
"""Analyze GSE17077 as a paired senescence cell-state dataset."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import numpy as np
import pandas as pd

from ivd_audit.audit import MECHANISM_SETS, read_affymetrix_annotation
from ivd_audit.core import collapse_by_symbols, spearman_correlation, summarise_gene_set
from ivd_audit.data import read_series_matrix
from ivd_audit.senescence import derive_donor_id, paired_senescence_effects


GRADE_MAP = {
    "I": 1.0,
    "II": 2.0,
    "III": 3.0,
    "IV": 4.0,
    "V": 5.0,
}


def prepare_gse17077(
    series_matrix: Path,
    annotation_path: Path,
) -> tuple[pd.DataFrame, pd.DataFrame]:
    expression, metadata = read_series_matrix(series_matrix)
    annotation = read_affymetrix_annotation(annotation_path)
    probe_to_symbol = dict(zip(annotation.iloc[:, 0], annotation["Gene symbol"]))
    symbols = pd.Series(expression.index, index=expression.index).map(probe_to_symbol)
    expression = collapse_by_symbols(expression, symbols)

    metadata = metadata.rename(
        columns={
            "senescent or non-senescent": "status",
            "tissue grade": "grade_label",
        }
    )
    metadata["sample"] = metadata.index
    metadata["donor"] = metadata["title"].map(derive_donor_id)
    metadata["grade"] = metadata["grade_label"].str.strip().map(GRADE_MAP)
    return expression, metadata


def module_grade_associations(
    expression: pd.DataFrame,
    metadata: pd.DataFrame,
) -> pd.DataFrame:
    rows = []
    meta = metadata.copy()
    meta["donor"] = meta["title"].map(derive_donor_id)
    for module, genes in MECHANISM_SETS.items():
        selected = [gene for gene in genes if gene in expression.index]
        donor_scores = []
        donor_grades = []
        for donor, group in meta.groupby("donor", sort=True):
            senescent = group.index[group["status"].str.lower().eq("senescent")]
            non_senescent = group.index[
                group["status"].str.lower().eq("non-senescent")
            ]
            if len(senescent) != 1 or len(non_senescent) != 1:
                continue
            difference = (
                expression.loc[selected, senescent[0]]
                - expression.loc[selected, non_senescent[0]]
            )
            donor_scores.append(float(difference.mean()))
            donor_grades.append(float(group["grade"].iloc[0]))
        rho = (
            spearman_correlation(donor_scores, donor_grades)
            if len(donor_scores) >= 4
            else float("nan")
        )
        rows.append(
            {
                "module": module,
                "n_genes": len(selected),
                "n_donors": len(donor_scores),
                "median_donor_effect": float(np.median(donor_scores))
                if donor_scores
                else float("nan"),
                "grade_spearman": rho,
            }
        )
    return pd.DataFrame(rows)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--series-matrix", type=Path, required=True)
    parser.add_argument("--annotation", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    args = parser.parse_args()
    args.output_dir.mkdir(parents=True, exist_ok=True)

    expression, metadata = prepare_gse17077(
        args.series_matrix,
        args.annotation,
    )
    effects, donor_scores = paired_senescence_effects(expression, metadata)
    module_rows = []
    for module, genes in MECHANISM_SETS.items():
        summary = summarise_gene_set(effects, genes)
        summary["module"] = module
        module_rows.append(summary)
    modules = pd.DataFrame(module_rows)[
        [
            "module",
            "n_genes",
            "n_up",
            "fraction_up",
            "median_effect",
            "sign_p_greater",
        ]
    ].sort_values("sign_p_greater")
    grade_associations = module_grade_associations(expression, metadata)

    paired_metadata = metadata.copy()
    paired_metadata["paired_donor"] = paired_metadata["donor"].isin(donor_scores.index)
    paired_metadata["mean_paired_effect"] = paired_metadata["donor"].map(
        donor_scores.to_dict()
    )
    paired_metadata.to_csv(
        args.output_dir / "GSE17077_sample_metadata.csv",
        index=False,
    )
    effects.rename("senescent_minus_non_senescent").to_csv(
        args.output_dir / "GSE17077_paired_gene_effects.csv",
        index_label="gene",
    )
    modules.to_csv(
        args.output_dir / "GSE17077_module_direction.csv",
        index=False,
    )
    grade_associations.to_csv(
        args.output_dir / "GSE17077_module_grade_association.csv",
        index=False,
    )

    summary = {
        "n_samples": int(len(metadata)),
        "n_donors_total": int(metadata["donor"].nunique()),
        "n_paired_donors": int(len(donor_scores)),
        "grades": {
            str(grade): int(count)
            for grade, count in metadata["grade_label"].value_counts().items()
        },
        "global_fraction_positive": float((effects > 0).mean()),
        "global_median_effect": float(effects.median()),
        "paired_donor_mean_effect": {
            donor: float(value) for donor, value in donor_scores.items()
        },
    }
    (args.output_dir / "GSE17077_summary.json").write_text(
        json.dumps(summary, indent=2),
        encoding="utf-8",
    )
    print(json.dumps(summary, indent=2))
    print("\nModule direction:")
    print(modules.to_string(index=False))


if __name__ == "__main__":
    main()
