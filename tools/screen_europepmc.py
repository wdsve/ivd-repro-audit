#!/usr/bin/env python
"""Extract accession contexts from Europe PMC JATS XML bundles."""

from __future__ import annotations

import argparse
import csv
import re
from pathlib import Path
from xml.etree import ElementTree


ACCESSION_PATTERN = re.compile(
    r"(?:GSE\d+|PRJNA\d+|E-MTAB-\d+|SRP\d+)",
    flags=re.IGNORECASE,
)


def _text(element: ElementTree.Element | None) -> str:
    if element is None:
        return ""
    return re.sub(r"\s+", " ", " ".join(element.itertext())).strip()


def extract_accession_contexts(
    xml_path: Path,
    context_chars: int = 220,
) -> list[dict[str, str]]:
    root = ElementTree.parse(xml_path).getroot()
    article_title = _text(root.find(".//article-title"))
    pmid = ""
    doi = ""
    for article_id in root.findall(".//article-id"):
        if article_id.attrib.get("pub-id-type") == "pmid":
            pmid = _text(article_id)
        elif article_id.attrib.get("pub-id-type") == "doi":
            doi = _text(article_id)
    body = _text(root)
    rows: list[dict[str, str]] = []
    seen: set[tuple[str, str]] = set()
    for match in ACCESSION_PATTERN.finditer(body):
        accession = match.group(0).upper()
        context = body[
            max(0, match.start() - context_chars) : match.end() + context_chars
        ]
        key = (accession, context)
        if key in seen:
            continue
        seen.add(key)
        rows.append(
            {
                "accession": accession,
                "pmcid": xml_path.stem,
                "pmid": pmid,
                "doi": doi,
                "article_title": article_title,
                "context": context,
            }
        )
    return rows


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("input_dir", type=Path)
    parser.add_argument("output_csv", type=Path)
    parser.add_argument("--context-chars", type=int, default=220)
    parser.add_argument(
        "--accessions",
        default="",
        help="Comma-separated accession allowlist.",
    )
    args = parser.parse_args()

    accession_filter = {
        value.strip().upper()
        for value in args.accessions.split(",")
        if value.strip()
    }
    rows: list[dict[str, str]] = []
    for xml_path in sorted(args.input_dir.glob("*.xml")):
        rows.extend(
            row
            for row in extract_accession_contexts(
                xml_path,
                context_chars=args.context_chars,
            )
            if not accession_filter or row["accession"] in accession_filter
        )

    args.output_csv.parent.mkdir(parents=True, exist_ok=True)
    with args.output_csv.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)
    print(f"wrote {len(rows)} accession contexts to {args.output_csv}")


if __name__ == "__main__":
    main()
