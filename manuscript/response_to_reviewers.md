# Pre-emptive response to likely reviewer concerns

## Comment 1. Low concordance may reflect platform or processing differences,
not lack of biological replication.

Response: We agree that public cohorts cannot eliminate all platform-specific
effects, and the revised manuscript is framed as failure to establish
gene-level replication rather than proof that the underlying biology is
absent. We added grade-only and adjusted models, donor-level resampling,
expression-matched nulls and an explicit statement that platform effects
remain a limitation. The conclusion is about what can be inferred from the
available cohorts, not about an unobservable latent mechanism.

## Comment 2. GSE70362 contains multiple samples from the same donor.

Response: The strict GSE70362 analysis contains 20 AF samples from 16 donors.
We added random-one-sample-per-donor analysis and donor-level cluster
bootstrap. The median ECM directional fraction remained 50%, and the median
gene-level cross-cohort concordance remained 30% under one-sample selection
and 33.3% under cluster bootstrap. The negative result is therefore not
created by repeated sampling of donors. GSE23130 does not provide donor
identifiers in its GEO metadata, so donor-level resampling was not possible
for that cohort. We now state explicitly that residual within-donor
dependence in GSE23130 cannot be excluded and that its 15 strict samples are
sample-level measurements rather than validated independent donors.

## Comment 3. The binomial sign test assumes independent genes.

Response: The ECM module has only 6.8 effective independent genes in
GSE70362 and 5.9 in GSE23130. We no longer use the binomial test as the final
evidence layer. We added size-matched and expression-decile-matched empirical
null distributions. For the primary ECM comparison, an expression-matched
null gave a lower-tail empirical probability of 0.0052 and a two-sided
probability of 0.0104.

## Comment 4. The 1,554-module analysis has no multiplicity control.

Response: We added phenotype-label permutation for cohort-specific module
direction, size-matched empirical nulls for gene-level concordance, and
Benjamini-Hochberg FDR on exact two-sided sign tests. Fourteen modules passed
the nominal module-plus-gene gate, but no module survived the exact-sign FDR
gate. Permutation and empirical nulls are retained as sensitivity checks.
Nominal modules are explicitly labelled as a hypothesis-generating shortlist.

## Comment 5. Low cross-cohort concordance may be attenuation caused by
unreliable gene effects.

Response: The strict ECM split-half reliabilities were 0.369 and 0.408. After
Spearman-Brown correction, simulation under zero latent correlation still
predicted approximately 50% sign concordance, whereas the observed value was
23.3%. The observed ECM effect-size correlation was -0.495 and the
disattenuated correlation was -0.884. The result is therefore not a simple
case of low reliability producing a near-chance estimate.

We also added cross-half positive controls. Independent halves of GSE70362
and GSE23130 reached median ECM concordance values of 63.3% and 64.5%,
whereas the cross-cohort value was 23.3%. This shows that the gene-level
metric can recover within-cohort structure.

## Comment 6. The negative result may simply reflect low statistical power.

Response: We agree that power is a central limitation and now quantify it
directly. With the observed reliabilities, the nominal 30-gene sign test had
20.4% power at a latent correlation of 0.6; the effective-n sensitivity
analysis had essentially no power. We therefore describe the result as failure
to establish replication, not proof that a shared programme is absent. The
positive controls show that within-cohort structure is detectable, but a
third matched cohort is still required for a strong domain-wide negative
claim.

## Comment 7. The 15-pair tissue analysis mixes different endpoints.

Response: Pairwise cohorts are now assigned comparability tiers. Primary
pairwise comparisons require the same compartment and endpoint class; all
other pairs are retained as secondary context. The primary pair subset has a
median concordance of 47.0%, and the full 15-pair median remains 49.4%.

## Comment 8. Public data cannot prove a mechanism.

Response: The manuscript does not make a mechanistic claim. It is presented
as a reproducibility audit and reporting framework. The ECM result is phrased
as lack of gene-level cross-cohort support, and the nominally replicated
modules require independent validation before any biological interpretation.

