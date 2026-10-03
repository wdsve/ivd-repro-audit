# Frozen sensitivity analysis plan

Date frozen before the final permutation run: 2026-09-16

Status: internal analysis freeze, not a public preregistration.

This plan defines the analyses used to address the main reviewer concerns:
technical non-transferability, donor dependence, gene dependence, multiple
testing, and reliability attenuation.

## Primary comparison

- Cohorts: GSE70362 and GSE23130.
- Tissue: annulus fibrosus.
- Endpoint: Thompson/histological grade I-IV.
- Processing: GSE23130 restricted to LCM.
- GSE70362 model: grade + batch.
- GSE23130 model: grade + source.
- Direction: positive effect means increasing with degeneration grade.
- Shared genes: symbols measured in both cohorts after probe collapsing.

## Grade coding and direction

- Encode grade only as a strictly increasing ordinal score: I = 1, I-II =
  1.5, II = 2, III = 3, IV = 4.
- Interpret the coefficient sign as a monotone trend, not as an equal-step
  or causal dose effect. The sign is invariant to strictly increasing
  recoding of the same grade order.
- Do not use this model to test arbitrary non-monotonic grade differences.

## Probe collapsing

- Use the highest-mean probe per gene as the primary rule.
- Repeat the primary ECM comparison using the first probe, the median across
  probes and 100 random-probe selections.
- Do not claim statistically significant anti-concordance unless the
  below-50% result is robust across these collapsing rules.

## Gene identity

- Use supplied platform symbols and current Entrez-to-symbol mapping for the
  primary analysis.
- Repeat the broad module audit after mapping historical platform symbols
  through current synonyms and nomenclature-authority symbols.
- Remove alias keys that map to more than one current canonical symbol.
- Report unresolved and ambiguous mappings and do not interpret small changes
  in nominal module counts as stable discovery.

## Scale invariance

- Repeat the primary ECM direction analysis with gene-wise Spearman trends,
  which are invariant to strictly increasing per-sample transformations.
- Evaluate both unadjusted trends and trends averaged within batch or source
  strata with at least four samples and three observed grades.
- Do not claim significant anti-concordance unless the below-50% result is
  robust to this scale-invariant analysis.

## FDR family and overlap

- Use all Hallmark, KEGG and Reactome modules as the global FDR family.
- Repeat FDR separately within each collection as a sensitivity analysis.
- Report pairwise module overlap; do not interpret thousands of overlapping
  modules as thousands of independent hypotheses.

## Primary outcome

- ECM direction: fraction of ECM genes with positive effects in each cohort
  and exact two-sided sign-test probability.
- Cross-cohort gene-level concordance: proportion of shared ECM genes with
  the same effect direction.
- Internal reliability: median Spearman correlation from repeated
  grade-stratified split-half analyses.

## Model identifiability

- Inspect grade-by-batch and grade-by-source crosstabs before interpreting
  adjusted coefficients.
- Treat adjusted models as nuisance-adjusted associations rather than fully
  identified causal grade effects when a grade level occurs in only one
  nuisance stratum.
- Retain grade-only models as sensitivity analyses. The primary ECM
  cross-cohort concordance must remain 23.3% under this alternative model.

## Pre-specified sensitivity analyses

### Donor independence

- Random one sample per GSE70362 donor, repeated 300 times.
- Donor-level cluster bootstrap, repeated 300 times.
- Donor-stratified split-half reliability.
- GSE23130 has no donor identifiers in its GEO metadata; donor-level
  resampling is not possible and residual within-donor dependence cannot be
  excluded.

Decision rule: the negative ECM result remains reportable only if the
donor-level median ECM direction stays near 50% and cross-cohort concordance
stays below 50% across the resampling distributions.

### Gene dependence and expression matching

- Effective number of independent ECM genes estimated from the correlation
  spectrum.
- Size-matched random-set null with 5,000 permutations.
- Expression-decile-matched random-set null for the primary ECM comparison.

Decision rule: the binomial sign test is not used as the final evidence
source. Empirical null probability is reported alongside it.

### Module direction permutation

- 199 permutations for each of three null constructions: stratified grade
  permutation, Freedman-Lane residual permutation and rotation-based
  residual permutation.
- The conservative result is the maximum empirical p-value across methods.
- Two-sided empirical p-values are computed from directional imbalance for
  the seven prespecified mechanism modules.

Decision rule: a module is nominally directional only when the empirical
p-value is below 0.05 before multiplicity control. Exact two-sided sign tests
are used for the 1,554-module FDR analysis because Monte Carlo resolution is
too coarse for the BH threshold.

### Multiple testing

- Benjamini-Hochberg FDR applied separately to module direction and
  cross-cohort concordance.
- Final strict gate uses exact two-sided sign tests with q < 0.05 for both
  cohorts and gene-level concordance.
- Permutation and size-matched empirical nulls are reported as sensitivity
  checks because their Monte Carlo resolution can be coarser than the
  BH-adjusted exact-p threshold.

Decision rule: nominal module-plus-gene results are reported as a shortlist
unless they survive FDR.

### Reliability attenuation

- Split-half reliability corrected with the Spearman-Brown formula.
- Observed cross-cohort effect-size correlation reported.
- Disattenuated correlation reported as a sensitivity estimate.
- Sign concordance simulated for latent correlations from 0 to 0.8 using the
  observed reliabilities.

Decision rule: the primary claim is written as failure to establish
gene-level replication, not as proof that underlying biology is absent.

### Pairwise cohort analysis

- Primary pairwise comparisons require the same compartment and endpoint
  class.
- Other comparisons are retained as secondary context only.

## Claim language

Permitted:

- module-level consistency was not supported by gene-level concordance
- a cross-cohort replicated association was not established
- the ECM module showed moderate internal reliability but was not externally concordant

Not permitted:

- the biological programme does not replicate
- ECM remodelling is consistent across cohorts
- a public-data mechanism is proved
