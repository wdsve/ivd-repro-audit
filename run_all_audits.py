#!/usr/bin/env python
"""Run the main, supplementary and literature audits in dependency order."""

from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path


def _run(command: list[str], workdir: Path) -> None:
    print("+", " ".join(str(value) for value in command))
    subprocess.run(command, cwd=workdir, check=True)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--project-root",
        type=Path,
        default=Path(__file__).resolve().parents[1],
    )
    parser.add_argument(
        "--europepmc-dir",
        type=Path,
        default=Path("D:/edge保存/分析加机器学习/europepmc_open_access_v2"),
    )
    args = parser.parse_args()
    root = args.project_root.resolve()
    project = Path(__file__).resolve().parent

    _run(
        [
            sys.executable,
            "run_audit.py",
            "--project-root",
            str(root),
            "--skip-manuscript",
        ],
        project,
    )
    _run(
        [
            sys.executable,
            "tools/probe_collapse_sensitivity.py",
            "--project-root",
            str(root),
            "--random-repetitions",
            "100",
        ],
        project,
    )
    _run(
        [
            sys.executable,
            "tools/gene_identity_sensitivity.py",
            "--project-root",
            str(root),
        ],
        project,
    )
    _run(
        [
            sys.executable,
            "tools/scale_invariance_sensitivity.py",
            "--project-root",
            str(root),
        ],
        project,
    )
    _run(
        [
            sys.executable,
            "tools/module_family_sensitivity.py",
            "--project-root",
            str(root),
        ],
        project,
    )
    _run(
        [
            sys.executable,
            "analyze_gse17077.py",
            "--series-matrix",
            str(root / "GSE17077_series_matrix.txt.gz"),
            "--annotation",
            str(root / "ldh_pipeline/data/raw/GSE23130/GPL1352.annot.gz"),
            "--output-dir",
            "results/GSE17077_senescence",
        ],
        project,
    )
    _run(
        [
            sys.executable,
            "analyze_gse176205.py",
            "--project-root",
            str(root),
            "--output-dir",
            "results/GSE176205_NP_validation",
        ],
        project,
    )
    if args.europepmc_dir.exists():
        _run(
            [
                sys.executable,
                "tools/scoping_literature_audit.py",
                str(args.europepmc_dir),
                "results/literature_audit/europepmc_scoping_audit.csv",
                "results/literature_audit/europepmc_scoping_summary.json",
            ],
            project,
        )
    else:
        print(f"Europe PMC directory not found, skipping: {args.europepmc_dir}")

    _run(
        [
            sys.executable,
            "-c",
            "from pathlib import Path; "
            "from ivd_audit.report import write_manuscript; "
            "write_manuscript(Path('.').resolve())",
        ],
        project,
    )
    _run(
        [
            sys.executable,
            "tools/citation_lint.py",
            "--project-root",
            str(root),
        ],
        project,
    )


if __name__ == "__main__":
    main()
