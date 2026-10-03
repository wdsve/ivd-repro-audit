"""Sensitivity of the primary ECM comparison to probe-to-symbol collapsing."""

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
    GRADE_MAP,
    MECHANISM_SETS,
    fit_effect_model,
    load_gene_info,
    read_affymetrix_annotation,
)
from ivd_audit.core import sign_concordance, summarise_gene_set  # noqa: E402
from ivd_audit.data import read_series_matrix  # noqa: E402


def _valid_probe_groups(
    expression: pd.DataFrame,
    symbols: pd.Series,
) -> pd.DataFrame:
    symbol_series = pd.Series(symbols, dtype="object").reindex(expression.index)
    valid = symbol_series.notna() & symbol_series.astype(str).str.strip().ne("")
    values = expression.loc[valid].copy()
    values["__symbol__"] = symbol_series.loc[valid].astype(str).to_numpy()
    return values


def collapse_probes(
    expression: pd.DataFrame,
    symbols: pd.Series,
    mode: str,
    *,
    rng: np.random.Generator | None = None,
) -> pd.DataFrame:
    values = _valid_probe_groups(expression, symbols)
    if mode == "highest_mean":
        values["__mean__"] = values.drop(columns="__symbol__").mean(
            axis=1, skipna=True
        )
        values = values.sort_values("__mean__", ascending=False, kind="mergesort")
        selected = values.drop_duplicates("__symbol__", keep="first")
        selected = selected.drop(columns="__mean__")
    elif mode == "first_probe":
        selected = values.drop_duplicates("__symbol__", keep="first")
    elif mode == "median_probe":
        matrix = values.drop(columns="__symbol__")
        grouped = matrix.groupby(values["__symbol__"], sort=False).median()
        grouped.index.name = "symbol"
        return grouped
    elif mode == "random_probe":
        if rng is None:
            raise ValueError("random_probe requires rng")
        order = rng.permutation(len(values))
        selected = values.iloc[order].drop_duplicates("__symbol__", keep="first")
    else:
        raise ValueError(f"unsupported collapse mode: {mode}")

    selected = selected.copy()
    selected.index = selected.pop("__symbol__").to_numpy()
    return selected


def _metadata_70362(metadata: pd.DataFrame) -> pd.DataFrame:
    metadata = metadata.rename(
        columns={
            "individual": "donor",
            "thompson grade": "grade_label",
            "tissue": "tissue",
            "batch": "batch",
        }
    )
    metadata["grade"] = metadata["grade_label"].str.strip().map(GRADE_MAP)
    metadata["batch"] = metadata["batch"].astype(str)
    return metadata


def _metadata_23130(metadata: pd.DataFrame) -> pd.DataFrame:
    metadata = metadata.rename(
        columns={
            "tissue_grade": "grade_label",
            "lcm_or_homogenization": "method",
            "tissue_source": "source",
        }
    )
    metadata["grade"] = metadata["grade_label"].str.strip().map(GRADE_MAP)
    metadata["method"] = metadata["method"].astype(str)
    metadata["source"] = metadata["source"].astype(str)
    return metadata


def _prepare_inputs(root: Path) -> dict[str, object]:
    expression_70362, metadata_70362 = read_series_matrix(
        root / "ldh_pipeline/data/raw/GSE70362/GSE70362_series_matrix.txt.gz"
    )
    entrez_to_symbol, _ = load_gene_info(
        root / "ldh_pipeline/data/raw/annotation/Homo_sapiens.gene_info.gz"
    )
    entrez = expression_70362.index.to_series().str.extract(r"^(\d+)", expand=False)
    symbols_70362 = entrez.map(entrez_to_symbol)
    metadata_70362 = _metadata_70362(metadata_70362)

    expression_23130, metadata_23130 = read_series_matrix(
        root / "ldh_pipeline/data/raw/GSE23130/GSE23130_series_matrix.txt.gz"
    )
    annotation = read_affymetrix_annotation(
        root / "ldh_pipeline/data/raw/GSE23130/GPL1352.annot.gz"
    )
    probe_to_symbol = dict(zip(annotation.iloc[:, 0], annotation["Gene symbol"]))
    symbols_23130 = pd.Series(
        expression_23130.index,
        index=expression_23130.index,
    ).map(probe_to_symbol)
    metadata_23130 = _metadata_23130(metadata_23130)

    return {
        "expression_70362": expression_70362,
        "symbols_70362": symbols_70362,
        "metadata_70362": metadata_70362,
        "expression_23130": expression_23130,
        "symbols_23130": symbols_23130,
        "metadata_23130": metadata_23130,
    }


