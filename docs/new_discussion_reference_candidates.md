# Selected supplementary references and citation map

Date updated: 2026-09-27

Eleven supplied PDFs were screened against the final English and Chinese
manuscripts. References are now numbered in first-citation order across the
full 29-item bibliography. The first citation appears in the Introduction.
Publication details should be rechecked at submission because some 2026
records are online-first or still being indexed.

## Applied citation map

Full original quotations and exact manuscript paragraph locations are in
`Citation Source Map.md`.

| Ref | Work | Manuscript location | Paragraph location and purpose |
|---|---|---|---|
| [12] | Sporadic CJD cross-omic comparison | Introduction; Discussion > Principal finding | Supports separating FDR-controlled overlap from nominal exploratory gene-set recurrence. |
| [2] | Glioma random-signature audit | Introduction; Discussion > Principal finding | Supports clinical-reference and random-signature null comparisons. |
| [11] | TransPro gene-selection benchmarking | Introduction; Discussion > Why this matters | Supports coexpression bias and the need to validate gene-level behaviour explicitly. |
| [22] | Eleven-gene sepsis signature | Discussion > Why this matters | Supports context-dependent portability across clinical validation settings. |
| [23] | NLRP3-anchored ICU sepsis score | Discussion > Why this matters | Supports cell-composition sensitivity and explicit boundaries between observational transcriptomic state and target engagement. |
| [24] | RSPO2+ NP single-cell and spatial study | Discussion > Why this matters; Limitations | Used only as IVD biological context for WNT/FN1-CD44 and fibrotic NP states. |
| [25] | ITGBL1/RPN1 fibrotic NP study | Discussion > Why this matters; Limitations | Used only as IVD biological context for fibrotic NP and integrin/N-glycosylation programmes. |
| [26] | Cell-type annotation best practices | Discussion > Reporting recommendation | Supports validated or consensus-based annotation. |
| [27] | Cell-type-resolved pseudobulk preprint | Discussion > Reporting recommendation | Supports held-out donor and pseudobulk evaluation rather than treating cells as independent. |
| [28] | FAIR Digital Objects with DataPLANT | Discussion > Reporting recommendation; Data availability | Supports machine-readable metadata and executable workflow provenance. |
| [29] | Hashtag-assisted pooling designs | Discussion > Reporting recommendation | Supports explicit reporting of batch-effect mitigation versus demultiplexing cell loss in cell-resolved designs. |

## Highest-priority methodological citations

### 1. Random-signature and clinical-reference nulls [Article ref 2]

**Glioma transcriptomic signature audit.**

- Diagnostics (Basel). 2026.
- PMID: 42739233
- DOI: 10.3390/diagnostics16172803

Use in Discussion:

- A signature can look well calibrated and still add no measurable value over
  a clinical reference model.
- Against random gene sets of the same size, discrimination can be
  indistinguishable externally.
- Concordance indices cannot be interpreted without clinical and
  random-signature references.

This is the strongest new citation for the section "Why module significance
is not enough".

### 2. Single-subject and small-cohort validation of omics signatures [not inserted]

**Minimalist single-subject analysis for case-control omics signatures.**

- Journal of the American Medical Informatics Association. 2026.
- PMID: 42093161
- DOI: 10.1093/jamia/ocag061

Use in Discussion:

- Conventional case-control transcriptomic signatures fail to reproduce
  consistently at very small sample sizes.
- Paired within-person designs can provide an alternative validation axis in
  rare or highly stratified disease.
- The method emphasizes pathway concordance rather than exact gene-level
  identity, which is a useful contrast to the gene-level gate used here.

### 3. Co-expression bias in differential gene selection [Article ref 11]

**TransPro benchmarking and bias correction.**

- GigaScience. 2026.
- PMID: 42148814
- DOI: 10.1093/gigascience/giag057

Use in Discussion:

- Marginal per-gene tests can be biased by gene-gene co-expression patterns.
- Reproducible gene selection requires interaction-aware or bias-corrected
  workflows.
- This supports the manuscript's argument that gene-level behavior cannot be
  inferred from module aggregation alone.

### 4. Gene-level and gene-set-level reproducibility in public cross-omic data [Article ref 12]

**Cross-omic comparative analysis in sporadic Creutzfeldt-Jakob disease.**

- International Journal of Molecular Sciences. 2026;27(15):6560.
- PMID: 42589231
- DOI: 10.3390/ijms27156560

Use in Discussion:

- Public cross-omic datasets are limited by tissue source and platform.
- Gene-level overlap can be limited even when nominal gene-set signals recur.
- FDR-controlled overlap and nominal exploratory overlap must be separated
  explicitly.

This is almost a conceptual sibling of the current manuscript.

