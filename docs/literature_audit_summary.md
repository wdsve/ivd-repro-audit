# Literature scoping audit

Date: 2026-09-21

## Corpus

- Source: Europe PMC open-access full-text export
- Query: articles mentioning GSE70362 or GSE23130 plus IVD terms
- Articles with usable XML: 95
- This is a scoping audit, not a PRISMA systematic review.

## Language and analysis fields

| Field | Articles |
|---|---:|
| More than one distinct GSE | 79 |
| Consistency language | 71 |
| Replication/reproducibility/concordance language | 84 |
| Multi-cohort plus consistency language | 62 |
| Gene-level concordance language | 0 |
| FDR or false-discovery language | 35 |
| Permutation language | 9 |
| Power language | 35 |

The gene-level field required explicit gene-level concordance or same-direction
language. Its absence is not proof that no concordance analysis was performed;
it means the analysis was not described with that terminology in the
open-access full text.

## Manuscript use

The audit supports a limited statement:

> In a scoping corpus of 95 open-access IVD transcriptome articles, 79 used
> more than one GSE and 62 combined multi-cohort use with consistency
> language, while no article described gene-level concordance using the
> prespecified text criteria.

It does not establish prevalence across the whole IVD literature.

## Artifacts

- `results/literature_audit/europepmc_scoping_audit.csv`
- `results/literature_audit/europepmc_scoping_summary.json`
