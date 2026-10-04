# Module-level agreement is not replication: a reporting and reproducibility gate for public human intervertebral disc transcriptomes

## Abstract

**Background.** Public transcriptome reanalyses in intervertebral disc (IVD)
research frequently interpret a pathway or module that is significant in one
cohort, or directionally concordant across cohorts, as evidence of
reproducibility. This interpretation ignores the possibility that the module
direction is driven by a different gene subset in each cohort.

**Methods.** We audited six public human IVD tissue transcriptome cohorts and
used the two largest graded annulus fibrosus cohorts, GSE70362 and GSE23130,
for a matched analysis. We compared all available samples with a strict
sample set restricted to Thompson grade I-IV, annulus fibrosus, and
laser-capture microdissection. Effects were estimated with linear models
adjusted for available technical variables. For every gene set we reported
the module direction in each cohort, exact and permutation p-values, and
gene-level sign concordance between cohorts. We additionally audited 1,554
Hallmark, KEGG and Reactome modules and 15 tissue cohort pairs. Internal
reproducibility was measured by repeated stratified split-half analyses;
for GSE70362, where donor identifiers were available, donor-level
one-sample and cluster-bootstrap analyses were used to assess within-donor
dependence; GSE23130 donor identifiers were unavailable. Global-shift,
processing-confound, multiple-testing and reliability-attenuation checks
were performed before interpretation.

**Results.** In the strict comparison, the ECM remodelling module increased in
77.4% of measured genes in GSE23130
(sign-test p = 0.0017) but in only
46.7% of genes in GSE70362
(p = 0.7077). Gene-level sign concordance was
23.3% (two-sided exact sign p =
0.0052), below the 50% expected
under independent directions. This below-chance level was specific to the
primary highest-mean-probe rule; alternative probe collapsing did not exceed
50% but was less extreme (random-probe median 36.7%). Donor-level resampling preserved a
median GSE70362 ECM fraction up near 50% and a median cross-cohort
concordance of approximately 30%. The ECM module showed moderate internal
reliability in both cohorts (split-half Spearman rho
0.37 and 0.41). Cross-half positive controls reached
median concordance values of 63.3% and 64.5%, above the cross-cohort value of
23.3%. Power calibration nevertheless showed that the nominal 30-gene test had
only 20.4% power at a latent correlation of 0.6. The result is a failure to
establish replication, not proof that shared biology is absent. Across 1,554
curated modules,
673 were significant in only one
cohort and 31 in both;
14 passed the additional gene-level
concordance gate at nominal p-values, but
0 survived the exact sign-test FDR gate.
An alias-aware gene-identity sensitivity did not change the strict result.
Phenotype permutation and expression-matched nulls were retained as
sensitivity analyses. Across 15 IVD tissue cohort pairs, the median gene-level sign
concordance was 49.4%
and the highest was 58.6%.
No Tier A third AF severity cohort was identified despite targeted searching.
In a scoping corpus of 95 open-access IVD
transcriptome articles, 79 used more than
one GSE and 62
combined multi-cohort use with consistency language, whereas no article
described gene-level concordance using the prespecified text criteria.

**Conclusions.** In public human IVD transcriptomes, module-level significance
does not establish cross-cohort replication. A reproducible claim should
require the same prespecified gene set to move in the same direction in an
independent cohort at the gene level, not only at the module level. We
operationalise this distinction as a five-level claim ladder, from exploratory
single-cohort signals to FDR-controlled gene-level replication.

**Keywords.** reproducibility; transcriptomics; bioinformatics; gene-sets; intervertebral-disc

## Significance statement

Public-data transcriptome studies often have too few independent cohorts for
biological replication, yet multi-cohort studies commonly use consistency
language. This audit shows that a module can be strongly significant,
internally reproducible, and still fail gene-level cross-cohort concordance.
The practical recommendation is simple: report module direction and
gene-level sign concordance together, and treat either layer alone as
hypothesis-generating.

## Introduction

Intervertebral disc degeneration is studied with many small human
transcriptome cohorts that differ in tissue compartment, RNA processing,
platform, degeneration scale, and clinical endpoint. In a scoping corpus of
95 open-access IVD transcriptome articles,
79 used more than one GSE and
62 combined
multi-cohort use with consistency language. None described gene-level
concordance using the prespecified text criteria. Reanalyses therefore may use
public cohorts to support a module by citing a significant enrichment in one
dataset and a directionally similar result in another without showing that the
same genes replicate. Comparable cross-omic and prognostic-signature audits
have shown that nominal gene-set recurrence and apparently good discrimination
can coexist with limited gene-level overlap or performance indistinguishable
from suitable null models [1,2]. These concerns align with long-standing
analyses of research validity [3] and systematic replication projects, where
most replication effect sizes were smaller than the original estimates [4].
The Open Science Collaboration similarly found replication effects about half
the magnitude of original effects [5].

That argument has a blind spot. A module may be enriched because 80% of its
genes move in one direction in cohort A and 55% move in the same direction in
cohort B, even while the individual genes that drive the signal differ.
Module membership is not evidence that the same biological programme is
active. Gene-level sign concordance is the missing check. This concern is
reinforced by transcriptomic benchmarking showing that marginal gene-by-gene
selection can be biased by coexpression structure, so aggregation may not
represent the gene-level behaviour required for replication [6].

We therefore built a reproducibility audit around public human IVD
transcriptomes (Figure 1). The audit asks four questions. First, are the compared
samples measuring the same tissue and endpoint? Second, could a global shift,
processing confound, or detection-depth difference explain the apparent
effect? Third, is the module internally reproducible? Fourth, do the same
genes move in the same direction in an independent cohort?

The audit is not a new pathway discovery study. It is a negative-control and
reporting framework for public-data claims, using gene sets that were fixed
before the cross-cohort comparison. It contributes three elements: a matched
IVD case study, a reusable gene-level reproducibility gate, and a claim ladder
that separates exploratory, internally stable, contextually concordant,
candidate-replicated and FDR-controlled claims. The contribution is not a new
statistical test or algorithm. It is the integration of domain-matched
evidence, operational claim gates, and sensitivity analyses spanning donor
dependence, probe selection, gene identity, scale and FDR-family structure.

## Methods

### Data sources