def _primary_ecm(
    expression_70362: pd.DataFrame,
    metadata_70362: pd.DataFrame,
    expression_23130: pd.DataFrame,
    metadata_23130: pd.DataFrame,
) -> dict[str, float | int]:
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
    ecm = MECHANISM_SETS["ECM remodelling"]
    summary_70362 = summarise_gene_set(effects_70362, ecm)
    summary_23130 = summarise_gene_set(effects_23130, ecm)
    shared = [gene for gene in ecm if gene in effects_70362.index and gene in effects_23130.index]
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
    parser.add_argument("--random-repetitions", type=int, default=100)
    parser.add_argument("--seed", type=int, default=20260927)
    args = parser.parse_args()

    root = args.project_root.resolve()
    output = PROJECT / "results"
    output.mkdir(parents=True, exist_ok=True)
    inputs = _prepare_inputs(root)
    rng = np.random.default_rng(args.seed)
    rows: list[dict[str, object]] = []

    for mode in ("highest_mean", "first_probe", "median_probe"):
        collapsed_70362 = collapse_probes(
            inputs["expression_70362"],
            inputs["symbols_70362"],
            mode,
        )
        collapsed_23130 = collapse_probes(
            inputs["expression_23130"],
            inputs["symbols_23130"],
            mode,
        )
        result = _primary_ecm(
            collapsed_70362,
            inputs["metadata_70362"],
            collapsed_23130,
            inputs["metadata_23130"],
        )
        rows.append({"mode": mode, "replicate": 0, **result})

    for replicate in range(1, args.random_repetitions + 1):
        collapsed_70362 = collapse_probes(
            inputs["expression_70362"],
            inputs["symbols_70362"],
            "random_probe",
            rng=rng,
        )
        collapsed_23130 = collapse_probes(
            inputs["expression_23130"],
            inputs["symbols_23130"],
            "random_probe",
            rng=rng,
        )
        result = _primary_ecm(
            collapsed_70362,
            inputs["metadata_70362"],
            collapsed_23130,
            inputs["metadata_23130"],
        )
        rows.append({"mode": "random_probe", "replicate": replicate, **result})

    frame = pd.DataFrame(rows)
    frame.to_csv(output / "probe_collapse_sensitivity.csv", index=False)

    random = frame[frame["mode"].eq("random_probe")]
    summary = {
        "random_repetitions": int(len(random)),
        "random_gse70362_fraction_up_median": float(
            random["gse70362_fraction_up"].median()
        ),
        "random_gse70362_fraction_up_lower": float(
            random["gse70362_fraction_up"].quantile(0.025)
        ),
        "random_gse70362_fraction_up_upper": float(
            random["gse70362_fraction_up"].quantile(0.975)
        ),
        "random_gse23130_fraction_up_median": float(
            random["gse23130_fraction_up"].median()
        ),
        "random_gse23130_fraction_up_lower": float(
            random["gse23130_fraction_up"].quantile(0.025)
        ),
        "random_gse23130_fraction_up_upper": float(
            random["gse23130_fraction_up"].quantile(0.975)
        ),
        "random_ecm_concordance_median": float(
            random["ecm_concordance"].median()
        ),
        "random_ecm_concordance_lower": float(
            random["ecm_concordance"].quantile(0.025)
        ),
        "random_ecm_concordance_upper": float(
            random["ecm_concordance"].quantile(0.975)
        ),
        "random_ecm_concordance_p_two_sided_median": float(
            random["ecm_concordance_p_two_sided"].median()
        ),
    }
    (output / "probe_collapse_sensitivity_summary.json").write_text(
        json.dumps(summary, indent=2),
        encoding="utf-8",
    )
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
