# IVD cross-cohort reproducibility audit

Companion code, derived result tables and figures for the manuscript:

> **Module-level agreement is not replication: a reporting and
> reproducibility gate for public human intervertebral disc transcriptomes**
> (under peer review)

## What it tests

The audit asks whether a gene module that is significant in one public human
intervertebral disc (IVD) cohort reproduces at the gene level in a second
matched cohort. It uses exact sign tests, matched tissue and grade strata,
repeated internal split-half reliability, global-shift diagnostics,
donor-level resampling, phenotype permutation, expression-matched nulls,
Benjamini-Hochberg FDR and reliability-attenuation simulation.

The primary comparison is:

- GSE70362 annulus fibrosus, Thompson grade I-IV, `n = 20`
- GSE23130 laser-capture annulus fibrosus, grade I-IV, `n = 15`

It also audits all available samples, seven prespecified mechanism modules,
1,554 MSigDB Hallmark/KEGG/Reactome modules and 15 public tissue cohort
pairs.

**Key result.** In the strict matched comparison, the ECM remodelling module
is significant in GSE23130 (77.4% of genes up, nominal p = 0.0066), but
gene-level directional concordance with GSE70362 is 23.3%, which does not
exceed chance. Module-level significance alone is therefore not evidence of
cross-cohort replication.

## Repository contents

| Path | Contents |
| --- | --- |
| `run_audit.py` | Main audit driver (all primary and sensitivity analyses) |
| `run_all_audits.py` | Main audit + GSE17077 + GSE176205 + literature scoping in one pass |
| `analyze_gse17077.py` | Paired senescence audit (GSE17077) |
| `analyze_gse176205.py` | NP directional validation (GSE176205) |
| `ivd_audit/` | Analysis package (models, concordance metrics, reporting) |
| `tools/` | Sensitivity analyses, manuscript/supplement builders, QA rendering |
| `tests/` | Unit tests for the core statistics |
| `results/` | Derived effect tables, diagnostics and audit outputs |
| `figures/` | Publication figures (PNG + PDF) |
| `manuscript/` | Manuscript source (EN/ZH), supplement, abstracts |
| `jbi_submission/` | Built journal submission package (DOCX/PDF, separate figures) |
| `docs/` | Frozen analysis plan, cohort registries, submission notes |
| `bundled_data/` | Small derived input tables (see Data setup) |

## Requirements

- Python 3.11 or newer
- Dependencies: `pip install -r requirements.txt`

## Data setup

All source data are public. The analysis code reads raw files from
`<project_root>/ldh_pipeline/data/`, where `project_root` defaults to the
parent directory of this repository clone (override with `--project-root`).

From the repository root, run:

```bash
python tools/download_data.py
```

The script downloads the public GEO series matrices (GSE70362, GSE23130,
GSE176205), the GPL1352 platform annotation and the NCBI gene info file, and
copies the small derived tables bundled in `bundled_data/` (external blood
cohort metadata and the 15-cohort-pair effect table) into the expected
layout. It then prints instructions for the one manual step: three MSigDB
2024.1 GMT files, which require a free registration at
<https://www.gsea-msigdb.org/gsea/msigdb/>.

GSE17077 inputs are passed as command-line arguments; see
`analyze_gse17077.py --help`. The literature scoping audit
(`tools/scoping_literature_audit.py`) takes a directory of Europe PMC
full-text XML files as input.

## Reproduce the analysis

From the repository root:

```bash
python run_audit.py            # main audit (see --help for replicate counts)
python run_all_audits.py       # everything, including secondary audits
python tools/build_jbi_submission.py   # rebuild the submission DOCX package
python -m unittest discover -s tests -v
```

The main run uses 199 phenotype permutations, 5,000 matched-set permutations,
300 donor resampling replicates per model and 100 split-half repetitions.
`run_audit.py` regenerates the tables in `results/`, the figures in
`figures/` and the manuscript source in `manuscript/`.

The frozen statistical plan is in `docs/analysis_plan_v2.md`.

## License and citation

Code is released under the MIT License (see `LICENSE`). The archived release
is available on Zenodo:

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.23133983.svg)](https://doi.org/10.5281/zenodo.23133983)

If you use this code or the derived tables, please cite the archived release
(see `CITATION.cff`): Liu Z. *Module-level agreement is not replication: a
reporting and reproducibility gate for public human intervertebral disc
transcriptomes - companion code* (v1.0.0). Zenodo.
https://doi.org/10.5281/zenodo.23133983