We used the public human IVD tissue cohorts already present in the analysis
workspace. The primary graded comparison used GSE70362 (annulus fibrosus and
nucleus pulposus; Thompson grades I-V) and GSE23130 (annulus fibrosus;
histological grades I-V). Additional tissue cohorts were GSE186542,
GSE167199, GSE146904 and GSE207176. The reproducibility analysis did not use
the blood cohorts because the question concerned tissue programme
transferability, not blood-versus-tissue generality. GEO is an international
public repository that archives raw data, processed data and metadata for
high-throughput functional genomic datasets [7]. GSE70362 was originally
reported by Kazezian et al. [8], GSE23130 by Gruber et al. [9], and
GSE167199 by Li et al. [10].

The strict primary analysis used 20 GSE70362 annulus fibrosus samples of
Thompson grade I-IV and 15 GSE23130 laser-capture samples of grade I-IV. The
all-sample comparison used 24 GSE70362 annulus fibrosus samples and all 23
GSE23130 samples.

### Analysis timing and prespecification

An internal analysis plan was frozen on 2026-09-16 before the final
permutation run. It is available as `Frozen Analysis Plan.md` and
`docs/analysis_plan_v2.md`. It was not publicly preregistered. In this
manuscript, "prespecified" therefore means that the final sensitivity
analyses and claim language were fixed before that run, not that the whole
investigation was prospective, blinded or registered in advance. Earlier
exploratory work informed cohort and endpoint selection. The audit should
therefore be read as a transparent retrospective analysis with an internal
freeze rather than a publicly registered prospective study.

### Harmonisation and effect estimation

GEO series matrices were parsed directly. Probes were mapped to Entrez or
gene symbols using the supplied platform annotations and the human gene_info
table. When multiple probes mapped to one symbol, the probe with the highest
mean expression was retained as the primary rule. Sensitivity analyses also
used the first probe, the median across probes, and repeated random-probe
selection. The primary gene-identity rule retained supplied platform symbols;
an alias-aware sensitivity additionally mapped historical symbols through
current synonyms and nomenclature-authority symbols.

For each cohort we fitted gene-wise linear models to the normalized
expression matrix. Direction was defined as increasing with degeneration
grade. The strict GSE70362 model included grade and batch; the strict
GSE23130 model included grade and tissue source. The all-sample GSE23130
model also included processing method. The all-sample GSE70362 model used the
annulus fibrosus subset to reduce tissue heterogeneity. We used an in-house
ordinary least-squares implementation rather than the limma package itself;
limma provides the reference framework for gene-wise linear models of
high-throughput expression data [11].

Grade was used only as a strictly increasing ordinal score: I = 1, I-II =
1.5, II = 2, III = 3 and IV = 4. The reported direction is the sign of a
gene-wise monotone trend. Any strictly increasing recoding of the same grade
order preserves that sign; coefficient magnitudes are scale-dependent and are
not interpreted as equal-step dose responses. The analysis does not test
arbitrary non-monotonic differences among grades.

### Reproducibility gates

Gene-set analysis was introduced to interpret genome-wide profiles through
coordinated gene sets rather than isolated genes [12]. For each gene set we
calculated the fraction of measured genes with positive
effects in each cohort, the median effect, and exact sign-test p-values. A
nominal module gate required same-direction significance in both cohorts and
gene-level sign concordance greater than 50% at p < 0.05. We then added a
strict gate: exact two-sided sign tests with Benjamini-Hochberg FDR across
the 1,554 modules [13]. Cohort-specific direction was also evaluated with
stratified label permutation, Freedman-Lane residual permutation and
rotation-based residual nulls [14]. Gene concordance was evaluated with
size-matched and expression-matched empirical nulls. A module was called
replicated only if the exact FDR gate passed. This does not require every gene
to agree; it asks whether module membership carries information across
cohorts.

We applied the gate to seven prespecified mechanism modules and to 1,554
Hallmark, KEGG and Reactome modules with at least 10 measured genes.

The claim ladder was operationalised as follows. Level 2 required nominal
same-direction significance in both matched cohorts. Level 3 (candidate
gene-level replication) additionally required greater than 50% shared-gene
sign concordance, a one-sided exact sign-test p < 0.05, and a one-sided
size-matched empirical-null p < 0.05. Level 4 (strong cross-cohort
replication) required both the cohort-direction tests and the gene-level
concordance test, both based on two-sided exact sign tests, to survive
Benjamini-Hochberg FDR across the prespecified module family. No module was
written as replicated unless Level 4 was reached.

### Technical diagnostics

We calculated the fraction of genes moving in each direction and the median
gene effect within each cohort. A directional fraction outside 30-70% or an
absolute median effect above 0.2 was flagged as a possible global shift. We
cross-tabulated grade against tissue, batch, processing method and source.
We did not use sva directly; known batch or source variables were included in
the design. The sva framework highlights the broader concern that latent
variation can bias high-throughput experiments [15]. Empirical-Bayes batch
adjustment methods such as ComBat address a related class of problems [16].
The GSE23130 grade V samples occurred only in homogenized tissue; the strict
analysis therefore restricted GSE23130 to laser-capture samples.

Internal reproducibility was measured by 100 repeated grade-stratified
split-half analyses. Within each repeat, gene effects were estimated
independently in the two halves, and the Spearman correlation of the two
effect vectors was recorded. The median split-half correlation was reported
for all genes and for the ECM module.

To address within-donor dependence in GSE70362, we repeated the ECM analysis
using one randomly selected sample per donor and using donor-level cluster
bootstrap. Split-half reliability was also repeated by splitting donors
rather than samples. We estimated the effective number of independent ECM
genes from the correlation spectrum and used expression-matched random gene
sets in addition to size-matched nulls. GSE23130 metadata did not include
donor identifiers, so donor-level resampling was not possible for that
cohort; residual within-donor dependence cannot be excluded. The effective-test
adjustment follows the eigenvalue-based approach of Li and Ji [17].

Finally, we estimated full-sample reliability from split-half correlations
with the Spearman-Brown formula and simulated expected sign concordance under
latent correlations from 0 to 0.8. This tests whether the observed 23.3%
concordance can be explained by reliability attenuation alone.

### Pair comparability and interpretive ceiling

Cohort pairs were classified by how closely their measurement context was
matched. Class A pairs shared tissue compartment, endpoint, processing method
and platform family. Class B pairs shared tissue compartment and endpoint but
differed in processing method or platform family. Class C pairs differed in
tissue compartment or endpoint and were retained as contextual comparisons
only.

The primary GSE70362-GSE23130 comparison is Class B: tissue compartment and
degeneration-grade endpoint are matched, but platform and processing method
are not. Platform identity is structurally confounded with cohort identity,
because each platform is represented by one cohort. No statistical model can
therefore separate platform-specific effects from cohort biology. The audit
can test transfer of a prespecified module signal across the observed
cohorts, but it cannot establish platform-independent biology. This ceiling
applies even if a module passes Level 4.
The MAQC project showed that microarray platforms can be concordant at the
differential-expression level, but that result does not resolve the present
cohort-platform identifiability problem [18].

