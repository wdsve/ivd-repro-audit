"""Sensitivity of FDR conclusions to module-family and overlap structure."""

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

from ivd_audit.audit import read_msigdb_symbol_sets  # noqa: E402
from ivd_audit.core import benjamini_hochberg  # noqa: E402


COLLECTIONS = {
    "Hallmark": "HALLMARK_",
    "KEGG": "KEGG_",
    "Reactome": "REACTOME_",
}


def _family_rows(frame: pd.DataFrame, mapping: str) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    for collection, prefix in COLLECTIONS.items():
        subset = frame[frame["module"].str.startswith(prefix)].copy()
        subset["direction_q_a"] = benjamini_hochberg(
            subset["cohort_a_sign_p_two_sided"].to_numpy()
        )
        subset["direction_q_b"] = benjamini_hochberg(
            subset["cohort_b_sign_p_two_sided"].to_numpy()
        )
        subset["direction_q_both"] = subset[
            ["direction_q_a", "direction_q_b"]
        ].max(axis=1)
        subset["concordance_q"] = benjamini_hochberg(
            subset["gene_concordance_p_two_sided"].to_numpy()
        )
        nominal = (
            subset["same_direction"]
            & subset["significant_in_cohort_a"]
            & subset["significant_in_cohort_b"]
            & subset["gene_level_replicated"]
        )
        strict = (
            subset["same_direction"]
            & subset["direction_q_both"].lt(0.05)
            & subset["concordance_q"].lt(0.05)
        )
        rows.append(
            {
                "mapping": mapping,
                "collection": collection,
                "modules": int(len(subset)),
                "nominal_gene_level": int(nominal.sum()),
                "local_fdr": int(strict.sum()),
            }
        )
    return rows


def _overlap(root: Path) -> dict[str, object]:
    sets = read_msigdb_symbol_sets(
        root,
        collection_names=(
            "h.all.v2024.1.Hs.entrez.gmt",
            "c2.cp.kegg_legacy.v2024.1.Hs.entrez.gmt",
            "c2.cp.reactome.v2024.1.Hs.entrez.gmt",
        ),
    )
    members: list[set[str]] = []
    for genes in sets.values():
        normalized = {gene.upper() for gene in genes}
        if len(normalized) >= 10:
            members.append(normalized)

    jaccard: list[float] = []
    for index, first in enumerate(members):
        for second in members[index + 1 :]:
            intersection = len(first & second)
            if intersection:
                jaccard.append(intersection / len(first | second))
    values = np.asarray(jaccard)
    return {
        "nonzero_jaccard_pairs": int(len(values)),
        "jaccard_median": float(np.median(values)),
        "jaccard_p90": float(np.quantile(values, 0.90)),
        "jaccard_p99": float(np.quantile(values, 0.99)),
        "jaccard_max": float(values.max()),
        "jaccard_gt_0_5": int((values > 0.5).sum()),
        "jaccard_gt_0_8": int((values > 0.8).sum()),
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

    rows: list[dict[str, object]] = []
    rows.extend(
        _family_rows(
            pd.read_csv(output / "msigdb_module_audit.csv"),
            "primary",
        )
    )
    rows.extend(
        _family_rows(
            pd.read_csv(output / "gene_identity_alias_module_audit.csv"),
            "alias-aware",
        )
    )
    frame = pd.DataFrame(rows)
    frame.to_csv(output / "module_family_sensitivity.csv", index=False)
    summary = {
        "families": rows,
        "overlap": _overlap(root),
    }
    (output / "module_family_sensitivity_summary.json").write_text(
        json.dumps(summary, indent=2),
        encoding="utf-8",
    )
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
