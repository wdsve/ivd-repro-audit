"""Core statistics used by the intervertebral disc reproducibility audit."""

from __future__ import annotations

import math
from typing import Mapping

import numpy as np
import pandas as pd


def _log_binomial_term(n: int, k: int, p: float) -> float:
    if p in (0.0, 1.0):
        if p == 0.0:
            return 0.0 if k == 0 else -math.inf
        return 0.0 if k == n else -math.inf
    return (
        math.lgamma(n + 1)
        - math.lgamma(k + 1)
        - math.lgamma(n - k + 1)
        + k * math.log(p)
        + (n - k) * math.log1p(-p)
    )


def binomial_p_greater(k: int, n: int, p: float = 0.5) -> float:
    """Exact P(X >= k) for X ~ Binomial(n, p)."""
    if n < 0:
        raise ValueError("n must be non-negative")
    if k < 0:
        return 1.0
    if k > n:
        return 0.0
    log_terms = [_log_binomial_term(n, i, p) for i in range(k, n + 1)]
    max_log = max(log_terms)
    if max_log == -math.inf:
        return 0.0
    return math.exp(max_log + math.log(sum(math.exp(x - max_log) for x in log_terms)))


def binomial_p_less(k: int, n: int, p: float = 0.5) -> float:
    """Exact P(X <= k) for X ~ Binomial(n, p)."""
    if n < 0:
        raise ValueError("n must be non-negative")
    if k < 0:
        return 0.0
    if k >= n:
        return 1.0
    log_terms = [_log_binomial_term(n, i, p) for i in range(0, k + 1)]
    max_log = max(log_terms)
    if max_log == -math.inf:
        return 0.0
    return math.exp(max_log + math.log(sum(math.exp(x - max_log) for x in log_terms)))


def binomial_p_two_sided(k: int, n: int, p: float = 0.5) -> float:
    """Two-sided exact binomial probability using doubled smaller tail."""
    return min(
        1.0,
        2 * min(binomial_p_greater(k, n, p), binomial_p_less(k, n, p)),
    )


def _finite_float(value: object) -> bool:
    try:
        return math.isfinite(float(value))
    except (TypeError, ValueError):
        return False


def sign_concordance(
    cohort_a: Mapping[str, float] | pd.Series,
    cohort_b: Mapping[str, float] | pd.Series,
) -> dict[str, float | int]:
    """Compare finite, non-zero gene-level effect directions across two cohorts."""
    a = pd.Series(cohort_a, dtype=float)
    b = pd.Series(cohort_b, dtype=float)
    frame = pd.concat([a.rename("a"), b.rename("b")], axis=1, join="inner")
    frame = frame[
        np.isfinite(frame["a"])
        & np.isfinite(frame["b"])
        & (frame["a"] != 0)
        & (frame["b"] != 0)
    ]
    n = int(len(frame))
    if n == 0:
        return {
            "n": 0,
            "n_concordant": 0,
            "fraction": float("nan"),
            "binomial_p_greater": float("nan"),
            "binomial_p_less": float("nan"),
            "binomial_p_two_sided": float("nan"),
        }
    concordant = np.sign(frame["a"].to_numpy()) == np.sign(frame["b"].to_numpy())
    n_concordant = int(concordant.sum())
    return {
        "n": n,
        "n_concordant": n_concordant,
        "fraction": n_concordant / n,
        "binomial_p_greater": binomial_p_greater(n_concordant, n),
        "binomial_p_less": binomial_p_less(n_concordant, n),
        "binomial_p_two_sided": min(
            1.0,
            2
            * min(
                binomial_p_greater(n_concordant, n),
                binomial_p_less(n_concordant, n),
            ),
        ),
    }


def collapse_by_symbols(
    expression: pd.DataFrame,
    symbols: Mapping[str, str] | pd.Series,
) -> pd.DataFrame:
    """Collapse probes to symbols, retaining the highest-mean probe per symbol."""
    symbol_series = pd.Series(symbols, dtype="object").reindex(expression.index)
    valid = symbol_series.notna() & symbol_series.astype(str).str.strip().ne("")
    values = expression.loc[valid].copy()
    values["__symbol__"] = symbol_series.loc[valid].astype(str).to_numpy()
    values["__mean__"] = values.drop(columns="__symbol__").mean(axis=1, skipna=True)
    values = values.sort_values("__mean__", ascending=False, kind="mergesort")
    values = values.drop_duplicates("__symbol__", keep="first")
    collapsed = values.drop(columns=["__symbol__", "__mean__"])
    collapsed.index = values["__symbol__"].to_numpy()
    return collapsed


def ols_effects(
    expression: pd.DataFrame,
    design: np.ndarray,
    coefficient: int = 1,
) -> pd.Series:
    """Estimate one linear-model coefficient for every row of an expression matrix."""
    x = np.asarray(design, dtype=float)
    if x.ndim != 2:
        raise ValueError("design must be a two-dimensional matrix")
    if x.shape[0] != expression.shape[1]:
        raise ValueError("design rows must match expression columns")
    if not 0 <= coefficient < x.shape[1]:
        raise ValueError("coefficient is outside the design matrix")

    values = expression.to_numpy(dtype=float)
    finite = np.isfinite(values)
    if not finite.all():
        values = np.where(finite, values, np.nan)

    estimates = np.full(expression.shape[0], np.nan, dtype=float)
    complete_rows = finite.all(axis=1)
    if complete_rows.any():
        beta, *_ = np.linalg.lstsq(x, values[complete_rows].T, rcond=None)
        estimates[complete_rows] = beta[coefficient]
    return pd.Series(estimates, index=expression.index, name="effect")