Grade was also partially non-identifiable within cohorts: source or batch
cells were empty for some grade levels. Adjustment therefore reduces obvious
technical confounding but cannot establish a causal grade effect or remove
all residual confounding.

### Software and code availability

The audit is implemented as a standalone Python project. All tables and
figures are regenerated by `run_audit.py`; statistical tests use exact
binomial tails and do not depend on additional statistical libraries beyond
NumPy and pandas. The code is available in the project repository.

## Results

### Cohort diagnostics

| Analysis set | Samples | Donors | Genes | Up | Median effect | Global shift |
|---|---|---|---|---|---|---|
| GSE70362 AF, all grades | 24 | 18 | 18479 | 47.6% | -0.0027 | False |
| GSE70362 AF, grade I-IV | 20 | 16 | 18479 | 43.6% | -0.0089 | False |
| GSE23130, all processing | 23 | NA | 22107 | 49.7% | -0.0002 | False |
| GSE23130 LCM, grade I-IV | 15 | NA | 22107 | 55.0% | +0.0075 | False |
| GSE70362 AF, grade I-IV, grade only | 20 | 16 | 18479 | 43.4% | -0.0084 | False |
| GSE23130 LCM, grade I-IV, grade only | 15 | NA | 22107 | 51.6% | +0.0021 | False |

None of the four primary analysis sets showed a global shift (Table 1). The strict
GSE70362 and GSE23130 sets had fractions up of 43.6% and 55.0%, with median
effects within 0.01 log units. The remaining between-cohort differences were
therefore not explained by a matrix-wide loading difference.

The donor count for GSE23130 is shown as not available because donor
identifiers were not provided in the series metadata. Its 15 strict samples
are therefore sample-level measurements, not validated independent donors.

The grade-processing crosstab showed why the unrestricted GSE23130 analysis
is not sufficient for a replication claim: grade V occurred only in
homogenized samples. Restricting to laser capture removed that specific
confound and left a grade I-IV comparison.

The remaining crosstabs showed partial non-identifiability rather than a
clean crossed design. In the strict GSE23130 subset, grade I occurred only in
CHTN specimens and grade IV only in surgical specimens. In GSE70362, grade II
occurred only in batch 1 and batch 2 did not contain grades III-IV. Adjusted
models are therefore interpreted as nuisance-adjusted associations, not as
fully identified causal grade effects. Grade-only sensitivity models retained
the primary ECM cross-cohort concordance at 23.3% (Table S2) and produced similar
directional estimates, so the principal audit conclusion did not depend on
the adjustment choice.

### ECM module significance does not imply gene-level replication

| Comparison | GSE70362 ECM up | GSE23130 ECM up | ECM gene concordance | Two-sided sign p |
|---|---|---|---|---|
| All available AF/LCM samples | 46.7% | 87.1% | 40.0% | 0.3616 |
| Strict grade I-IV AF/LCM, adjusted | 46.7% | 77.4% | 23.3% | 0.0052 |
| Strict grade I-IV AF/LCM, grade only | 50.0% | 74.2% | 23.3% | 0.0052 |

In the all-sample comparison (Table 2), the ECM module was strongly positive in
GSE23130 (87.1% up,
p = 1.70 x 10^-5) and absent in GSE70362
(46.7% up,
p = 0.7077). Gene-level concordance was
40.0%, without evidence of concordance above
chance.

The strict grade I-IV laser-capture comparison preserved the contradiction.
GSE23130 remained positive (77.4% up,
p = 0.0017), while GSE70362 remained
non-reproducible at the gene level. The cross-cohort concordance was
23.3% (two-sided exact sign p =
0.0052).
The same module was therefore a strong result in one cohort and a
non-concordant direction match in the other (Figure 2).

The prespecified highest-mean-probe rule gave 23.3% ECM concordance
(two-sided exact p = 0.0052). Probe-collapsing sensitivity analyses gave
30.0% for the first probe, 33.3% for the median probe, and a median of 36.7%
(2.5-97.5%: 23.3-48.4%) across 100 random-probe selections. No rule exceeded
50%, but the below-chance significance was not robust to probe selection
(Table 2, Table S23).
The defensible conclusion is therefore failure to exceed chance, not evidence
of statistically significant anti-concordance.

| Collapse rule | GSE70362 ECM up | GSE23130 ECM up | ECM concordance | Two-sided sign p |
|---|---|---|---|---|
| Highest-mean probe (primary) | 46.7% | 77.4% | 23.3% | 0.0052 |
| First probe | 46.7% | 83.9% | 30.0% | 0.0428 |
| Median probe | 46.7% | 74.2% | 33.3% | 0.0987 |
| Random probe, median (2.5-97.5%) | 46.7% | 71.0% (61.3%-80.6%) | 36.7% (23.3%-48.4%) | 0.2005 (median) |

Scale-invariant rank-trend analyses also failed to support cross-cohort
concordance. Unadjusted gene-wise Spearman trends gave 33.3% ECM concordance
(p = 0.0987), and averaging trends within batch or source strata gave 36.7%
(p = 0.2005). In the stratified rank-trend analysis, GSE23130 retained a
positive ECM signal (74.2% up, p = 0.0053), whereas GSE70362 remained
non-directional (53.3% up, p = 0.4278). The result therefore remains below
50% without providing significant evidence of anti-concordance (Table S25).

| Analysis | GSE70362 ECM up | GSE23130 ECM up | ECM concordance | Two-sided sign p |
|---|---|---|---|---|
| Adjusted OLS (primary) | 46.7% | 77.4% | 23.3% | 0.0052 |
| Unadjusted Spearman trend | 46.7% | 64.5% | 33.3% | 0.0987 |
| Batch/source-stratified Spearman trend | 53.3% | 74.2% | 36.7% | 0.2005 |

Internal split-half analyses showed that both strict datasets contained
moderate gene-level reliability (median Spearman rho 0.37 and
0.41 for the ECM module; Table S3). This rules out the simplest explanation
that GSE23130 was pure noise. The evidence supports failure to establish
cross-cohort gene-level replication, not a claim that biological programmes
in the two patient populations are categorically different.

Donor-level sensitivity analyses preserved the negative result (Table S7,
Figure 5).

