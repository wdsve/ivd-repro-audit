"""Data preparation and reproducibility analyses for the IVD audit."""

from __future__ import annotations

import gzip
import io
from pathlib import Path
from typing import Iterable

import numpy as np
import pandas as pd

from .core import (
    benjamini_hochberg,
    binomial_p_two_sided,
    collapse_by_symbols,
    empirical_p_greater,
    ols_effects,
    sign_concordance,
    spearman_correlation,
    summarise_gene_set,
)
from .data import read_gmt, read_series_matrix


MECHANISM_SETS: dict[str, set[str]] = {
    "ECM remodelling": {
        "MMP1", "MMP2", "MMP3", "MMP7", "MMP9", "MMP10", "MMP12", "MMP13",
        "MMP14", "TIMP1", "TIMP2", "TIMP3", "ADAMTS1", "ADAMTS2", "ADAMTS4",
        "ADAMTS5", "COL1A1", "COL2A1", "COL3A1", "COL5A1", "COL9A1", "COL11A1",
        "COL12A1", "FN1", "ELN", "LOX", "LOXL2", "SPARC", "ACAN", "SOX9",
        "CHI3L1",
    },
    "Inflammation/cytokine": {
        "TNF", "IL1B", "IL6", "IL18", "IL1A", "IL4", "IL10", "IL13", "IL17A",
        "TGFB1", "NFKB1", "RELA", "PTGS2", "NLRP3", "CASP1", "CCL2", "CCL3",
        "CCL4", "CCL5", "CXCL1", "CXCL2", "CXCL8", "CXCL10", "CX3CL1",
        "CXCR1", "CXCR2", "TLR2", "TLR4", "MYD88", "IRAK1", "IRF7",
    },
    "Macrophage/myeloid": {
        "CD68", "CD163", "ITGAM", "ITGAX", "CSF1R", "MRC1", "ARG1", "NOS2",
        "CD80", "CD86", "MSR1", "MARCO", "FCGR2A", "FCGR3A", "AIF1", "LYVE1",
        "C1QA", "C1QB", "C1QC", "SIGLEC1", "CD14", "ADGRE1",
    },
    "Angiogenesis/vascular": {
        "VEGFA", "VEGFB", "VEGFC", "KDR", "FLT1", "HIF1A", "HIF1B", "ANGPT1",
        "ANGPT2", "TEK", "PECAM1", "VWF", "PDGFA", "PDGFB", "PDGFRA", "PDGFRB",
        "EDN1", "NOS3", "TIE1",
    },
    "Adhesion/cytoskeleton": {
        "FLNA", "ACTA2", "VIM", "TLN1", "ITGB1", "ITGB2", "ITGA4", "ITGAL",
        "ITGAV", "ICAM1", "VCAM1", "SELE", "SELP", "CDH5", "RHOA", "CDC42",
        "RAC1", "MYH9", "MYL9", "TPM1", "TAGLN", "JUP", "PKP1", "DSP",
    },
    "Apoptosis/autophagy": {
        "FAS", "FASLG", "TNFRSF1A", "CASP1", "CASP3", "CASP6", "CASP7", "CASP8",
        "BAX", "BCL2", "BCL2L1", "MAP1LC3A", "MAP1LC3B", "ATG3", "ATG5", "ATG7",
        "ATG12", "BECN1", "SQSTM1", "MERTK", "GAS6", "MFGE8", "ELMO1", "TYROBP",
        "AXL", "NFE2L2",
    },
    "Immune activation": {
        "CD4", "CD8A", "CD8B", "CD3D", "CD3E", "CD3G", "CD19", "CD79A", "MS4A1",
        "NCAM1", "NKG7", "KLRD1", "GZMA", "GZMB", "PRF1", "IFNG", "IL2", "IL12A",
        "IL12B", "STAT1", "STAT3", "JAK2", "LCP2", "ZAP70", "LCK", "FYN",
        "CD274", "PDCD1", "CTLA4", "FOXP3", "IL2RA",
    },
}

GRADE_MAP = {
    "I": 1.0,
    "I-II": 1.5,
    "II": 2.0,
    "II-III": 2.5,
    "III": 3.0,
    "III-IV": 3.5,
    "IV": 4.0,
    "IV-V": 4.5,
    "V": 5.0,
}


