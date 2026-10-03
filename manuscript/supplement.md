# Supplementary material

## Table S1. Primary comparison

These three rows are consolidated into main-text Table 2.

| Comparison | GSE70362 ECM up | GSE23130 ECM up | ECM gene concordance | Two-sided sign p |
|---|---|---|---|---|
| All available AF/LCM samples | 46.7% | 87.1% | 40.0% | 0.3616 |
| Strict grade I-IV AF/LCM, adjusted | 46.7% | 77.4% | 23.3% | 0.0052 |
| Strict grade I-IV AF/LCM, grade only | 50.0% | 74.2% | 23.3% | 0.0052 |

## Table S2. Cohort effect diagnostics

| Analysis set | Samples | Donors | Genes | Up | Median effect | Global shift |
|---|---|---|---|---|---|---|
| GSE70362 AF, all grades | 24 | 18 | 18479 | 47.6% | -0.0027 | False |
| GSE70362 AF, grade I-IV | 20 | 16 | 18479 | 43.6% | -0.0089 | False |
| GSE23130, all processing | 23 | NA | 22107 | 49.7% | -0.0002 | False |
| GSE23130 LCM, grade I-IV | 15 | NA | 22107 | 55.0% | +0.0075 | False |
| GSE70362 AF, grade I-IV, grade only | 20 | 16 | 18479 | 43.4% | -0.0084 | False |
| GSE23130 LCM, grade I-IV, grade only | 15 | NA | 22107 | 51.6% | +0.0021 | False |

## Table S3. Internal split-half reliability

| cohort | gene_space | median_spearman | n_splits |
|---|---|---|---|
| GSE70362_AF_all | all | 0.1983099325567557 | 100 |
| GSE70362_AF_all | ECM | 0.4075639599555061 | 100 |
| GSE70362_AF_I_IV | all | 0.1383736790830905 | 100 |
| GSE70362_AF_I_IV | ECM | 0.3690767519466074 | 100 |
| GSE23130_all | all | -0.0654864000493762 | 100 |
| GSE23130_all | ECM | 0.044758064516129 | 100 |
| GSE23130_LCM_all | all | 0.1337130096184392 | 100 |
| GSE23130_LCM_all | ECM | 0.4084677419354838 | 100 |
| GSE70362_AF_I_IV_grade_only | all | 0.2353076937601182 | 100 |
| GSE70362_AF_I_IV_grade_only | ECM | 0.3388209121245829 | 100 |
| GSE23130_LCM_grade_only | all | 0.2382855306866113 | 100 |
| GSE23130_LCM_grade_only | ECM | 0.7268145161290323 | 100 |

## Table S4. Full MSigDB audit

The complete audit of 1554 modules is provided as
`results/msigdb_module_audit.csv`.

## Table S5. Pairwise tissue cohort concordance

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

## Table S6. Prespecified mechanism modules

The complete comparison is provided as
`results/curated_module_audit.csv`.

## Table S7. Donor-level sensitivity

| Sensitivity model | Replicates | Fraction up | Up 2.5% | Up 97.5% | Concordance | Conc 2.5% | Conc 97.5% | Effect rho |
|---|---|---|---|---|---|---|---|---|
| Donor cluster bootstrap | 300 | 50.0% | 36.7% | 60.0% | 33.3% | 20.0% | 53.3% | -0.450 |
| One sample per donor | 300 | 50.0% | 46.7% | 53.3% | 30.0% | 23.3% | 33.3% | -0.498 |

## Table S8. Reliability attenuation

| Latent correlation | Expected concordance | 2.5% | 97.5% |
|---|---|---|---|
| 0.0 | 50.0% | 33.3% | 66.7% |
| 0.2 | 53.5% | 36.7% | 70.0% |
| 0.4 | 57.1% | 40.0% | 73.3% |
| 0.6 | 60.8% | 43.3% | 76.7% |
| 0.8 | 64.6% | 46.7% | 80.0% |

## Table S9. Effective independent genes

| cohort | gene_space | effective_genes |
|---|---|---|
| GSE70362_AF_I_IV | ECM | 6.842470672703271 |
| GSE23130_LCM_all | ECM | 5.9055599648777015 |

## Table S10. Expression-matched ECM null

| module | n_genes | empirical_p_greater | empirical_p_less | empirical_p_two_sided | null_median | null_upper_95 |
|---|---|---|---|---|---|---|
| ECM remodelling | 30 | 0.9988002399520096 | 0.0045990801839632 | 0.0091981603679264 | 0.5 | 0.6333333333333333 |

## Table S11. Cross-half positive controls