| Sensitivity model | Replicates | Fraction up | Up 2.5% | Up 97.5% | Concordance | Conc 2.5% | Conc 97.5% | Effect rho |
|---|---|---|---|---|---|---|---|---|
| Donor cluster bootstrap | 300 | 50.0% | 36.7% | 60.0% | 33.3% | 20.0% | 53.3% | -0.450 |
| One sample per donor | 300 | 50.0% | 46.7% | 53.3% | 30.0% | 23.3% | 33.3% | -0.498 |

The effective number of independent ECM genes was low:
6.8
in GSE70362 and
5.9
in GSE23130 (Table S9). We therefore did not treat the binomial sign test as the final
test. An expression-matched null gave an empirical lower-tail probability of
0.0046 for the primary ECM comparison (Table S10).

Reliability attenuation did not explain the result (Table S8, Figure 5). With the observed
split-half reliabilities, simulated concordance under zero latent correlation
remained near 50%, whereas the observed concordance was
23.3%. The observed ECM effect-size
correlation was
-0.495; after
disattenuation it was
-0.884.

| Latent correlation | Expected concordance | 2.5% | 97.5% |
|---|---|---|---|
| 0.0 | 50.0% | 33.3% | 66.7% |
| 0.2 | 53.5% | 36.7% | 70.0% |
| 0.4 | 57.1% | 40.0% | 73.3% |
| 0.6 | 60.8% | 43.3% | 76.7% |
| 0.8 | 64.6% | 46.7% | 80.0% |

The result was not limited to the unweighted sign metric (Table S12).

| Metric | Value |
|---|---|
| Unweighted sign concordance | 23.3% |
| Effect-size weighted concordance | 24.2% |
| Top-half effect concordance | 26.7% |
| Effect-size Spearman rho | -0.495 |

Within-cohort cross-half analyses provided a positive control (Table S11,
Figure S1). Two independent
halves of the same cohort were analyzed with the same models and compared with
the same concordance metric.

| Cohort | Replicates | Concordance | 2.5% | 97.5% | Effect rho |
|---|---|---|---|---|---|
| GSE70362_AF_I_IV | 300 | 63.3% | 46.7% | 80.0% | 0.365 |
| GSE23130_LCM_all | 300 | 64.5% | 38.7% | 77.4% | 0.380 |

The donor-level ECM module score also changed in opposite directions
(Table S14):

| Cohort | Genes | Score slope |
|---|---|---|
| GSE70362_AF_I_IV | 30 | -0.0185 |
| GSE23130_LCM_all | 31 | +0.1729 |

Power calibration showed the expected resolution of the gene-level sign test
(Table S13, Figure S1).
With the observed reliabilities, the nominal 30-gene test had limited power,
and the effective-n sensitivity analysis was deliberately conservative.

| Latent correlation | Mean concordance | Power, nominal n | Power, effective n | Effective genes |
|---|---|---|---|---|
| 0.0 | 50.0% | 4.4% | 0.0% | 5 |
| 0.2 | 53.7% | 6.2% | 0.0% | 5 |
| 0.4 | 57.4% | 11.1% | 0.0% | 5 |
| 0.6 | 60.9% | 20.4% | 0.0% | 5 |

The three permutation schemes agreed on the direction of the ECM result
(Table S15). No
method made GSE70362 nominally directional, while GSE23130 ranged from
borderline to nominally positive.

| Method | GSE70362 p | GSE23130 p |
|---|---|---|
| stratified | 0.7500 | 0.1000 |
| freedman_lane | 0.3700 | 0.0700 |
| rotation | 0.6600 | 0.0100 |

### A broad module audit produces the same pattern

| Stage | Modules |
|---|---|
| Modules tested | 1554 |
| Significant in one cohort only | 673 |
| Significant in both cohorts | 31 |
| Significant in opposite directions | 0 |
| Nominal module and gene-level gate | 14 |
| Passed exact-sign FDR gate | 0 |

Of 1,554 modules, 673 were significant in only one cohort (Figure 3; the full
module-level results are provided in Table S4). Thirty-one were
significant in both cohorts; 14 of those also passed the gene-level
concordance gate at nominal p-values. After exact sign-test FDR control,
with permutation and size-matched empirical nulls as sensitivity checks,
0 modules passed the strict gate. No
module was nominally significant in opposite directions in both cohorts,
which is expected for modest correlation: discordance appears as chance-level
gene concordance rather than as a clean sign reversal.
In the terms of Box 1, 14 modules reached Level 3 (candidate gene-level
replication) and 0 reached Level 4 (strong cross-cohort replication).

Gene-identity sensitivity gave the same qualitative result (Table S24). Mapping 1,098
alias-only platform symbols to current canonical symbols expanded the tested
set from 1,554 to 1,572 modules and increased nominal Level 3 results from 14
to 15. The number significant in both cohorts remained 31, and 0 modules
survived the strict FDR gate.

FDR-family sensitivity also preserved the strict null (Table S26). Applying
Benjamini-Hochberg separately within Hallmark, KEGG and Reactome yielded 0
collection-local FDR results under both primary and alias-aware mappings.
Nominal gene-level results were 0, 3 and 11 in the primary mapping and 0, 3
and 12 after alias mapping. The module sets were not independent: 1,636 pairs
had Jaccard similarity above 0.5 and 94 above 0.8. The strict result is
therefore not caused only by pooling overlapping collections into one large
FDR family, but the overlap structure limits any interpretation of FDR as
independent evidence across modules.

The module-level directional imbalance and gene-level concordance were
essentially uncorrelated (Spearman rho approximately -0.05). A stronger
module direction in one or both cohorts therefore did not predict that the
same genes would agree in the other cohort.

The nominally replicated modules were not interpreted as mechanisms
(Table S27). Their
names clustered around protein targeting, chaperones, glycosylation,
ER-Golgi transport, autophagy and interferon-related processes, but most did
not survive multiple-testing control. The nominal list is therefore a
hypothesis-generating shortlist, not a biological conclusion.