## Comment 9. The methodology is already known.

Response: The contribution is not a new sign-test statistic. It is the
domain-specific empirical demonstration that module-level agreement can fail
gene-level reproducibility, a quantified reproducibility baseline for public
IVD transcriptomes, and a reusable reporting gate. It adds an operational
claim ladder and a sensitivity battery spanning donor dependence, probe
selection, gene identity, scale and FDR-family structure. The manuscript states
this position explicitly rather than claiming a new mechanism or novel
mathematical method.

## Comment 10. Grade is partially confounded with batch or source.

Response: We agree. The strict GSE23130 subset has grade I only in CHTN
specimens and grade IV only in surgical specimens. GSE70362 has grade II only
in batch 1, while batch 2 does not contain grades III-IV. The adjusted
coefficients are therefore interpreted as nuisance-adjusted associations, not
fully identified causal grade effects. Grade-only sensitivity models retained
the primary ECM cross-cohort concordance at 23.3% and similar directional
estimates. Residual confounding is now stated explicitly in the Methods and
Limitations.

## Comment 11. Treating Thompson grade as a numeric variable is not justified.

Response: Grade is not interpreted as an interval-scaled exposure. It is used
only as a strictly increasing ordinal score (I = 1, I-II = 1.5, II = 2, III =
3, IV = 4) to define the sign of a gene-wise monotone trend. Under any
strictly increasing recoding of the same grade order, the sign is unchanged.
Coefficient magnitudes are scale-dependent and are not interpreted as
equal-step dose effects. We now state that the model does not test arbitrary
non-monotonic differences among grades.

## Comment 12. Probe selection may determine gene-level concordance.

Response: We added a probe-collapsing sensitivity analysis using the first
probe, the median across probes and 100 random-probe selections. The primary
highest-mean-probe rule gave 23.3% ECM concordance, while first-probe,
median-probe and random-probe rules gave 30.0%, 33.3% and a median of 36.7%,
respectively. No rule exceeded 50%, but the exact below-chance magnitude was
not robust. We therefore softened the claim from statistically significant
anti-concordance to failure to exceed chance.

## Comment 13. Historical aliases may change gene-set membership.

Response: We added an alias-aware mapping sensitivity using current synonyms
and nomenclature-authority symbols from human gene_info. It recovered 1,098
alias-only platform symbols but left 3,305 unresolved and removed 4,434
ambiguous alias keys. The broad audit expanded from 1,554 to 1,572 modules,
one-cohort signals increased from 673 to 692, and nominal gene-level results
increased from 14 to 15. The number significant in both cohorts remained 31,
the strict FDR result remained 0, and the curated ECM comparison was
unchanged. We now describe broad module counts as mapping-sensitive and avoid
interpreting small nominal changes as stable discoveries.

## Comment 14. Cross-platform scale differences may drive direction calls.

Response: We added scale-invariant gene-wise Spearman trend analyses, both
unadjusted and averaged within batch or source strata. The unadjusted and
stratified analyses gave 33.3% and 36.7% ECM concordance, respectively, with
two-sided p-values of 0.0987 and 0.2005. GSE23130 retained a positive ECM
signal (74.2% up, p = 0.0053), while GSE70362 remained non-directional (53.3%
up, p = 0.4278). We therefore report failure to exceed 50% concordance rather
than statistically significant anti-concordance.

## Comment 15. The FDR family may be too broad because modules overlap.

Response: We repeated Benjamini-Hochberg separately within Hallmark, KEGG and
Reactome. The strict result remained zero in every collection under both
primary and alias-aware mappings. Nominal gene-level results were 0, 3 and 11
for the primary mapping and 0, 3 and 12 after alias mapping. Module overlap
was substantial: 1,636 pairs had Jaccard similarity above 0.5 and 94 above
0.8. We now state that the global FDR result is not explained only by family
dilution, while also avoiding any claim that modules represent thousands of
independent hypotheses.