| Cohort | Replicates | Concordance | 2.5% | 97.5% | Effect rho |
|---|---|---|---|---|---|
| GSE70362_AF_I_IV | 300 | 63.3% | 46.7% | 80.0% | 0.365 |
| GSE23130_LCM_all | 300 | 64.5% | 38.7% | 77.4% | 0.380 |

## Table S12. Weighted concordance

| Metric | Value |
|---|---|
| Unweighted sign concordance | 23.3% |
| Effect-size weighted concordance | 24.2% |
| Top-half effect concordance | 26.7% |
| Effect-size Spearman rho | -0.495 |

## Table S13. Power calibration

| Latent correlation | Mean concordance | Power, nominal n | Power, effective n | Effective genes |
|---|---|---|---|---|
| 0.0 | 50.0% | 4.4% | 0.0% | 5 |
| 0.2 | 53.7% | 6.2% | 0.0% | 5 |
| 0.4 | 57.4% | 11.1% | 0.0% | 5 |
| 0.6 | 60.9% | 20.4% | 0.0% | 5 |

## Table S14. Module score slopes

| Cohort | Genes | Score slope |
|---|---|---|
| GSE70362_AF_I_IV | 30 | -0.0185 |
| GSE23130_LCM_all | 31 | +0.1729 |

## Table S15. Permutation-method sensitivity

| Method | GSE70362 p | GSE23130 p |
|---|---|---|
| stratified | 0.7500 | 0.1000 |
| freedman_lane | 0.3700 | 0.0700 |
| rotation | 0.6600 | 0.0100 |

## Table S16. Exact-contrast cohort pairs

| Pair | Genes | Concordance |
|---|---|---|
| GSE186542 vs GSE167199 | 13441 | 58.6% |

## Table S17. Compartment-matched cohort pairs

| Pair | Genes | Concordance |
|---|---|---|
| GSE70362 vs GSE23130 | 14004 | 51.4% |
| GSE186542 vs GSE207176 | 13563 | 42.5% |
| GSE167199 vs GSE207176 | 13827 | 38.7% |

## Table S18. GSE176205 NP directional validation

| Module | Genes | GSE176205 up | GSE176205 median | GSE70362 NP up | GSE70362 median | Concordance | Effect rho |
|---|---|---|---|---|---|---|---|
| Inflammation/cytokine | 27 | 44.4% | -0.222 | 60.0% | +0.010 | 59.3% | +0.031 |
| Angiogenesis/vascular | 17 | 41.2% | -0.424 | 72.2% | +0.036 | 58.8% | -0.029 |
| Macrophage/myeloid | 18 | 50.0% | +0.066 | 68.4% | +0.016 | 55.6% | +0.480 |
| Immune activation | 30 | 43.3% | -0.058 | 51.6% | +0.004 | 53.3% | +0.058 |
| ECM remodelling | 29 | 16.7% | -0.557 | 56.7% | +0.007 | 44.8% | +0.231 |
| Apoptosis/autophagy | 26 | 34.6% | -0.392 | 50.0% | +0.005 | 38.5% | -0.117 |
| Adhesion/cytoskeleton | 23 | 58.3% | +0.265 | 39.1% | -0.016 | 34.8% | -0.139 |

## Table S19. GSE17077 paired senescence analysis

| Module | Genes | Senescent up | Median effect | One-sided p |
|---|---|---|---|---|
| Angiogenesis/vascular | 18 | 44.4% | -0.022 | 0.7596588134765634 |
| Adhesion/cytoskeleton | 24 | 41.7% | -0.008 | 0.8462718725204479 |
| Immune activation | 31 | 41.9% | -0.006 | 0.8594792424701133 |
| ECM remodelling | 31 | 41.9% | -0.017 | 0.8594792424701133 |
| Apoptosis/autophagy | 25 | 40.0% | -0.023 | 0.8852385282516482 |
| Inflammation/cytokine | 30 | 40.0% | -0.010 | 0.8997557889670215 |
| Macrophage/myeloid | 20 | 35.0% | -0.008 | 0.9423408508300802 |

## Table S20. Third-cohort registry summary

| Tier | Datasets |
|---|---|
| B | 2 |
| C | 14 |
| core | 2 |
| exclude | 16 |
| unverified | 5 |

## Table S21. Literature scoping audit

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

## Table S22. Reproduced blood cohorts

| Cohort | Design | Samples |
|---|---|---|
| GSE124272 | 8 LDH vs 8 healthy | 16 |
| GSE150408 | 42 IDD vs 17 healthy; 25 treatment | 59 |
| GSE150408 untreated | 17 untreated IDD vs 17 healthy | 34 |