| Module | Genes | GSE70362 up | GSE23130 up | Concordance |
|---|---|---|---|---|
| KEGG_PROTEIN_EXPORT | 22 | 95.5% | 77.3% | 81.8% |
| REACTOME_HSP90_CHAPERONE_CYCLE_FOR_STEROID_HORMONE_RECEPTORS_SHR_IN_THE_PRESENCE_OF_LIGAND | 49 | 65.3% | 77.6% | 75.5% |
| REACTOME_ANTIGEN_PRESENTATION_FOLDING_ASSEMBLY_AND_PEPTIDE_LOADING_OF_CLASS_I_MHC | 29 | 69.0% | 75.9% | 72.4% |
| REACTOME_CHAPERONE_MEDIATED_AUTOPHAGY | 21 | 71.4% | 71.4% | 71.4% |
| REACTOME_RHO_GTPASES_ACTIVATE_IQGAPS | 27 | 70.4% | 85.2% | 70.4% |
| REACTOME_SRP_DEPENDENT_COTRANSLATIONAL_PROTEIN_TARGETING_TO_MEMBRANE | 63 | 77.8% | 87.3% | 68.3% |
| KEGG_PATHOGENIC_ESCHERICHIA_COLI_INFECTION | 44 | 72.7% | 77.3% | 68.2% |
| REACTOME_COOPERATION_OF_PREFOLDIN_AND_TRIC_CCT_IN_ACTIN_AND_TUBULIN_FOLDING | 31 | 67.7% | 80.6% | 67.7% |
| REACTOME_CYCLIN_D_ASSOCIATED_EVENTS_IN_G1 | 44 | 65.9% | 63.6% | 65.9% |
| KEGG_VIBRIO_CHOLERAE_INFECTION | 54 | 63.0% | 74.1% | 63.0% |

### Pairwise tissue cohorts remain close to chance

| Pair | Genes | Concordance | Exact p |
|---|---|---|---|
| GSE186542 vs GSE167199 | 13441 | 58.6% | $5.673517\times10^{-90}$ |
| GSE167199 vs GSE146904 | 13788 | 57.4% | $1.948720\times10^{-67}$ |
| GSE23130 vs GSE146904 | 13960 | 53.6% | $4.187344\times10^{-18}$ |
| GSE70362 vs GSE23130 | 14004 | 51.4% | $3.510011\times10^{-4}$ |
| GSE23130 vs GSE207176 | 14004 | 51.3% | $7.647001\times10^{-4}$ |
| GSE23130 vs GSE167199 | 13827 | 50.9% | 0.0135 |
| GSE70362 vs GSE186542 | 13563 | 49.7% | 0.7593 |
| GSE70362 vs GSE146904 | 13960 | 49.4% | 0.9212 |
| GSE70362 vs GSE207176 | 14004 | 49.1% | 0.9880 |
| GSE23130 vs GSE186542 | 13563 | 48.7% | 0.9988 |
| GSE70362 vs GSE167199 | 13827 | 47.6% | 1.0000 |
| GSE186542 vs GSE146904 | 13554 | 44.2% | 1.0000 |
| GSE186542 vs GSE207176 | 13563 | 42.5% | 1.0000 |
| GSE146904 vs GSE207176 | 13960 | 41.8% | 1.0000 |
| GSE167199 vs GSE207176 | 13827 | 38.7% | 1.0000 |

Across 15 tissue cohort pairs, the median gene-level sign concordance was
49.4% (Figure 4, Table S5). This broad
summary is contextual only because the pairs differ in tissue compartment and
endpoint. Large gene counts can make even modest deviations from 50%
statistically significant, which is why effect size is reported alongside the
p-value.

Exact tissue-and-endpoint matches were rare. The complete exact-contrast set
contained 1 pair (Table S16):

| Pair | Genes | Concordance |
|---|---|---|
| GSE186542 vs GSE167199 | 13441 | 58.6% |

Relaxing the requirement to the same compartment and endpoint class added
3 further pairs (Table S17):

| Pair | Genes | Concordance |
|---|---|---|
| GSE70362 vs GSE23130 | 14004 | 51.4% |
| GSE186542 vs GSE207176 | 13563 | 42.5% |
| GSE167199 vs GSE207176 | 13827 | 38.7% |

The full 15-pair table is retained in the supplement as exploratory context.
The exact-contrast result is not pooled with the broader set.

### No comparable third AF severity cohort was identified

We maintained a third-cohort registry with explicit eligibility tiers
(Table S20). The
current public-data landscape does not contain a Tier A cohort matching the
primary AF I-IV comparison.

| Tier | Datasets |
|---|---|
| B | 2 |
| C | 14 |
| core | 2 |
| exclude | 16 |
| unverified | 5 |

`GSE176205` is an NP bulk RNA-seq cohort (3 controls and 6 degeneration
samples), but its raw group contrast shows a severe global shift: only
25.6% of genes move
upward, with median effect
-1.038. Per-sample
median centering removes the global shift, after which the ECM direction has
only 16.7%
positive genes and concordance with the GSE70362 NP effect of
44.8% (Table S18).
This is retained as a contrast-specific sensitivity analysis, not a third
severity cohort.

| Module | Genes | GSE176205 up | GSE176205 median | GSE70362 NP up | GSE70362 median | Concordance | Effect rho |
|---|---|---|---|---|---|---|---|
| Inflammation/cytokine | 27 | 44.4% | -0.222 | 60.0% | +0.010 | 59.3% | +0.031 |
| Angiogenesis/vascular | 17 | 41.2% | -0.424 | 72.2% | +0.036 | 58.8% | -0.029 |
| Macrophage/myeloid | 18 | 50.0% | +0.066 | 68.4% | +0.016 | 55.6% | +0.480 |
| Immune activation | 30 | 43.3% | -0.058 | 51.6% | +0.004 | 53.3% | +0.058 |
| ECM remodelling | 29 | 16.7% | -0.557 | 56.7% | +0.007 | 44.8% | +0.231 |
| Apoptosis/autophagy | 26 | 34.6% | -0.392 | 50.0% | +0.005 | 38.5% | -0.117 |
| Adhesion/cytoskeleton | 23 | 58.3% | +0.265 | 39.1% | -0.016 | 34.8% | -0.139 |

`GSE17077` was corrected from a secondary-paper label of normal versus
degenerated AF to its official design: senescent versus non-senescent
laser-capture annulus cells. Eight donors had paired senescent and
non-senescent samples. The global paired effect showed no shift, but the ECM
module was not enriched in senescent cells
(41.9%
positive; Table S19).

| Module | Genes | Senescent up | Median effect | One-sided p |
|---|---|---|---|---|
| Angiogenesis/vascular | 18 | 44.4% | -0.022 | 0.7596588134765634 |
| Adhesion/cytoskeleton | 24 | 41.7% | -0.008 | 0.8462718725204479 |
| Immune activation | 31 | 41.9% | -0.006 | 0.8594792424701133 |
| ECM remodelling | 31 | 41.9% | -0.017 | 0.8594792424701133 |
| Apoptosis/autophagy | 25 | 40.0% | -0.023 | 0.8852385282516482 |
| Inflammation/cytokine | 30 | 40.0% | -0.010 | 0.8997557889670215 |
| Macrophage/myeloid | 20 | 35.0% | -0.008 | 0.9423408508300802 |