def summarise_gene_set(
    effects: Mapping[str, float] | pd.Series,
    genes: list[str] | set[str] | tuple[str, ...],
) -> dict[str, float | int]:
    """Summarise direction and magnitude for a prespecified gene set."""
    effect_series = pd.Series(effects, dtype=float)
    selected = effect_series.reindex(list(genes))
    selected = selected[np.isfinite(selected) & (selected != 0)]
    n_genes = int(len(selected))
    if n_genes == 0:
        return {
            "n_genes": 0,
            "n_up": 0,
            "fraction_up": float("nan"),
            "median_effect": float("nan"),
            "sign_p_greater": float("nan"),
            "sign_p_two_sided": float("nan"),
        }
    n_up = int((selected > 0).sum())
    return {
        "n_genes": n_genes,
        "n_up": n_up,
        "fraction_up": n_up / n_genes,
        "median_effect": float(selected.median()),
        "sign_p_greater": binomial_p_greater(n_up, n_genes),
        "sign_p_two_sided": min(
            1.0,
            2
            * min(
                binomial_p_greater(n_up, n_genes),
                binomial_p_less(n_up, n_genes),
            ),
        ),
    }


def spearman_correlation(
    values_a: Mapping[str, float] | pd.Series,
    values_b: Mapping[str, float] | pd.Series,
) -> float:
    """Spearman correlation without relying on SciPy."""
    a = pd.Series(values_a, dtype=float)
    b = pd.Series(values_b, dtype=float)
    frame = pd.concat([a.rename("a"), b.rename("b")], axis=1, join="inner").dropna()
    if len(frame) < 2:
        return float("nan")
    ranks = frame.rank(method="average")
    if ranks["a"].nunique() < 2 or ranks["b"].nunique() < 2:
        return float("nan")
    return float(np.corrcoef(ranks["a"].to_numpy(), ranks["b"].to_numpy())[0, 1])


def empirical_p_greater(observed: float, null: np.ndarray) -> float:
    """Add-one empirical upper-tail probability."""
    values = np.asarray(null, dtype=float)
    values = values[np.isfinite(values)]
    if len(values) == 0:
        return float("nan")
    return float((1 + np.sum(values >= observed)) / (len(values) + 1))


def benjamini_hochberg(p_values: np.ndarray) -> np.ndarray:
    """Benjamini-Hochberg FDR, returned in the input order."""
    values = np.asarray(p_values, dtype=float)
    output = np.full(len(values), np.nan, dtype=float)
    finite = np.isfinite(values)
    if not finite.any():
        return output
    indices = np.where(finite)[0]
    ordered = indices[np.argsort(values[indices], kind="mergesort")]
    ranked = values[ordered]
    m = len(ranked)
    adjusted = ranked * m / np.arange(1, m + 1)
    adjusted = np.minimum.accumulate(adjusted[::-1])[::-1]
    adjusted = np.clip(adjusted, 0, 1)
    output[ordered] = adjusted
    return output


def effective_gene_number(expression: pd.DataFrame) -> float:
    """Effective number of independent genes from the correlation spectrum."""
    values = expression.to_numpy(dtype=float)
    if values.shape[0] == 0:
        return float("nan")
    if values.shape[0] == 1:
        return 1.0
    complete = np.isfinite(values).all(axis=1)
    values = values[complete]
    if values.shape[0] < 2:
        return float("nan")
    correlations = np.corrcoef(values)
    eigvals = np.real(np.linalg.eigvalsh(correlations))
    eigvals = eigvals[eigvals > 0]
    if len(eigvals) == 0:
        return float("nan")
    return float(eigvals.sum() ** 2 / np.square(eigvals).sum())


def spearman_brown(split_half_reliability: float) -> float:
    """Correct a split-half reliability to the full-length estimate."""
    value = float(split_half_reliability)
    if not np.isfinite(value) or value <= -1:
        return float("nan")
    return float(2 * value / (1 + value))


def disattenuate_correlation(
    observed_correlation: float,
    reliability_a: float,
    reliability_b: float,
) -> float:
    """Correct a cross-cohort correlation for independent measurement error."""
    if reliability_a <= 0 or reliability_b <= 0:
        return float("nan")
    corrected = float(observed_correlation) / math.sqrt(reliability_a * reliability_b)
    return float(np.clip(corrected, -1, 1))


def simulate_sign_concordance(
    *,
    true_correlation: float,
    reliability_a: float,
    reliability_b: float,
    n_genes: int,
    n_rep: int = 2000,
    seed: int = 2026,
) -> dict[str, float]:
    """Simulate expected sign concordance under latent effect correlation and noise."""
    if not -1 <= true_correlation <= 1:
        raise ValueError("true_correlation must be between -1 and 1")
    if not 0 < reliability_a <= 1 or not 0 < reliability_b <= 1:
        raise ValueError("reliabilities must be in (0, 1]")
    rng = np.random.default_rng(seed)
    latent_a = rng.standard_normal((n_rep, n_genes))
    latent_b = (
        true_correlation * latent_a
        + math.sqrt(1 - true_correlation**2) * rng.standard_normal((n_rep, n_genes))
    )
    observed_a = (
        math.sqrt(reliability_a) * latent_a
        + math.sqrt(1 - reliability_a) * rng.standard_normal((n_rep, n_genes))
    )
    observed_b = (
        math.sqrt(reliability_b) * latent_b
        + math.sqrt(1 - reliability_b) * rng.standard_normal((n_rep, n_genes))
    )
    concordance = np.mean(np.sign(observed_a) == np.sign(observed_b), axis=1)
    return {
        "mean": float(np.mean(concordance)),
        "lower_2_5": float(np.quantile(concordance, 0.025)),
        "upper_97_5": float(np.quantile(concordance, 0.975)),
    }
