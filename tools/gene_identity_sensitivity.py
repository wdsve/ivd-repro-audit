"""Quantify sensitivity to canonical symbols versus historical gene aliases."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import pandas as pd

PROJECT = Path(__file__).resolve().parents[1]
if str(PROJECT) not in sys.path:
    sys.path.insert(0, str(PROJECT))

from ivd_audit.audit import (  # noqa: E402
    GRADE_MAP,
    MECHANISM_SETS,
    fit_effect_model,
    paired_module_audit,
    prepare_gse70362,
    read_affymetrix_annotation,
    read_msigdb_symbol_sets,
    read_series_matrix,
)
from ivd_audit.core import (  # noqa: E402
    benjamini_hochberg,
    collapse_by_symbols,
    sign_concordance,
)


def _alias_map(gene_info_path: Path) -> tuple[dict[str, str], set[str]]:
    frame = pd.read_csv(
        gene_info_path,
        sep="\t",
        dtype=str,
        low_memory=False,
    ).fillna("")
    mapping: dict[str, str] = {}
    conflicts: set[str] = set()
    for _, row in frame.iterrows():
        canonical = str(row["Symbol"]).strip()
        if not canonical:
            continue
        values = [canonical]
        values.extend(
            value.strip()
            for value in str(row.get("Synonyms", "")).split("|")
            if value.strip()
        )
        authority = str(row.get("Symbol_from_nomenclature_authority", "")).strip()
        if authority:
            values.append(authority)
        for value in values:
            key = value.upper()
            previous = mapping.get(key)
            if previous is not None and previous.upper() != canonical.upper():
                conflicts.add(key)
            else:
                mapping[key] = canonical
    for key in conflicts:
        mapping.pop(key, None)
    return mapping, conflicts


def _canonicalize(value: object, alias: dict[str, str]) -> str:
    text = str(value).strip()
    return alias.get(text.upper(), text.upper())


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

    annotation = read_affymetrix_annotation(
        root / "ldh_pipeline/data/raw/GSE23130/GPL1352.annot.gz"
    )
    alias, conflicts = _alias_map(
        root / "ldh_pipeline/data/raw/annotation/Homo_sapiens.gene_info.gz"
    )
    platform_symbols = {
        str(value).strip()
        for value in annotation["Gene symbol"].dropna()
        if str(value).strip() and str(value).strip() != "---"
    }
    exact = {value for value in platform_symbols if value.upper() in alias}
    exact_current = {
        value
        for value in platform_symbols
        if value.upper() == alias.get(value.upper(), "").upper()
    }
    alias_only = exact - exact_current
    unresolved = platform_symbols - exact

    expression_70362, metadata_70362 = prepare_gse70362(root)
    expression_23130, metadata_23130 = read_series_matrix(
        root / "ldh_pipeline/data/raw/GSE23130/GSE23130_series_matrix.txt.gz"
    )
    probe_to_symbol = dict(zip(annotation.iloc[:, 0], annotation["Gene symbol"]))
    raw_symbols = pd.Series(
        expression_23130.index,
        index=expression_23130.index,
    ).map(probe_to_symbol)
    canonical_symbols = raw_symbols.map(lambda value: _canonicalize(value, alias))
    expression_23130 = collapse_by_symbols(expression_23130, canonical_symbols)

    metadata_23130 = metadata_23130.rename(
        columns={
            "tissue_grade": "grade_label",
            "lcm_or_homogenization": "method",
            "tissue_source": "source",
        }
    )
    metadata_23130["grade"] = (
        metadata_23130["grade_label"].str.strip().map(GRADE_MAP)
    )
    metadata_23130["method"] = metadata_23130["method"].astype(str)
    metadata_23130["source"] = metadata_23130["source"].astype(str)

    af = (
        metadata_70362["tissue"].eq("Annulus fibrosus")
        & metadata_70362["grade"].between(1, 4)
    )
    lcm = metadata_23130["method"].eq("LCM")
    effects_70362 = fit_effect_model(
        expression_70362.loc[:, af],
        metadata_70362.loc[af].reset_index(drop=True),
        continuous=["grade"],
        categorical=["batch"],
    )
    effects_23130 = fit_effect_model(
        expression_23130.loc[:, lcm],
        metadata_23130.loc[lcm].reset_index(drop=True),
        continuous=["grade"],
        categorical=["source"],
    )

    sets = read_msigdb_symbol_sets(
        root,
        collection_names=(
            "h.all.v2024.1.Hs.entrez.gmt",
            "c2.cp.kegg_legacy.v2024.1.Hs.entrez.gmt",
            "c2.cp.reactome.v2024.1.Hs.entrez.gmt",
        ),
    )
    audit = paired_module_audit(
        effects_70362,
        effects_23130,
        sets,
        min_genes=10,
    )
    audit["direction_q_gse70362"] = benjamini_hochberg(
        audit["cohort_a_sign_p_two_sided"].to_numpy()
    )
    audit["direction_q_gse23130"] = benjamini_hochberg(
        audit["cohort_b_sign_p_two_sided"].to_numpy()
    )
    audit["direction_q_both"] = audit[
        ["direction_q_gse70362", "direction_q_gse23130"]
    ].max(axis=1)
    audit["concordance_q_two_sided"] = benjamini_hochberg(
        audit["gene_concordance_p_two_sided"].to_numpy()
    )
    audit["replicated_fdr"] = (
        audit["same_direction"]
        & audit["direction_q_both"].lt(0.05)
        & audit["concordance_q_two_sided"].lt(0.05)
    )
    audit.to_csv(output / "gene_identity_alias_module_audit.csv", index=False)

    ecm = MECHANISM_SETS["ECM remodelling"]
    shared_ecm = [
        gene
        for gene in ecm
        if gene in effects_70362.index and gene in effects_23130.index
    ]
    ecm_concordance = sign_concordance(
        effects_70362.reindex(shared_ecm),
        effects_23130.reindex(shared_ecm),
    )

    current_summary = json.loads(
        (output / "audit_summary.json").read_text(encoding="utf-8")
    )
    summary = {
        "platform_symbols": len(platform_symbols),
        "canonical_symbols": len(exact_current),
        "alias_only_symbols": len(alias_only),
        "unresolved_symbols": len(unresolved),
        "ambiguous_alias_keys_removed": len(conflicts),
        "current_modules_tested": int(
            current_summary["msigdb"]["n_modules_tested"]
        ),
        "alias_modules_tested": int(len(audit)),
        "current_significant_one_cohort": int(
            current_summary["msigdb"]["n_significant_one_sided"]
        ),
        "alias_significant_one_cohort": int(
            (audit["significant_in_cohort_a"] ^ audit["significant_in_cohort_b"]).sum()
        ),
        "current_significant_both": int(
            current_summary["msigdb"]["n_significant_both"]
        ),
        "alias_significant_both": int(
            (audit["significant_in_cohort_a"] & audit["significant_in_cohort_b"]).sum()
        ),
        "current_nominal_gene_level": int(
            current_summary["msigdb"]["n_gene_level_replicated"]
        ),
        "alias_nominal_gene_level": int(audit["gene_level_replicated"].sum()),
        "current_replicated_fdr": int(
            current_summary["msigdb"]["n_replicated_fdr"]
        ),
        "alias_replicated_fdr": int(audit["replicated_fdr"].sum()),
        "shared_ecm_genes": len(shared_ecm),
        "ecm_concordance": float(ecm_concordance["fraction"]),
    }
    (output / "gene_identity_sensitivity_summary.json").write_text(
        json.dumps(summary, indent=2),
        encoding="utf-8",
    )
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