### Scoping audit of multi-cohort language

To test whether the reporting issue is plausible in the accessible IVD
literature, we performed a language-level scoping audit of the open-access
full-text corpus (Table S21). This is not a systematic review and cannot establish
prevalence.

| Scoping metric | Articles |
|---|---|
| Open-access articles in scoping corpus | 95 |
| Articles using more than one GSE | 79 |
| Articles with consistency language | 71 |
| Multi-cohort articles with consistency language | 62 |
| Articles describing gene-level concordance | 0 |
| Articles mentioning permutation | 9 |
| Articles mentioning FDR | 35 |
| Articles mentioning power | 35 |

The strongest defensible interpretation is that multi-cohort analyses and
consistency language are common in the scoping corpus, while explicit
gene-level concordance language was not detected. The absence of a phrase is
not proof that an analysis was absent, but it identifies a reporting gap.

### Blood cohorts were reproduced but excluded from the tissue claim

The two external blood cohorts were successfully reconstructed from raw
archives (Table S22). They are retained as exploratory cross-compartment context only.

| Cohort | Design | Samples |
|---|---|---|
| GSE124272 | 8 LDH vs 8 healthy | 16 |
| GSE150408 | 42 IDD vs 17 healthy; 25 treatment | 59 |
| GSE150408 untreated | 17 untreated IDD vs 17 healthy | 34 |

## Discussion

### Novelty and relationship to prior work

Several components of this audit are established. Random-signature studies
show that biologically unrelated gene sets can appear significant [19],
marginal selection can be biased by coexpression [6], batch and latent
variation can distort high-throughput data [15,16], and cross-platform
concordance depends strongly on analysis choices [18]. Reporting frameworks
such as STROBE and FAIR address adjacent transparency and reuse problems
[20,21]. The novel contribution of this paper is therefore not a new
statistic or algorithm. It is the integrated, domain-matched IVD audit that
combines gene-level sign concordance, an operational claim ladder and a
sensitivity battery spanning donor dependence, probe selection, gene
identity, scale and FDR-family structure.

### Principal finding

Module-level agreement is not replication. In the clearest matched comparison,
the same ECM module was significant and moderately internally reliable in GSE23130
but its gene-level direction was not supported in GSE70362. The result
persisted under donor-level resampling and did not arise from reliability
attenuation. Alternative probe-collapsing rules remained below 50%
concordance but showed that the exact below-chance magnitude was not robust.
The broad audit found hundreds of one-cohort module signals; no
module survived the strict exact-sign FDR gate. This pattern aligns with a
cross-omic sCJD analysis, where FDR-controlled gene-set overlap was absent and
nominal overlap remained exploratory [1], and with a glioma audit in which a
well-calibrated signature was indistinguishable from random-signature and
clinical-reference benchmarks in external validation [2].
Random-signature studies further show that gene sets unrelated to the
clinical outcome can appear significant [19].

### Why this matters

Public IVD transcriptomes are heterogeneous. They differ in tissue
compartment, dissection or digestion, platform, grade scale, sample size and
clinical context. A module score integrates those differences into a single
direction, which can make two cohorts look more similar than their underlying
genes. Gene-level concordance is a direct check on that aggregation.
Benchmarking studies also show that gene-gene dependencies can bias marginal
selection, so aggregation should be explicitly validated rather than assumed
to preserve gene-level signal [6].

The audit also shows why technical checks alone are insufficient. The primary
cohorts passed the global-shift screen, and the strict comparison removed the
known grade-processing confound. The failure occurred after those checks, at
the cross-cohort gene level. The comparison is nevertheless Class B rather
than Class A: cohort and platform remain structurally confounded, so even a
positive result could support only statistical transfer across the observed
cohorts, not platform-independent biology.

Context dependence is not unique to IVD. A compact sepsis blood signature
discriminated in one clinically distinct validation contrast but was near-null
for infection source and short-term survival in other Day 1 settings [22],
whereas an exploratory ICU sepsis transcriptomic score was sensitive to
cell-composition adjustment and was explicitly framed as an observational
state rather than target engagement [23]. These examples support matching each
reproducibility claim to the tissue, endpoint, processing method and clinical
context in which it is made.

Recent IVD single-cell and spatial studies provide biological context for
fibrotic NP cell states and matrix-integrin programmes, including
WNT/FN1-CD44 and integrin/N-glycosylation axes [24,25]. Such findings support
plausibility but do not imply that the bulk ECM module investigated here is
replicated across cohorts; biological relevance and reproducibility are
separate claims.

**Box 1. Claim ladder for public-data module reproducibility.**

| Level | Claim | Minimum evidence | Permitted language |
|---|---|---|---|
| 0 | Exploratory module signal | Significant module in one cohort | exploratory or hypothesis-generating |
| 1 | Internally reproducible module | Repeated split-half or permutation supports within-cohort direction | internally stable, not independently replicated |
| 2 | Contextually concordant module | Same prespecified module direction in matched independent cohorts | consistency in this matched context |
| 3 | Candidate gene-level replication | Same-direction significance in both cohorts; >50% shared-gene sign concordance; one-sided exact and size-matched empirical-null p < 0.05 | candidate replication requiring confirmation |
| 4 | Strong cross-cohort replication | Both two-sided exact module-direction tests and gene-level concordance survive FDR across the prespecified family | statistically replicated across the observed cohorts in the matched tissue and endpoint context, not platform-independent |

Claim level does not override pair comparability. A Level 4 finding in a
Class B pair supports statistical transfer across the observed cohorts only;
platform-independent or mechanistic replication requires Class A data,
additional independent cohorts or experimental validation.

### Reporting recommendation

The recommendation below follows the claim ladder in Box 1. For public-data
IVD studies, we recommend a four-line reproducibility statement for every
claimed module:

1. Report the module direction and exact sign-test p-value in each cohort.
2. Report the proportion of shared genes moving in the same direction and its
   exact and empirical p-value.
3. Report an internal reliability estimate and state whether the comparison is
   matched by tissue, endpoint and processing.
4. For multiple modules, report multiplicity control and state whether the
   result survives FDR.

Words such as "replicated" or "consistent" should be reserved for findings
that pass all four layers. A one-cohort module is exploratory even when its
p-value is small.

