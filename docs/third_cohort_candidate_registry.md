# Third-cohort candidate screen

Date: 2026-09-19

## Decision summary

- No true Tier A cohort has been identified.
- `GSE17077` was initially reported by secondary papers as a normal versus
  degenerated AF cohort, but the official GEO record corrects this: it
  profiles senescent versus non-senescent laser-capture annulus cells
  (19 samples from 11 donors). It is not a severity cohort.
- `GSE176205` remains the best verified independent directional validation
  cohort: human nucleus pulposus, 3 controls and 6 degeneration samples,
  with raw counts and FPKM.
- `GSE15227` remains a same-platform technical control, but independence from
  the other Gruber cohorts must be verified.
- `GSE230808`, `GSE244889`, `GSE165722` and `GSE199866` are single-cell
  resources and can only be used for donor-level pseudobulk validation.

## GSE17077

Official title:

> Gene Expression Data from Senescent vs Non-senescent Cells in the in Vivo
> Human Annulus

The official description uses laser-capture microdissection to harvest
senescent and non-senescent annulus cells from 11 human specimens. The GEO
record contains 19 samples. This makes it useful for senescence-module
validation and paired cell-state comparisons, but not for degeneration-grade
or cross-cohort severity replication.

The local paired analysis used the eight donors with both senescent and
non-senescent samples. The global paired effect showed no matrix-wide shift
(42.5% positive, median effect -0.013). The ECM module was not directionally
enriched in senescent cells (13/31 genes positive, 41.9%, one-sided sign
p = 0.86). No prespecified mechanism module showed a positive directional
signal. These results are retained as a contrast-specific supplement, not as
severity replication.

## Rejected or downgraded accessions

- `GSE41883`: TNF-alpha stimulation of annulus fibrosus cells, not a cohort.
- `GSE27494`: IL-1beta stimulation of annulus fibrosus cells, not a cohort.
- `GSE147383`: only four donors with paired AF/NP, not a large cohort.
- `GSE129789`: IVD tissue with Pfirrmann grades, but methylation rather than
  transcriptome.
- `GSE151090`, `GSE112216`, `GSE114169`, `GSE245147`: in-vitro or
  cell-level experiments.
- `GSE110804`: cell-perturbation dataset rather than a patient cohort.
- `E-MTAB-11554`: miRNA microarray.
- `E-MTAB-15392`: proteomics.
- `GSE252383`, `GSE252474`, `GSE134955`, `GSE188909`: mouse models.
- `GSE290270`, `GSE290271`: hydrogel/exosome intervention studies.

Unverified smaller candidates retained for metadata checks:

- `GSE59485`: possible small human NP tissue cohort.
- `GSE7362`: organism and design unresolved.
- `GSE13904`: organism and design unresolved.
- `GSE153761`: used in mixed blood/tissue models and not yet proven to be a
  clean independent tissue cohort.

## Search artifacts

- `results/third_cohort_search/europepmc_accession_contexts.csv`
- `results/third_cohort_search/key_candidate_contexts.csv`
- `results/third_cohort_search/candidate_registry.csv`