## Table S23. Probe-to-symbol collapsing sensitivity

These rows are consolidated into main-text Table 2.

| Collapse rule | GSE70362 ECM up | GSE23130 ECM up | ECM concordance | Two-sided sign p |
|---|---|---|---|---|
| Highest-mean probe (primary) | 46.7% | 77.4% | 23.3% | 0.0052 |
| First probe | 46.7% | 83.9% | 30.0% | 0.0428 |
| Median probe | 46.7% | 74.2% | 33.3% | 0.0987 |
| Random probe, median (2.5-97.5%) | 46.7% | 71.0% (61.3%-80.6%) | 36.7% (23.3%-48.4%) | 0.2005 (median) |

The primary analysis used the highest-mean probe per gene. Alternative
collapsing rules and 100 random-probe selections did not exceed 50% ECM
concordance, but they showed that the exact below-chance level in the primary
analysis was sensitive to probe selection.

## Table S24. Gene-identity sensitivity

| Metric | Primary mapping | Alias-aware mapping |
|---|---|---|
| Platform gene symbols | 22107 | 22107 |
| Current canonical symbols | 17704 | 17704 |
| Alias-only symbols recovered | 0 | 1098 |
| Unresolved symbols | 3305 | 3305 |
| Ambiguous alias keys removed | 4434 | 4434 |
| Modules tested | 1554 | 1572 |
| Significant in one cohort | 673 | 692 |
| Significant in both cohorts | 31 | 31 |
| Nominal gene-level results | 14 | 15 |
| Strict FDR results | 0 | 0 |

The primary mapping retained supplied platform symbols. The alias-aware
mapping additionally used current synonyms and nomenclature-authority symbols
from human gene_info. It recovered 1,098 alias-only symbols but left 3,305
unresolved and removed 4,434 ambiguous alias keys. The strict FDR conclusion
remained zero modules, while broader nominal counts changed modestly.

## Table S25. Scale-invariant trend sensitivity

| Analysis | GSE70362 ECM up | GSE23130 ECM up | ECM concordance | Two-sided sign p |
|---|---|---|---|---|
| Adjusted OLS (primary) | 46.7% | 77.4% | 23.3% | 0.0052 |
| Unadjusted Spearman trend | 46.7% | 64.5% | 33.3% | 0.0987 |
| Batch/source-stratified Spearman trend | 53.3% | 74.2% | 36.7% | 0.2005 |

Spearman trends are invariant to any strictly increasing transformation of
each gene across samples and therefore test whether the direction call is
driven by platform-specific scale assumptions. The stratified analysis
averages gene-wise Spearman trends within batch or source strata with at least
four samples and three observed grades.

## Table S26. Module-family FDR and overlap sensitivity

| Mapping | Collection | Modules | Nominal gene-level | Collection-local FDR |
|---|---|---|---|---|
| primary | Hallmark | 50 | 0 | 0 |
| primary | KEGG | 182 | 3 | 0 |
| primary | Reactome | 1322 | 11 | 0 |
| alias-aware | Hallmark | 50 | 0 | 0 |
| alias-aware | KEGG | 184 | 3 | 0 |
| alias-aware | Reactome | 1338 | 12 | 0 |

The module sets were not independent. Among 1,554 tested modules, 243,830
pairs had nonzero Jaccard overlap, 1,636 exceeded Jaccard 0.5 and 94 exceeded
0.8. Collection-local FDR was zero for Hallmark, KEGG and Reactome under both
primary and alias-aware mappings.

## Table S27. Nominally replicated modules

The 14 modules that reached Level 3 (candidate gene-level replication) at
nominal p-values are a hypothesis-generating shortlist, not a biological
conclusion; 0 survived the strict FDR gate. The top 10 by gene-level
concordance are shown here; the full list is in
`results/msigdb_module_audit.csv`.

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

## Figure S1. Positive controls and power calibration

(A) Cross-cohort ECM concordance compared with within-cohort cross-half
positive controls. (B) Power of the nominal 30-gene sign test across
simulated latent correlations. (C) Unweighted, effect-size-weighted and
top-half effect concordance. This figure was moved from the main text
(Figure 6 in earlier drafts) to keep the main-text display-item count within
the journal limit.

## Technical diagnostic tables

The grade, batch, processing-method and source crosstabs are provided in
`results/confound_*.csv`. These tables are part of the stopping rules: the
unrestricted GSE23130 comparison is not used as the primary replication test
because grade V occurs only in homogenized samples.