Where cell-resolved data are available, the same reporting logic should be
applied at donor and cell-state level. Annotation should be independently
validated or consensus-based [26], and cross-cohort classification should be
evaluated on held-out donors using pseudobulk or comparable aggregation rather
than treating individual cells as independent samples [27]. Machine-readable
metadata and executable workflow descriptions should accompany the analysis
to make provenance and parameter choices traceable [28]. When cell-resolved
designs use hashtag-assisted pooling, the trade-off between batch-effect
mitigation and demultiplexing cell loss should be reported explicitly, because
pooled designs can remove cells required for downstream pseudobulk comparisons
[29]. Established reporting statements such as STROBE provide a broader
framework for transparent observational research reporting [20].

### Limitations

The audit is retrospective and uses public cohorts with different platforms
and processing methods. The strict comparison has 20 and 15 samples, limited
power for small gene sets, and cannot eliminate all platform-specific effects.
This limitation defines the claim: the observed data do not establish
cross-cohort gene-level replication. They do not prove that the underlying
biology is absent or opposite.

No Tier A third AF severity cohort was identified, so the strongest domain
statement is that the current public-data landscape does not provide the
independent evidence needed for such a claim. The literature component is a
scoping language audit rather than a systematic review. The results therefore
identify a reporting and data gap, not a prevalence estimate across all IVD
studies.

Because the primary cohorts differ in platform and processing method, cohort
and platform effects are not identifiable separately. The negative primary
result is therefore a failure to establish cross-cohort gene-level
transferability, not proof that a shared biological programme is absent. A
future positive result would require the same qualification.

The analysis was not publicly preregistered. The internal freeze limits, but
does not eliminate, concern that the primary comparison or sensitivity
analyses were selected after exploratory inspection.

Donor identifiers were available only for GSE70362. GSE23130 was analysed at
the sample level because its GEO metadata did not identify donors, so
residual within-donor dependence in that cohort remains unresolved.

Grade, batch, source and processing method were not fully crossed. Some grade
levels occurred in only one nuisance stratum, so the adjusted grade
coefficients are not fully identified causal effects. The grade-only
sensitivity analysis reproduced the primary ECM concordance, but residual
confounding remains a limitation.

Grade was modelled as an ordinal trend rather than as a categorical exposure.
This choice preserves the sign of monotonic gene-level associations under any
strictly increasing coding, but it does not capture non-monotonic differences
among grades and does not justify interpreting coefficient magnitudes as
linear dose-response effects.

The primary probe rule retained the highest-mean probe per gene. Alternative
first-probe, median-probe and random-probe rules remained below 50% ECM
concordance, but the exact below-chance magnitude depended on probe
selection. The study therefore does not claim statistically significant
anti-concordance.

Gene identity was also imperfect. Of 22,107 platform symbols, 1,098 were
mapped only through historical aliases, 3,305 remained unresolved, and 4,434
ambiguous alias keys were removed to avoid conflicting mappings. The
alias-aware sensitivity did not change the primary ECM comparison or the FDR
conclusion, but broad module counts were mapping-sensitive.

The scale-invariant rank-trend analysis preserved direction in GSE23130 but
gave only 33.3-36.7% cross-cohort ECM concordance, with two-sided p-values
between 0.0987 and 0.2005. The primary below-chance p-value is therefore not
treated as robust evidence of anti-concordance.

The module family was operationally defined as one global
Hallmark/KEGG/Reactome family. Collection-local FDR analyses also produced
zero strict results, but module overlap was substantial: 1,636 pairs exceeded
Jaccard 0.5 and 94 exceeded 0.8. FDR therefore should not be interpreted as
evidence from thousands of independent hypotheses.

The nominally replicated modules require independent cohorts and, where
possible, experimental validation. Recent single-cell evidence for fibrotic NP
states and matrix-integrin programmes [24,25] does not remove the need for an
independent bulk severity cohort or experimental validation, and it does not
establish causality for the present module result. No result in this study
establishes a causal mechanism.

## Data availability

All source cohorts are public GEO series: GSE70362, GSE23130, GSE186542,
GSE167199, GSE146904 and GSE207176. MSigDB 2024.1 files were used for the
module audit. The derived effect tables, audit results, figures and
manuscript are generated by the code in this project, which is available at
https://github.com/wdsve/ivd-repro-audit and archived at
https://doi.org/10.5281/zenodo.23133983. Machine-readable
metadata and executable workflow descriptions would make the analysis easier
to reuse and audit [28]. The FAIR principles provide the underlying standard
for findable, accessible, interoperable and reusable data and metadata [21].

## Figure legends

**Figure 1. A reproducibility gate for cross-cohort omics claims.** The
workflow moves from cohort inventory to harmonisation, technical diagnostics,
independent-unit re-estimation, module and gene-level testing, and reporting.
Each gate can stop a claim before it is written as replication.

**Figure 2. ECM module significance does not reproduce at the gene level.**
(A) Fraction of ECM genes increasing with degeneration in GSE23130 and
GSE70362 under all-sample and strict grade I-IV analyses. (B) Gene-level sign
concordance between the two cohorts. The dashed reference is 50%. The strict
comparison is below 50%, but the exact below-chance magnitude depends on the
probe-collapsing rule. Internal split-half correlations show that both
cohorts contain moderate ECM reliability, so the failure is not explained by
the absence of within-cohort signal.

**Figure 3. Broad MSigDB module audit.** Each point is a Hallmark, KEGG or
Reactome module with at least 10 measured genes. The x-axis is the maximum
absolute deviation from 50% directional balance in either cohort; the y-axis
is gene-level sign concordance. The bar panel summarises the audit funnel.

**Figure 4. Pairwise tissue cohort concordance.** Gene-level sign concordance
for 15 pairs of public human IVD tissue cohorts. The vertical reference at
50% denotes chance. Most pairs cluster near chance, and the highest pair
remains below 60%.

**Figure 5. Donor-level sensitivity and reliability attenuation.** (A)
One-sample-per-donor and donor cluster-bootstrap distributions for the
GSE70362 ECM directional fraction. (B) The corresponding cross-cohort
gene-level concordance. (C) Simulated sign concordance under latent
correlations from 0 to 0.8 using the observed split-half reliabilities. The
red line is the observed ECM concordance.

## References

1. Oberoi RK, Gurung D, Harris LK. Cross-Omic Comparative Analysis Identifies Transcriptomic Signatures and Exploratory Gene Set-Level Signals in Sporadic Creutzfeldt-Jakob Disease. *International Journal of Molecular Sciences*. 2026;27:6560. doi:10.3390/ijms27156560

2. Yasar S, Yagin B, Alzakari SA, et al. Evaluating a Glioma Transcriptomic Signature Against a Clinical Reference Model and a Random-Signature Null Distribution: A Leakage-Controlled Internal Audit and a Survey of the Field. *Diagnostics*. 2026;16:2803. doi:10.3390/diagnostics16172803

