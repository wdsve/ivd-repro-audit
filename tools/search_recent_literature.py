#!/usr/bin/env python
"""Search recent PubMed records for discussion citations."""

from __future__ import annotations

import csv
import json
import subprocess
import time
import urllib.parse
from pathlib import Path


EUTILS = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils"
QUERIES = {
    "cross_cohort_transcriptomics": (
        '("transcriptomics"[Title/Abstract] OR "transcriptome"[Title/Abstract]) '
        'AND ("reproducibility"[Title/Abstract] OR "replicability"[Title/Abstract] '
        'OR "cross-cohort"[Title/Abstract] OR "cross-study"[Title/Abstract]) '
        'AND 2023:2026[dp]'
    ),
    "signature_external_validation": (
        '("gene expression signature"[Title/Abstract] OR '
        '"transcriptomic signature"[Title/Abstract]) '
        'AND ("external validation"[Title/Abstract] OR '
        '"reproducibility"[Title/Abstract] OR "replicability"[Title/Abstract]) '
        'AND 2023:2026[dp]'
    ),
    "module_gene_set_reproducibility": (
        '("gene set"[Title/Abstract] OR "module preservation"[Title/Abstract]) '
        'AND ("reproducibility"[Title/Abstract] OR "replicability"[Title/Abstract] '
        'OR "cross-study"[Title/Abstract]) AND 2023:2026[dp]'
    ),
    "public_omics_reanalysis": (
        '("public data"[Title/Abstract] OR "public transcriptome"[Title/Abstract] '
        'OR "secondary analysis"[Title/Abstract]) '
        'AND ("reproducibility"[Title/Abstract] OR "bias"[Title/Abstract] '
        'OR "validation"[Title/Abstract]) AND 2023:2026[dp]'
    ),
    "single_cell_integration_benchmark": (
        '("single-cell"[Title/Abstract] OR "single cell"[Title/Abstract]) '
        'AND ("integration benchmark"[Title/Abstract] OR "batch effect"[Title/Abstract] '
        'OR "reproducibility"[Title/Abstract]) AND 2023:2026[dp]'
    ),
    "musculoskeletal_reproducibility": (
        '("osteoarthritis"[Title/Abstract] OR "intervertebral disc"[Title/Abstract] '
        'OR "musculoskeletal"[Title/Abstract]) '
        'AND ("transcriptomic signature"[Title/Abstract] OR '
        '"gene expression signature"[Title/Abstract]) '
        'AND ("reproducibility"[Title/Abstract] OR '
        '"external validation"[Title/Abstract]) AND 2023:2026[dp]'
    ),
    "computational_reporting_standards": (
        '("computational biology"[Title/Abstract] OR "bioinformatics"[Title/Abstract]) '
        'AND ("reporting standard"[Title/Abstract] OR '
        '"reproducibility standard"[Title/Abstract] OR '
        '"minimum reporting"[Title/Abstract]) AND 2023:2026[dp]'
    ),
}


def _request(endpoint: str, params: dict[str, str | int]) -> dict:
    url = f"{EUTILS}/{endpoint}?{urllib.parse.urlencode(params)}"
    completed = subprocess.run(
        ["curl.exe", "--ssl-no-revoke", "--http1.1", "-sL", url],
        check=True,
        capture_output=True,
        text=True,
    )
    return json.loads(completed.stdout)


def search(query: str, retmax: int = 20) -> list[dict[str, str]]:
    search_result = _request(
        "esearch.fcgi",
        {
            "db": "pubmed",
            "term": query,
            "retmax": retmax,
            "sort": "pub_date",
            "retmode": "json",
        },
    )
    ids = search_result["esearchresult"].get("idlist", [])
    if not ids:
        return []
    summary = _request(
        "esummary.fcgi",
        {
            "db": "pubmed",
            "id": ",".join(ids),
            "retmode": "json",
        },
    )
    rows = []
    for pmid in summary["result"]["uids"]:
        item = summary["result"][pmid]
        doi = ""
        for article_id in item.get("articleids", []):
            if article_id.get("idtype") == "doi":
                doi = article_id.get("value", "")
                break
        rows.append(
            {
                "pmid": pmid,
                "year": item.get("pubdate", ""),
                "journal": item.get("fulljournalname", ""),
                "title": item.get("title", ""),
                "doi": doi,
            }
        )
    return rows


def main() -> None:
    output = Path("results/literature_audit/recent_candidate_papers.csv")
    output.parent.mkdir(parents=True, exist_ok=True)
    rows = []
    for topic, query in QUERIES.items():
        for row in search(query):
            row["topic"] = topic
            rows.append(row)
        time.sleep(0.4)
    with output.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=["topic", "pmid", "year", "journal", "title", "doi"],
        )
        writer.writeheader()
        writer.writerows(rows)
    print(f"wrote {len(rows)} records to {output}")


if __name__ == "__main__":
    main()