def load_gene_info(path: str | Path) -> tuple[dict[str, str], dict[str, str]]:
    frame = pd.read_csv(path, sep="\t", dtype=str, low_memory=False)
    frame = frame[["GeneID", "Symbol", "dbXrefs"]].fillna("")
    entrez_to_symbol = dict(zip(frame["GeneID"], frame["Symbol"]))
    ensembl_to_symbol: dict[str, str] = {}
    for gene_id, symbol, xrefs in frame.itertuples(index=False):
        for item in str(xrefs).split("|"):
            if item.startswith("Ensembl:"):
                ensembl_to_symbol[item.removeprefix("Ensembl:")] = symbol
    return entrez_to_symbol, ensembl_to_symbol


def build_design(
    metadata: pd.DataFrame,
    continuous: Iterable[str] = (),
    categorical: Iterable[str] = (),
) -> np.ndarray:
    """Build a full-rank design matrix with an intercept and first-level references."""
    pieces: list[np.ndarray] = [np.ones((len(metadata), 1), dtype=float)]
    names = ["intercept"]
    for column in continuous:
        values = pd.to_numeric(metadata[column], errors="coerce").to_numpy(dtype=float)
        if not np.isfinite(values).all():
            raise ValueError(f"continuous design column {column!r} contains missing values")
        pieces.append(values[:, None])
        names.append(column)
    for column in categorical:
        values = metadata[column].astype(str)
        levels = sorted(values.unique())
        for level in levels[1:]:
            pieces.append((values == level).to_numpy(dtype=float)[:, None])
            names.append(f"{column}={level}")
    del names
    return np.column_stack(pieces)


def read_affymetrix_annotation(path: str | Path) -> pd.DataFrame:
    with gzip.open(path, "rt", encoding="utf-8", errors="replace") as handle:
        lines = handle.readlines()
    start = next(i for i, line in enumerate(lines) if line.startswith("ID\t"))
    return pd.read_csv(
        io.StringIO("".join(lines[start:])),
        sep="\t",
        dtype=str,
        low_memory=False,
    )


def prepare_gse70362(
    project_root: str | Path,
) -> tuple[pd.DataFrame, pd.DataFrame]:
    root = Path(project_root)
    expression, metadata = read_series_matrix(
        root / "ldh_pipeline/data/raw/GSE70362/GSE70362_series_matrix.txt.gz"
    )
    entrez_to_symbol, _ = load_gene_info(
        root / "ldh_pipeline/data/raw/annotation/Homo_sapiens.gene_info.gz"
    )
    entrez = expression.index.to_series().str.extract(r"^(\d+)", expand=False)
    symbols = entrez.map(entrez_to_symbol)
    expression = collapse_by_symbols(expression, symbols)

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
    metadata["sample"] = metadata.index
    return expression, metadata


def prepare_gse23130(
    project_root: str | Path,
) -> tuple[pd.DataFrame, pd.DataFrame]:
    root = Path(project_root)
    expression, metadata = read_series_matrix(
        root / "ldh_pipeline/data/raw/GSE23130/GSE23130_series_matrix.txt.gz"
    )
    annotation = read_affymetrix_annotation(
        root / "ldh_pipeline/data/raw/GSE23130/GPL1352.annot.gz"
    )
    probe_to_symbol = dict(zip(annotation.iloc[:, 0], annotation["Gene symbol"]))
    symbols = pd.Series(expression.index, index=expression.index).map(probe_to_symbol)
    expression = collapse_by_symbols(expression, symbols)

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
    metadata["sample"] = metadata.index
    return expression, metadata


def fit_effect_model(
    expression: pd.DataFrame,
    metadata: pd.DataFrame,
    continuous: Iterable[str],
    categorical: Iterable[str],
) -> pd.Series:
    design = build_design(metadata, continuous=continuous, categorical=categorical)
    return ols_effects(expression, design, coefficient=1)