3. Ioannidis JPA. Why most published research findings are false. *PLoS Medicine*. 2005;2:e124. doi:10.1371/journal.pmed.0020124

4. Errington TM, et al. Investigating the replicability of preclinical cancer biology. *eLife*. 2021;10:e71601. doi:10.7554/eLife.71601

5. Open Science Collaboration. Estimating the reproducibility of psychological science. *Science*. 2015;349:aac4716. doi:10.1126/science.aac4716

6. Yu D, Li C, Yan S, et al. Comparative evaluation of gene selection approaches in transcriptomics: bias correction and visualization with TransPro. *GigaScience*. 2026;15:giag057. doi:10.1093/gigascience/giag057

7. Barrett T, et al. NCBI GEO: archive for functional genomics data sets: update. *Nucleic Acids Research*. 2013;41:D991-D995. doi:10.1093/nar/gks1193

8. Kazezian Z, Gawri R, Haglund L, et al. Gene Expression Profiling Identifies Interferon Signalling Molecules and IGFBP3 in Human Degenerative Annulus Fibrosus. *Scientific Reports*. 2015;5:15662. doi:10.1038/srep15662

9. Gruber HE, Hoelscher GL, Ingram JA, Hanley EN. Genome-wide analysis of pain-, nerve- and neurotrophin-related gene expression in the degenerating human annulus. *Molecular Pain*. 2012;8:63. doi:10.1186/1744-8069-8-63

10. Li Z, Sun Y, He M, Liu J. Differentially-expressed mRNAs, microRNAs and long noncoding RNAs in intervertebral disc degeneration identified by RNA-sequencing. *Bioengineered*. 2021;12:1026-1039. doi:10.1080/21655979.2021.1899533

11. Ritchie ME, et al. limma powers differential expression analyses for RNA-sequencing and microarray studies. *Nucleic Acids Research*. 2015;43:e47. doi:10.1093/nar/gkv007

12. Subramanian A, et al. Gene set enrichment analysis: a knowledge-based approach for interpreting genome-wide expression profiles. *PNAS*. 2005;102:15545-15550. doi:10.1073/pnas.0506580102

13. Benjamini Y, Hochberg Y. Controlling the false discovery rate: a practical and powerful approach to multiple testing. *Journal of the Royal Statistical Society Series B*. 1995;57:289-300. doi:10.1111/j.2517-6161.1995.tb02031.x

14. Freedman D, Lane D. A nonstochastic interpretation of reported significance levels. *Journal of Business & Economic Statistics*. 1983;1:292-298. doi:10.1080/07350015.1983.10509354

15. Leek JT, et al. The sva package for removing batch effects and other unwanted variation in high-throughput experiments. *Bioinformatics*. 2012;28:882-883. doi:10.1093/bioinformatics/bts034

16. Johnson WE, Li C, Rabinovic A. Adjusting batch effects in microarray expression data using empirical Bayes methods. *Biostatistics*. 2007;8:118-127. doi:10.1093/biostatistics/kxj037

17. Li J, Ji L. Adjusting multiple testing in multilocus analyses using the eigenvalues of a correlation matrix. *Heredity*. 2005;95:221-227. doi:10.1038/sj.hdy.6800717

18. MAQC Consortium. The MicroArray Quality Control (MAQC) project shows inter- and intraplatform reproducibility of gene expression measurements. *Nature Biotechnology*. 2006;24:1151-1161. doi:10.1038/nbt1239

19. Venet D, Dumont JE, Detours V. Most random gene expression signatures are significantly associated with breast cancer outcome. *PLoS Computational Biology*. 2011;7:e1002240. doi:10.1371/journal.pcbi.1002240

20. von Elm E, Altman DG, Egger M, et al. The Strengthening the Reporting of Observational Studies in Epidemiology (STROBE) statement: guidelines for reporting observational studies. *Lancet*. 2007;370:1453-1457. doi:10.1016/S0140-6736(07)61602-X

21. Wilkinson MD, Dumontier M, Aalbersberg IJ, et al. The FAIR Guiding Principles for scientific data management and stewardship. *Scientific Data*. 2016;3:160018. doi:10.1038/sdata.2016.18

22. Qin C, Wang W, Du Q, et al. An 11-gene blood transcriptomic signature reflects a sepsis-associated host-response pattern across public cohorts. *Frontiers in Medicine*. 2026;13:1844619. doi:10.3389/fmed.2026.1844619

23. Yang X, Hu T, Wang J, et al. An NLRP3 inflammasome-anchored Astragalus mechanistic prior yields a mortality-associated transcriptomic signal in ICU sepsis: a secondary analysis with exploratory cross-cohort assessment. *Inflammation Research*. 2026;75:201. doi:10.1007/s00011-026-02352-0

24. Li Q, Liang G, Bo K, et al. Single-cell and spatial transcriptomics characterisation of RSPO2+ nucleus pulposus cells reveals a WNT/FN1-CD44 degenerative axis and therapeutic targets in IVDD. *Journal of Orthopaedic Translation*. 2026;60:101203. doi:10.1016/j.jot.2026.101203

25. Qiang S, Liu Y, Dong Y, et al. ITGBL1 and RPN1 Mark a Fibrotic NP Subpopulation with Coupled Integrin Signaling and N-Glycosylation Programs in IVDD. *Journal of Inflammation Research*. 2026;19. doi:10.2147/JIR.S629922

26. Sun L, Ma L, Chen L, et al. Annotation of cell types in single-cell sequencing for cardiovascular disease: concepts, workflows, challenges, and best practices. *International Journal of Biochemistry and Cell Biology*. 2026;201:107027. doi:10.1016/j.biocel.2026.107027

27. Marchi A, Anwer D, Kerkhoven E, et al. Cell-Type-Resolved Pseudobulk Classification Across Independent Cohorts Identifies Microglial PTPRG as a Transcriptional Hub in Alzheimer's Disease. *bioRxiv*. 2026. Preprint. doi:10.64898/2026.04.07.717029

28. Dörpholz H, Simon R, Usadel B, Kranz A. Integrating cross-omics research through FAIR Digital Objects with DataPLANT. *Journal of Integrative Bioinformatics*. 2025;22(4):20250056. doi:10.1515/jib-2025-0056

29. Chatterjee B, Gorga K, Blair C, et al. Moderated designs can balance between batch-effect mitigation and cell loss due to hashtag-assisted pooling in single-cell experiments. *Genome Research*. 2026;36:2027-2036. doi:10.1101/gr.281624.125
