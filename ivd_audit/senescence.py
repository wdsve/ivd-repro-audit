"""Paired senescent-versus-non-senescent analysis for GSE17077."""

from __future__ import annotations

import re

import numpy as np
import pandas as pd


def derive_donor_id(title: str) -> str:
    value = re.sub(r"(?i)^Disc Tissue\s*", "", str(title)).strip()
    value = re.sub(r"(?i)(?:ts|s)$", "", value).strip()
    value = re.sub(r"\s*-\s*", "-", value)
    return re.sub(r"\s+", "", value)


def paired_senescence_effects(
    expression: pd.DataFrame,
    metadata: pd.DataFrame,
) -> tuple[pd.Series, pd.Series]:
    """Estimate paired senescent minus non-senescent effects by donor."""
    meta = metadata.copy()
    meta["donor"] = meta["title"].map(derive_donor_id)
    meta["status"] = meta["status"].str.strip().str.lower()
    donor_differences: dict[str, pd.Series] = {}
    donor_scores: dict[str, float] = {}

    for donor, group in meta.groupby("donor", sort=True):
        senescent = group.index[group["status"] == "senescent"]
        non_senescent = group.index[group["status"] == "non-senescent"]
        if len(senescent) != 1 or len(non_senescent) != 1:
            continue
        senescent_sample = senescent[0]
        non_senescent_sample = non_senescent[0]
        difference = expression[senescent_sample] - expression[non_senescent_sample]
        difference = difference.replace([np.inf, -np.inf], np.nan).dropna()
        if difference.empty:
            continue
        donor_differences[donor] = difference
        donor_scores[donor] = float(difference.mean())

    if not donor_differences:
        return pd.Series(dtype=float), pd.Series(dtype=float)
    effects = pd.concat(donor_differences, axis=1).mean(axis=1)
    return effects, pd.Series(donor_scores, name="mean_effect")
