#!/usr/bin/env python
"""Scoping audit of multi-cohort claims in an open-access Europe PMC corpus."""

from __future__ import annotations

import argparse
import csv
import json
import re
from pathlib import Path
from xml.etree import ElementTree

import pandas as pd


GSE_PATTERN = re.compile(r"GSE\d+", flags=re.IGNORECASE)
CONSISTENCY_PATTERN = re.compile(r"\bconsisten\w*", flags=re.IGNORECASE)
REPLICATION_PATTERN = re.compile(
    r"\b(?:replicat\w*|reproduc\w*|concordan\w*)\b",
    flags=re.IGNORECASE,
)
GENE_LEVEL_PATTERN = re.compile(
    r"(?:gene[- ]level.{0,80}(?:concordan|same direction)|"
    r"(?:concordan|same direction).{0,80}gene[- ]level)",
    flags=re.IGNORECASE | re.DOTALL,
)
FDR_PATTERN = re.compile(r"\bFDR\b|false discovery", flags=re.IGNORECASE)
PERMUTATION_PATTERN = re.compile(r"\bpermutation\w*", flags=re.IGNORECASE)
POWER_PATTERN = re.compile(r"\bpower\b", flags=re.IGNORECASE)


def _text(element: ElementTree.Element | None) -> str:
    if element is None:
        return ""
    return re.sub(r"\s+", " ", " ".join(element.itertext())).strip()


def audit_article(xml_path: Path) -> dict[str, object]:
    root = ElementTree.parse(xml_path).getroot()
    title = _text(root.find(".//article-title"))
    pmid = ""
    doi = ""
    for article_id in root.findall(".//article-id"):
        if article_id.attrib.get("pub-id-type") == "pmid":
            pmid = _text(article_id)
        elif article_id.attrib.get("pub-id-type") == "doi":
            doi = _text(article_id)
    text = _text(root)
    accessions = sorted(set(match.upper() for match in GSE_PATTERN.findall(text)))
    return {
        "pmcid": xml_path.stem,
        "pmid": pmid,
        "doi": doi,
        "title": title,
        "n_gse": len(accessions),
        "accessions": "|".join(accessions),
        "multi_cohort": len(accessions) >= 2,
        "consistency_language": bool(CONSISTENCY_PATTERN.search(text)),
        "replication_language": bool(REPLICATION_PATTERN.search(text)),
        "gene_level_concordance_language": bool(GENE_LEVEL_PATTERN.search(text)),
        "fdr": bool(FDR_PATTERN.search(text)),
        "permutation": bool(PERMUTATION_PATTERN.search(text)),
        "power": bool(POWER_PATTERN.search(text)),
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("input_dir", type=Path)
    parser.add_argument("output_csv", type=Path)
    parser.add_argument("output_json", type=Path)
    args = parser.parse_args()

    rows = [audit_article(path) for path in sorted(args.input_dir.glob("*.xml"))]
    frame = pd.DataFrame(rows)
    args.output_csv.parent.mkdir(parents=True, exist_ok=True)
    frame.to_csv(args.output_csv, index=False, quoting=csv.QUOTE_MINIMAL)

    summary = {
        "n_articles": int(len(frame)),
        "n_multi_cohort": int(frame["multi_cohort"].sum()),
        "n_consistency_language": int(frame["consistency_language"].sum()),
        "n_replication_language": int(frame["replication_language"].sum()),
        "n_gene_level_concordance_language": int(
            frame["gene_level_concordance_language"].sum()
        ),
        "n_fdr": int(frame["fdr"].sum()),
        "n_permutation": int(frame["permutation"].sum()),
        "n_power": int(frame["power"].sum()),
        "n_multi_cohort_with_consistency_language": int(
            (frame["multi_cohort"] & frame["consistency_language"]).sum()
        ),
        "n_multi_cohort_with_gene_level_concordance_language": int(
            (
                frame["multi_cohort"]
                & frame["gene_level_concordance_language"]
            ).sum()
        ),
    }
    args.output_json.write_text(
        json.dumps(summary, indent=2),
        encoding="utf-8",
    )
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
