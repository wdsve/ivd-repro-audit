"""Readers for the public cohort files used by the reproducibility audit."""

from __future__ import annotations

import csv
import gzip
from pathlib import Path

import pandas as pd


def parse_series_matrix_text(text: str) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Parse a GEO series matrix into probe expression and sample metadata."""
    lines = text.splitlines()
    metadata_lines: list[list[str]] = []
    in_table = False
    table_rows: list[list[str]] = []

    for line in lines:
        if line.startswith("!Sample_"):
            metadata_lines.append(next(csv.reader([line], delimiter="\t")))
        elif line.startswith("!series_matrix_table_begin"):
            in_table = True
        elif line.startswith("!series_matrix_table_end"):
            in_table = False
        elif in_table and line.strip():
            table_rows.append(next(csv.reader([line], delimiter="\t")))

    if not table_rows:
        raise ValueError("series matrix contains no expression table")

    sample_ids: list[str] | None = None
    pending_titles: list[str] | None = None
    metadata_by_sample: dict[str, dict[str, str]] = {}
    for row in metadata_lines:
        tag = row[0].removeprefix("!Sample_")
        values = row[1:]
        if tag == "geo_accession":
            sample_ids = values
            metadata_by_sample = {sample: {} for sample in values}
            if pending_titles is not None:
                for sample, value in zip(sample_ids, pending_titles):
                    metadata_by_sample[sample]["title"] = value.strip()
            continue
        if sample_ids is None:
            if tag == "title":
                pending_titles = values
            continue
        if tag == "title":
            for sample, value in zip(sample_ids, values):
                metadata_by_sample[sample]["title"] = value.strip()
            continue
        for sample, value in zip(sample_ids, values):
            if ":" in value:
                key, parsed_value = value.split(":", 1)
                metadata_by_sample[sample][key.strip()] = parsed_value.strip()

    metadata = pd.DataFrame.from_dict(metadata_by_sample, orient="index")

    header = table_rows[0]
    sample_columns = header[1:]
    records: dict[str, list[float]] = {}
    for row in table_rows[1:]:
        if len(row) != len(header):
            continue
        try:
            records[row[0]] = [float(value) for value in row[1:]]
        except ValueError:
            continue
    expression = pd.DataFrame.from_dict(records, orient="index", columns=sample_columns)
    expression.index.name = "probe"
    metadata.index.name = "sample"
    return expression, metadata


def read_series_matrix(path: str | Path) -> tuple[pd.DataFrame, pd.DataFrame]:
    matrix_path = Path(path)
    if matrix_path.suffix == ".gz":
        with gzip.open(matrix_path, "rt", encoding="utf-8", errors="replace") as handle:
            text = handle.read()
    else:
        text = matrix_path.read_text(encoding="utf-8", errors="replace")
    return parse_series_matrix_text(text)


def read_gmt(path: str | Path) -> dict[str, set[str]]:
    """Read an MSigDB GMT file, returning Entrez identifiers."""
    gene_sets: dict[str, set[str]] = {}
    with Path(path).open(encoding="utf-8", errors="replace") as handle:
        for line in handle:
            fields = line.rstrip("\n").split("\t")
            if len(fields) < 3:
                continue
            gene_sets[fields[0]] = {field.strip() for field in fields[2:] if field.strip()}
    return gene_sets
