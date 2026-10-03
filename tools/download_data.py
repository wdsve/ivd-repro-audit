#!/usr/bin/env python
"""Download the public input data required by the audit.

The analysis code reads raw data from ``<project_root>/ldh_pipeline/data/``.
By default ``project_root`` is the parent directory of this repository, which
matches the default of ``run_audit.py``. Use ``--project-root`` to choose a
different location.

This script downloads all files that are publicly fetchable without
registration (GEO series matrices, GEO platform annotation, NCBI gene info)
and copies the small derived tables bundled in ``bundled_data/`` into the
expected layout. The three MSigDB GMT files require a free registration and
must be downloaded manually; the script prints instructions for them.
"""

from __future__ import annotations

import argparse
import shutil
import sys
import urllib.request
from pathlib import Path

GEO_FTP = "https://ftp.ncbi.nlm.nih.gov/geo"

DOWNLOADS = {
    "ldh_pipeline/data/raw/GSE70362/GSE70362_series_matrix.txt.gz": (
        f"{GEO_FTP}/series/GSE70nnn/GSE70362/matrix/GSE70362_series_matrix.txt.gz"
    ),
    "ldh_pipeline/data/raw/GSE23130/GSE23130_series_matrix.txt.gz": (
        f"{GEO_FTP}/series/GSE23nnn/GSE23130/matrix/GSE23130_series_matrix.txt.gz"
    ),
    "ldh_pipeline/data/raw/GSE23130/GPL1352.annot.gz": (
        f"{GEO_FTP}/platforms/GPL1nnn/GPL1352/annot/GPL1352.annot.gz"
    ),
    "ldh_pipeline/data/raw/annotation/Homo_sapiens.gene_info.gz": (
        "https://ftp.ncbi.nlm.nih.gov/gene/DATA/GENE_INFO/Mammalia/"
        "Homo_sapiens.gene_info.gz"
    ),
    "ldh_pipeline/data/raw/GSE176205/GSE176205_series_matrix.txt.gz": (
        f"{GEO_FTP}/series/GSE176nnn/GSE176205/matrix/"
        "GSE176205_series_matrix.txt.gz"
    ),
    "ldh_pipeline/data/raw/GSE176205/"
    "GSE176205_mRNA_Expression_Profiling_upload.txt.gz": (
        f"{GEO_FTP}/series/GSE176nnn/GSE176205/suppl/"
        "GSE176205_mRNA_Expression_Profiling_upload.txt.gz"
    ),
}

MSIGDB_FILES = [
    "h.all.v2024.1.Hs.entrez.gmt",
    "c2.cp.kegg_legacy.v2024.1.Hs.entrez.gmt",
    "c2.cp.reactome.v2024.1.Hs.entrez.gmt",
]


def _download(url: str, target: Path) -> None:
    target.parent.mkdir(parents=True, exist_ok=True)
    if target.exists():
        print(f"  skip (exists): {target}")
        return
    print(f"  downloading: {url}")
    print(f"            -> {target}")
    urllib.request.urlretrieve(url, target)  # noqa: S310 (fixed NCBI URLs)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--project-root",
        type=Path,
        default=Path(__file__).resolve().parents[2],
        help="Directory that will contain ldh_pipeline/data/ "
        "(default: parent of this repository, matching run_audit.py).",
    )
    args = parser.parse_args()
    root = args.project_root.resolve()
    repo = Path(__file__).resolve().parents[1]

    print(f"Project root: {root}")
    print("\n[1/3] Downloading public files from NCBI/GEO ...")
    for relative, url in DOWNLOADS.items():
        _download(url, root / relative)

    print("\n[2/3] Copying bundled derived tables ...")
    bundled = repo / "bundled_data"
    for source in sorted(bundled.rglob("*")):
        if source.is_file():
            target = root / source.relative_to(bundled)
            target.parent.mkdir(parents=True, exist_ok=True)
            if not target.exists():
                shutil.copy2(source, target)
            print(f"  {source.relative_to(bundled)} -> {target}")

    print("\n[3/3] MSigDB files (manual step, free registration required):")
    print("  1. Register and log in at https://www.gsea-msigdb.org/gsea/msigdb/")
    print("  2. Download the 2024.1 Human GMT files:")
    for name in MSIGDB_FILES:
        print(f"       - {name}")
    print(f"  3. Place them in: {root / 'ldh_pipeline/data/raw/msigdb/'}")

    print("\nDone. Verify with: python run_audit.py --help")
    return 0


if __name__ == "__main__":
    sys.exit(main())