def stratified_half(
    metadata: pd.DataFrame,
    stratum: str,
    rng: np.random.Generator,
) -> np.ndarray:
    indices: list[int] = []
    for _, group in metadata.groupby(stratum, sort=True):
        candidates = group.index.to_numpy(copy=True)
        rng.shuffle(candidates)
        indices.extend(candidates[: max(1, len(candidates) // 2)].tolist())
    return np.asarray(sorted(indices), dtype=int)


def random_one_per_group(
    metadata: pd.DataFrame,
    group_column: str,
    rng: np.random.Generator,
) -> np.ndarray:
    """Choose one independent observation per group."""
    selected: list[int] = []
    for _, group in metadata.groupby(group_column, sort=True):
        positions = group.index.to_numpy(copy=True)
        selected.append(int(rng.choice(positions)))
    return np.asarray(sorted(selected), dtype=int)


def group_stratified_half(
    metadata: pd.DataFrame,
    group_column: str,
    stratum_column: str,
    rng: np.random.Generator,
) -> np.ndarray:
    """Split whole groups into halves while balancing a group-level stratum."""
    group_values = metadata.groupby(group_column)[stratum_column].median()
    unique_strata = np.sort(group_values.unique())
    selected_groups: list[str] = []
    for stratum in unique_strata:
        groups = group_values[group_values == stratum].index.to_numpy(copy=True)
        rng.shuffle(groups)
        selected_groups.extend(groups[: max(1, len(groups) // 2)].tolist())
    selected = metadata.index[metadata[group_column].isin(selected_groups)]
    return np.asarray(sorted(selected), dtype=int)


def cluster_bootstrap_indices(
    metadata: pd.DataFrame,
    group_column: str,
    rng: np.random.Generator,
) -> np.ndarray:
    """Bootstrap whole groups and return all rows from each sampled group."""
    groups = metadata[group_column].drop_duplicates().to_numpy(copy=True)
    sampled = rng.choice(groups, size=len(groups), replace=True)
    positions: list[int] = []
    for group in sampled:
        positions.extend(metadata.index[metadata[group_column] == group].tolist())
    return np.asarray(positions, dtype=int)


def permutation_module_directions(
    expression: pd.DataFrame,
    metadata: pd.DataFrame,
    gene_sets: dict[str, set[str]],
    continuous: Iterable[str],
    categorical: Iterable[str],
    *,
    n_perm: int = 999,
    seed: int = 2026,
    method: str = "label",
) -> pd.DataFrame:
    """Permutation p-values for directional imbalance in every module."""
    if method not in {"label", "stratified", "freedman_lane", "rotation"}:
        raise ValueError(f"unsupported permutation method: {method}")
    continuous = list(continuous)
    categorical = list(categorical)
    names = list(gene_sets)
    gene_to_index = {gene: index for index, gene in enumerate(expression.index)}
    module_matrix = np.zeros((len(expression), len(names)), dtype=np.float32)
    module_sizes = np.zeros(len(names), dtype=float)
    for module_index, name in enumerate(names):
        indices = [gene_to_index[gene] for gene in gene_sets[name] if gene in gene_to_index]
        module_sizes[module_index] = len(indices)
        if indices:
            module_matrix[indices, module_index] = 1.0

    observed = fit_effect_model(
        expression,
        metadata,
        continuous=continuous,
        categorical=categorical,
    )
    observed_values = observed.to_numpy(dtype=float)
    observed_positive = (observed_values > 0).astype(np.float32)
    observed_fraction = (module_matrix.T @ observed_positive) / module_sizes

    null_fraction = np.zeros((n_perm, len(names)), dtype=np.float32)
    rng = np.random.default_rng(seed)
    full_design = build_design(
        metadata,
        continuous=continuous,
        categorical=categorical,
    )
    reduced_design = build_design(
        metadata,
        continuous=[],
        categorical=categorical,
    )
    expression_values = expression.to_numpy(dtype=float)
    reduced_beta = np.linalg.lstsq(
        reduced_design,
        expression_values.T,
        rcond=None,
    )[0]
    reduced_fitted = reduced_design @ reduced_beta
    residuals = expression_values.T - reduced_fitted

    for permutation_index in range(n_perm):
        if method in {"label", "stratified"}:
            permuted = metadata.copy()
            if method == "stratified" and categorical:
                order = np.arange(len(permuted))
                for _, group in permuted.groupby(list(categorical), sort=True):
                    positions = group.index.to_numpy(copy=True)
                    if len(positions) > 1:
                        order[positions] = rng.permutation(positions)
            else:
                order = rng.permutation(len(permuted))
            if continuous:
                permuted[continuous] = metadata[continuous].to_numpy()[order]
            design = build_design(
                permuted,
                continuous=continuous,
                categorical=categorical,
            )
            permuted_values = expression_values.T
        elif method == "freedman_lane":
            design = full_design
            order = rng.permutation(residuals.shape[1])
            permuted_values = reduced_fitted + residuals[:, order]
        else:
            design = full_design
            rotation, _ = np.linalg.qr(
                rng.standard_normal((residuals.shape[1], residuals.shape[1]))
            )
            permuted_values = reduced_fitted + residuals @ rotation
        beta, *_ = np.linalg.lstsq(
            design,
            permuted_values,
            rcond=None,
        )
        positive = (beta[1] > 0).astype(np.float32)
        null_fraction[permutation_index] = (
            module_matrix.T @ positive
        ) / module_sizes

    records: list[dict[str, float | str]] = []
    for module_index, name in enumerate(names):
        fraction = float(observed_fraction[module_index])
        null = null_fraction[:, module_index]
        p_up = empirical_p_greater(fraction, null)
        p_down = empirical_p_greater(1 - fraction, 1 - null)
        records.append(
            {
                "module": name,
                "n_genes": int(module_sizes[module_index]),
                "observed_fraction_up": fraction,
                "p_up": p_up,
                "p_down": p_down,
                "p_two_sided": min(1.0, 2 * min(p_up, p_down)),
            }
        )
    return pd.DataFrame(records)


def split_half_reliability(
    expression: pd.DataFrame,
    metadata: pd.DataFrame,
    continuous: Iterable[str],
    categorical: Iterable[str],
    n_rep: int = 100,
    seed: int = 2026,
    group_column: str | None = None,
) -> dict[str, float]:
    rng = np.random.default_rng(seed)
    correlations: list[float] = []
    for _ in range(n_rep):
        first = (
            group_stratified_half(
                metadata,
                group_column=group_column,
                stratum_column="grade",
                rng=rng,
            )
            if group_column
            else stratified_half(metadata, "grade", rng)
        )
        second = metadata.index.difference(first).to_numpy()
        if len(first) < 4 or len(second) < 4:
            continue
        effect_a = fit_effect_model(
            expression.iloc[:, first],
            metadata.iloc[first],
            continuous=continuous,
            categorical=categorical,
        )
        effect_b = fit_effect_model(
            expression.iloc[:, second],
            metadata.iloc[second],
            continuous=continuous,
            categorical=categorical,
        )
        valid = effect_a.notna() & effect_b.notna()
        if valid.sum() < min(100, len(expression)):
            continue
        correlations.append(spearman_correlation(effect_a[valid], effect_b[valid]))
    finite = [value for value in correlations if np.isfinite(value)]
    return {
        "median_spearman": float(np.median(finite)) if finite else float("nan"),
        "n_splits": len(finite),
    }


def donor_effect_sensitivity(
    expression: pd.DataFrame,
    metadata: pd.DataFrame,
    genes: set[str],
    reference_effects: pd.Series,
    continuous: Iterable[str],
    categorical: Iterable[str],
    *,
    group_column: str = "donor",
    n_rep: int = 500,
    seed: int = 2026,
) -> pd.DataFrame:
    """One-sample-per-donor and cluster-bootstrap sensitivity distributions."""
    selected_genes = [gene for gene in genes if gene in expression.index]
    expression = expression.loc[selected_genes]
    rng = np.random.default_rng(seed)
    records: list[dict[str, float | int | str]] = []
    for mode in ("one_sample_per_donor", "cluster_bootstrap"):
        for replicate in range(n_rep):
            indices = (
                random_one_per_group(metadata, group_column, rng)
                if mode == "one_sample_per_donor"
                else cluster_bootstrap_indices(metadata, group_column, rng)
            )
            sampled_metadata = metadata.iloc[indices].reset_index(drop=True)
            sampled_expression = expression.iloc[:, indices]
            sampled_effects = fit_effect_model(
                sampled_expression,
                sampled_metadata,
                continuous=continuous,
                categorical=categorical,
            )
            summary = summarise_gene_set(sampled_effects, genes)
            concordance = sign_concordance(sampled_effects, reference_effects)
            records.append(
                {
                    "mode": mode,
                    "replicate": replicate,
                    "n_samples": len(indices),
                    "n_donors": sampled_metadata[group_column].nunique(),
                    "fraction_up": summary["fraction_up"],
                    "median_effect": summary["median_effect"],
                    "gene_concordance": concordance["fraction"],
                    "effect_rho": spearman_correlation(
                        sampled_effects,
                        reference_effects,
                    ),
                }
            )
    return pd.DataFrame(records)


def weighted_sign_concordance(
    effects_a: pd.Series,
    effects_b: pd.Series,
) -> dict[str, float]:
    """Unweighted and effect-size-weighted cross-cohort sign concordance."""
    frame = pd.concat(
        [effects_a.rename("a"), effects_b.rename("b")],
        axis=1,
        join="inner",
    ).dropna()
    frame = frame[(frame["a"] != 0) & (frame["b"] != 0)]
    if frame.empty:
        return {
            "n_genes": 0,
            "unweighted": float("nan"),
            "weighted": float("nan"),
            "top_half": float("nan"),
            "effect_rho": float("nan"),
        }
    concordant = np.sign(frame["a"]) == np.sign(frame["b"])
    weights = np.minimum(frame["a"].abs(), frame["b"].abs())
    top_n = max(1, int(np.ceil(len(frame) / 2)))
    top_genes = weights.nlargest(top_n).index
    return {
        "n_genes": int(len(frame)),
        "unweighted": float(concordant.mean()),
        "weighted": float(
            np.average(concordant.astype(float), weights=weights.to_numpy())
        ),
        "top_half": float(concordant.loc[top_genes].mean()),
        "effect_rho": spearman_correlation(frame["a"], frame["b"]),
    }


def sign_concordance_power(
    *,
    true_correlations: Iterable[float],
    reliability_a: float,
    reliability_b: float,
    n_genes: int,
    effective_n_genes: int,
    n_rep: int = 5000,
    alpha: float = 0.05,
    seed: int = 2026,
) -> pd.DataFrame:
    """Power of gene-level sign tests under known latent correlations."""
    rng = np.random.default_rng(seed)
    records: list[dict[str, float]] = []
    for true_correlation in true_correlations:
        latent_a = rng.standard_normal((n_rep, n_genes))
        latent_b = (
            true_correlation * latent_a
            + np.sqrt(1 - true_correlation**2)
            * rng.standard_normal((n_rep, n_genes))
        )
        observed_a = (
            np.sqrt(reliability_a) * latent_a
            + np.sqrt(1 - reliability_a) * rng.standard_normal((n_rep, n_genes))
        )
        observed_b = (
            np.sqrt(reliability_b) * latent_b
            + np.sqrt(1 - reliability_b) * rng.standard_normal((n_rep, n_genes))
        )
        concordance = np.mean(
            np.sign(observed_a) == np.sign(observed_b),
            axis=1,
        )
        nominal_hits = 0
        effective_hits = 0
        effective_n = max(1, int(round(effective_n_genes)))
        for fraction in concordance:
            k = int(round(fraction * n_genes))
            if binomial_p_two_sided(k, n_genes) < alpha:
                nominal_hits += 1
            k_effective = int(round(fraction * effective_n))
            if binomial_p_two_sided(k_effective, effective_n) < alpha:
                effective_hits += 1
        records.append(
            {
                "true_correlation": true_correlation,
                "mean_concordance": float(np.mean(concordance)),
                "power_nominal_n": nominal_hits / n_rep,
                "power_effective_n": effective_hits / n_rep,
                "effective_n_genes": effective_n,
            }
        )
    return pd.DataFrame(records)


def module_score_slope(
    expression: pd.DataFrame,
    metadata: pd.DataFrame,
    genes: set[str],
    continuous: Iterable[str],
    categorical: Iterable[str],
) -> dict[str, float]:
    """Association of a prespecified module score with the continuous endpoint."""
    selected = [gene for gene in genes if gene in expression.index]
    if len(selected) < 3:
        return {"n_genes": len(selected), "slope": float("nan")}
    matrix = expression.loc[selected].to_numpy(dtype=float)
    matrix = (matrix - matrix.mean(axis=1, keepdims=True)) / matrix.std(
        axis=1,
        keepdims=True,
    )
    score = np.nanmean(matrix, axis=0)
    design = build_design(
        metadata,
        continuous=continuous,
        categorical=categorical,
    )
    beta, *_ = np.linalg.lstsq(design, score, rcond=None)
    return {"n_genes": len(selected), "slope": float(beta[1])}


def cross_half_concordance(
    expression: pd.DataFrame,
    metadata: pd.DataFrame,
    genes: set[str],
    continuous: Iterable[str],
    categorical: Iterable[str],
    *,
    group_column: str | None = None,
    n_rep: int = 300,
    seed: int = 2026,
) -> pd.DataFrame:
    """Positive-control distribution from independent within-cohort halves."""
    selected_genes = [gene for gene in genes if gene in expression.index]
    expression = expression.loc[selected_genes]
    rng = np.random.default_rng(seed)
    records: list[dict[str, float | int]] = []
    for replicate in range(n_rep):
        first = (
            group_stratified_half(
                metadata,
                group_column=group_column,
                stratum_column="grade",
                rng=rng,
            )
            if group_column
            else stratified_half(metadata, "grade", rng)
        )
        second = metadata.index.difference(first).to_numpy()
        effect_a = fit_effect_model(
            expression.iloc[:, first],
            metadata.iloc[first].reset_index(drop=True),
            continuous=continuous,
            categorical=categorical,
        )
        effect_b = fit_effect_model(
            expression.iloc[:, second],
            metadata.iloc[second].reset_index(drop=True),
            continuous=continuous,
            categorical=categorical,
        )
        summary_a = summarise_gene_set(effect_a, genes)
        summary_b = summarise_gene_set(effect_b, genes)
        concordance = sign_concordance(effect_a, effect_b)
        records.append(
            {
                "replicate": replicate,
                "fraction_up_a": summary_a["fraction_up"],
                "fraction_up_b": summary_b["fraction_up"],
                "median_effect_a": summary_a["median_effect"],
                "median_effect_b": summary_b["median_effect"],
                "gene_concordance": concordance["fraction"],
                "effect_rho": spearman_correlation(effect_a, effect_b),
            }
        )
    return pd.DataFrame(records)


def size_matched_concordance_p(
    effects_a: pd.Series,
    effects_b: pd.Series,
    observed_fraction: float,
    n_genes: int,
    *,
    n_perm: int = 5000,
    seed: int = 2026,
) -> dict[str, float]:
    """Size-matched empirical null for gene-level direction concordance."""
    frame = pd.concat(
        [effects_a.rename("a"), effects_b.rename("b")],
        axis=1,
        join="inner",
    ).dropna()
    frame = frame[(frame["a"] != 0) & (frame["b"] != 0)]
    concordant = (
        np.sign(frame["a"].to_numpy()) == np.sign(frame["b"].to_numpy())
    ).astype(float)
    if len(concordant) == 0 or n_genes <= 0:
        return {
            "empirical_p": float("nan"),
            "null_median": float("nan"),
            "null_upper_95": float("nan"),
        }
    rng = np.random.default_rng(seed)
    indices = rng.integers(
        0,
        len(concordant),
        size=(n_perm, min(n_genes, len(concordant))),
    )
    null = concordant[indices].mean(axis=1)
    p_greater = empirical_p_greater(observed_fraction, null)
    p_less = empirical_p_greater(-observed_fraction, -null)
    return {
        "empirical_p_greater": p_greater,
        "empirical_p_less": p_less,
        "empirical_p_two_sided": min(1.0, 2 * min(p_greater, p_less)),
        "null_median": float(np.median(null)),
        "null_upper_95": float(np.quantile(null, 0.95)),
    }


def expression_matched_concordance_p(
    effects_a: pd.Series,
    effects_b: pd.Series,
    expression_a: pd.DataFrame,
    expression_b: pd.DataFrame,
    genes: set[str],
    *,
    n_bins: int = 5,
    n_perm: int = 5000,
    seed: int = 2026,
) -> dict[str, float]:
    """Expression-matched empirical null for one gene set."""
    common_all = [
        gene
        for gene in effects_a.index
        if gene in effects_b.index
        and gene in expression_a.index
        and gene in expression_b.index
    ]
    common_all = [
        gene
        for gene in common_all
        if np.isfinite(effects_a[gene])
        and np.isfinite(effects_b[gene])
        and effects_a[gene] != 0
        and effects_b[gene] != 0
    ]
    module_genes = [gene for gene in genes if gene in set(common_all)]
    if len(module_genes) < 10:
        return {
            "n_genes": len(module_genes),
            "empirical_p": float("nan"),
            "null_median": float("nan"),
            "null_upper_95": float("nan"),
        }
    a = effects_a.reindex(common_all)
    b = effects_b.reindex(common_all)
    observed = sign_concordance(
        effects_a.reindex(module_genes),
        effects_b.reindex(module_genes),
    )["fraction"]
    mean_a = expression_a.reindex(common_all).mean(axis=1).rank(pct=True)
    mean_b = expression_b.reindex(common_all).mean(axis=1).rank(pct=True)
    expression_score = (mean_a + mean_b) / 2
    bins = pd.qcut(expression_score, q=n_bins, labels=False, duplicates="drop")

    frame = pd.DataFrame({"a": a, "b": b, "bin": bins}).dropna()
    frame["concordant"] = np.sign(frame["a"]) == np.sign(frame["b"])
    module_frame = frame.loc[module_genes]
    bin_positions = {
        int(bin_value): group.index.to_numpy(copy=True)
        for bin_value, group in frame.groupby("bin")
    }
    counts = module_frame["bin"].value_counts().to_dict()
    rng = np.random.default_rng(seed)
    null = np.zeros(n_perm, dtype=float)
    for permutation_index in range(n_perm):
        selected: list[str] = []
        for bin_value, count in counts.items():
            positions = bin_positions[int(bin_value)]
            sampled = rng.choice(positions, size=count, replace=False)
            selected.extend(sampled.tolist())
        null[permutation_index] = frame.loc[selected, "concordant"].mean()
    return {
        "n_genes": len(module_frame),
        "empirical_p_greater": empirical_p_greater(observed, null),
        "empirical_p_less": empirical_p_greater(-observed, -null),
        "empirical_p_two_sided": min(
            1.0,
            2
            * min(
                empirical_p_greater(observed, null),
                empirical_p_greater(-observed, -null),
            ),
        ),
        "null_median": float(np.median(null)),
        "null_upper_95": float(np.quantile(null, 0.95)),
    }


def add_size_matched_concordance_p(
    audit: pd.DataFrame,
    effects_a: pd.Series,
    effects_b: pd.Series,
    *,
    n_perm: int = 5000,
    seed: int = 2026,
) -> pd.DataFrame:
    """Add size-matched empirical concordance p-values to a module audit table."""
    results = audit.copy()
    null_by_size: dict[int, np.ndarray] = {}
    frame = pd.concat(
        [effects_a.rename("a"), effects_b.rename("b")],
        axis=1,
        join="inner",
    ).dropna()
    frame = frame[(frame["a"] != 0) & (frame["b"] != 0)]
    concordant = (
        np.sign(frame["a"].to_numpy()) == np.sign(frame["b"].to_numpy())
    ).astype(float)
    rng = np.random.default_rng(seed)
    for size in sorted(results["n_genes"].astype(int).unique()):
        indices = rng.integers(
            0,
            len(concordant),
            size=(n_perm, min(size, len(concordant))),
        )
        null_by_size[int(size)] = concordant[indices].mean(axis=1)
    empirical_less = []
    empirical_greater = []
    null_median = []
    null_upper = []
    for row in results.itertuples(index=False):
        size = int(row.n_genes)
        null = null_by_size[size]
        empirical_greater.append(
            empirical_p_greater(float(row.gene_concordance), null)
        )
        empirical_less.append(
            empirical_p_greater(-float(row.gene_concordance), -null)
        )
        null_median.append(float(np.median(null)))
        null_upper.append(float(np.quantile(null, 0.95)))
    results["concordance_empirical_p_greater"] = empirical_greater
    results["concordance_empirical_p_less"] = empirical_less
    results["concordance_empirical_p_two_sided"] = [
        min(1.0, 2 * min(greater, less))
        for greater, less in zip(empirical_greater, empirical_less)
    ]
    results["concordance_null_median"] = null_median
    results["concordance_null_upper_95"] = null_upper
    results["concordance_q_two_sided"] = benjamini_hochberg(
        results["concordance_empirical_p_two_sided"].to_numpy()
    )
    return results


def effect_diagnostics(effects: pd.Series) -> dict[str, float | int | bool]:
    values = effects.replace([np.inf, -np.inf], np.nan).dropna()
    values = values[values != 0]
    fraction_up = float((values > 0).mean())
    median_effect = float(values.median())
    return {
        "n_genes": int(len(values)),
        "fraction_up": fraction_up,
        "median_effect": median_effect,
        "global_shift": bool(
            abs(median_effect) > 0.2 or fraction_up > 0.70 or fraction_up < 0.30
        ),
    }


def module_table(
    effects: pd.Series,
    gene_sets: dict[str, set[str]],
) -> pd.DataFrame:
    rows = []
    for name, genes in gene_sets.items():
        summary = summarise_gene_set(effects, genes)
        summary["module"] = name
        rows.append(summary)
    columns = [
        "module",
        "n_genes",
        "n_up",
        "fraction_up",
        "median_effect",
        "sign_p_greater",
    ]
    return pd.DataFrame(rows)[columns].sort_values("sign_p_greater")


def paired_module_audit(
    effects_a: pd.Series,
    effects_b: pd.Series,
    gene_sets: dict[str, set[str]],
    min_genes: int = 10,
) -> pd.DataFrame:
    rows: list[dict[str, object]] = []
    for name, genes in gene_sets.items():
        shared = [gene for gene in genes if gene in effects_a.index and gene in effects_b.index]
        if len(shared) < min_genes:
            continue
        summary_a = summarise_gene_set(effects_a, shared)
        summary_b = summarise_gene_set(effects_b, shared)
        concordance = sign_concordance(effects_a[shared], effects_b[shared])
        same_direction = (
            np.isfinite(summary_a["median_effect"])
            and np.isfinite(summary_b["median_effect"])
            and np.sign(summary_a["median_effect"]) == np.sign(summary_b["median_effect"])
        )
        significant_a = summary_a["sign_p_greater"] < 0.05
        significant_b = summary_b["sign_p_greater"] < 0.05
        replicated = (
            same_direction
            and significant_a
            and significant_b
            and concordance["fraction"] > 0.5
            and concordance["binomial_p_greater"] < 0.05
        )
        rows.append(
            {
                "module": name,
                "n_genes": len(shared),
                "cohort_a_fraction_up": summary_a["fraction_up"],
                "cohort_a_median_effect": summary_a["median_effect"],
                "cohort_a_sign_p": summary_a["sign_p_greater"],
                "cohort_a_sign_p_two_sided": summary_a["sign_p_two_sided"],
                "cohort_b_fraction_up": summary_b["fraction_up"],
                "cohort_b_median_effect": summary_b["median_effect"],
                "cohort_b_sign_p": summary_b["sign_p_greater"],
                "cohort_b_sign_p_two_sided": summary_b["sign_p_two_sided"],
                "gene_concordance": concordance["fraction"],
                "gene_concordance_p": concordance["binomial_p_greater"],
                "gene_concordance_p_two_sided": concordance[
                    "binomial_p_two_sided"
                ],
                "same_direction": same_direction,
                "significant_in_cohort_a": significant_a,
                "significant_in_cohort_b": significant_b,
                "gene_level_replicated": replicated,
            }
        )
    return pd.DataFrame(rows).sort_values(
        ["gene_level_replicated", "gene_concordance"],
        ascending=[False, False],
    )


def pairwise_concordance(
    effects: pd.DataFrame,
    metadata: pd.DataFrame,
) -> pd.DataFrame:
    rows: list[dict[str, object]] = []
    cohorts = list(effects.columns)
    for i, cohort_a in enumerate(cohorts):
        for cohort_b in cohorts[i + 1 :]:
            shared = effects[[cohort_a, cohort_b]].dropna()
            signed = shared[(shared[cohort_a] != 0) & (shared[cohort_b] != 0)]
            n_genes = len(signed)
            if n_genes == 0:
                continue
            concordance = sign_concordance(
                signed[cohort_a].to_numpy(),
                signed[cohort_b].to_numpy(),
            )
            meta_a = metadata.set_index("cohort").loc[cohort_a]
            meta_b = metadata.set_index("cohort").loc[cohort_b]
            rows.append(
                {
                    "cohort_a": cohort_a,
                    "cohort_b": cohort_b,
                    "same_compartment": meta_a["compartment"] == meta_b["compartment"],
                    "same_tissue": meta_a["tissue"] == meta_b["tissue"],
                    "same_endpoint_class": meta_a["endpoint_class"] == meta_b["endpoint_class"],
                    "n_genes": n_genes,
                    "gene_concordance": concordance["fraction"],
                    "gene_concordance_p": concordance["binomial_p_greater"],
                    "rho": spearman_correlation(signed[cohort_a], signed[cohort_b]),
                }
            )
    return pd.DataFrame(rows).sort_values("gene_concordance", ascending=False)


def read_msigdb_symbol_sets(
    project_root: str | Path,
    collection_names: Iterable[str] = ("h.all.v2024.1.Hs.entrez.gmt",),
) -> dict[str, set[str]]:
    root = Path(project_root) / "ldh_pipeline/data/raw/msigdb"
    entrez_to_symbol, _ = load_gene_info(
        Path(project_root) / "ldh_pipeline/data/raw/annotation/Homo_sapiens.gene_info.gz"
    )
    output: dict[str, set[str]] = {}
    for filename in collection_names:
        for name, entrez in read_gmt(root / filename).items():
            symbols = {entrez_to_symbol[gene] for gene in entrez if gene in entrez_to_symbol}
            if len(symbols) >= 10:
                output[name] = symbols
    return output