### 5. Exploratory cross-cohort assessment and outcome-language boundaries [Article ref 23]

**NLRP3-anchored transcriptomic score in ICU sepsis with exploratory
cross-cohort assessment.**

- Inflammation Research. 2026.
- PMID: 42700257
- DOI: 10.1007/s00011-026-02352-0

Use in Discussion:

- Cross-cohort directional concordance can remain imprecise.
- Association can be sensitive to estimated cell composition.
- The paper explicitly limits itself to an observational transcriptomic
  state and does not claim causal target engagement.

### 6. Portability across public cohorts and clinical sub-contexts [Article ref 22]

**Eleven-gene sepsis blood transcriptomic signature across public cohorts.**

- Frontiers in Medicine. 2026;13:1844619.
- PMID: 42396135
- DOI: 10.3389/fmed.2026.1844619

Use in Discussion:

- A score may show moderate portability in one clinical contrast and near-null
  discrimination in other contrasts.
- External validation must match the validation context to the claim.
- This supports separating "portable across public cohorts" from "valid for
  every clinical endpoint".

## Technical reproducibility and annotation

### 7. Batch effects and cell loss in pooled single-cell designs [Article ref 29]

**Moderated hashtag-assisted pooling designs.**

- Genome Research. 2026.
- PMID: 42532835
- DOI: 10.1101/gr.281624.125

Use in Discussion:

- Pooling can reduce batch effects but also remove cells during
  demultiplexing.
- Experimental design choices directly affect the data retained for
  pseudobulk and cross-cohort comparison.

### 8. Cell-type annotation and cross-study reproducibility [Article ref 26]

**Annotation of cell types in single-cell sequencing.**

- International Journal of Biochemistry and Cell Biology. 2026.
- PMID: 42716373
- DOI: 10.1016/j.biocel.2026.107027

Use in Discussion:

- Annotation accuracy depends more on reference quality than on algorithmic
  sophistication.
- Misannotation causes systematic mechanistic bias and undermines cross-study
  reproducibility.
- Ensemble consensus using independent annotation methods is more robust.

This supports the manuscript's broader warning that cell-type labels are not
self-validating.

### 9. Cross-cohort pseudobulk classification [Article ref 27]

**Cell-type-resolved pseudobulk classification across independent cohorts.**

- bioRxiv preprint. 2026.
- PMID: 41993387
- DOI: 10.64898/2026.04.07.717029

Use in Discussion only as a preprint:

- Donor-level pseudobulk can generalize across independent single-cell
  cohorts.
- The key unit is the cell type and donor, not individual cells.
- This is useful for proposing the next stage of the present analysis.

### 10. FAIR workflows and traceable analysis [Article ref 28]

**ARC and FAIR Digital Objects with DataPLANT.**

- Journal of Integrative Bioinformatics. 2026.
- PMID: 42307005
- DOI: 10.1515/jib-2025-0056

Use in Discussion:

- Machine-readable metadata and executable workflows improve reproducibility
  and reuse.
- Analysis context and parameter changes should be traceable.

## Recent IVD-specific citations

### 11. Spatial and single-cell NP state [Article ref 24]

**RSPO2-positive NP cells and WNT/FN1-CD44 axis.**

- Journal of Orthopaedic Translation. 2026;60:101203.
- PMID: 42668501
- DOI: 10.1016/j.jot.2026.101203

Use in Discussion:

- Supports current IVD interest in fibrotic NP cell states and FN1-CD44
  signaling.
- Useful for separating biological plausibility from cross-cohort
  reproducibility.

### 12. Fibrotic NP subpopulation [Article ref 25]

**ITGBL1 and RPN1 in a fibrotic NP subpopulation.**

- Journal of Inflammation Research. 2026;19:629922.
- PMID: 42733874
- DOI: 10.2147/JIR.S629922

Use in Discussion:

- Recent independent evidence for fibrotic NP cell states and integrin-linked
  programs.
- Cite as biological context, not as replication of the present ECM module.

## Suggested placement

| Manuscript location | New citations |
|---|---|
| Introduction, module aggregation problem | 42148814 |
| Discussion, random-signature and clinical reference | 42739233 |
| Discussion, small-cohort validation alternatives | 42093161 |
| Discussion, public cross-omic replication | 42589231 |
| Discussion, exploratory cross-cohort language | 42700257 |
| Discussion, clinical context portability | 42396135 |
| Discussion, single-cell and pseudobulk limits | 42532835, 42716373, 41993387 |
| Discussion, FAIR workflows | 42307005 |
| Introduction/Discussion, IVD biological context | 42668501, 42733874 |

## Search artifacts

- `results/literature_audit/recent_candidate_papers.csv`
- `results/literature_audit/selected_recent_abstracts.xml`
