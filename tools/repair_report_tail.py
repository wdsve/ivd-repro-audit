"""Repair the report generator after the DOI bulk-edit formatting accident."""

from pathlib import Path

PROJECT = Path(__file__).resolve().parents[1]
REPORT = PROJECT / "ivd_audit" / "report.py"

TAIL = r'''
"""

    (manuscript_dir / "manuscript.md").write_text(manuscript, encoding="utf-8")

    abstract_zh = f"""# 中文摘要

**标题：** 模块层面一致不等于复制：公共人椎间盘转录组的报告与可复现性门槛

**背景：** 公共椎间盘转录组研究常把单队列中显著的模块，或两个队列中
方向相似的模块，写成“一致”或“验证”。但模块方向可以由不同基因子集
驱动；如果不检查基因级方向一致率，模块层面的相似性无法证明同一个
生物学程序被复制。

**方法：** 审计 6 个公共人椎间盘组织转录组队列，并对两个最大的分级纤维环
队列 GSE70362 与 GSE23130 做匹配分析。严格比较限定为 Thompson I-IV 级、
纤维环、LCM 样本；效应量使用校正批次或组织来源的线性模型估计。对每个
基因集同时报告队列内方向、精确符号检验和跨队列基因级方向一致率。还审计
1,554 个 Hallmark、KEGG 和 Reactome 模块，并用 100 次分层 split-half
评估队列内部可靠性；同时加入供者单样本、供者 cluster bootstrap、
phenotype permutation、表达匹配零模型和 FDR 控制。

**结果：** 严格比较中，GSE23130 的 ECM 重塑模块有
{_pct(strict["gse23130_ecm_fraction_up"])} 个基因上调
（p = {_p(strict["gse23130_ecm_sign_p"])}），GSE70362 仅
{_pct(strict["gse70362_ecm_fraction_up"])} 个基因上调
（p = {_p(strict["gse70362_ecm_sign_p"])}）。但两队列 ECM 基因级方向
一致率只有 {_pct(strict["ecm_sign_concordance"])}
（双侧符号检验 p = {_p(strict["ecm_sign_concordance_p_two_sided"])}），
低于随机的 50%。
两个队列内部 split-half 相关系数分别为 {rel_70362:.2f} 和
{rel_23130:.2f}。供者单样本和 cluster bootstrap 分析也维持约 50% 的
GSE70362 ECM 方向和约 30% 的跨队列一致率，说明失败并非单纯由单队列
噪声或供者重复采样造成。

在 1,554 个模块中，{summary["msigdb"]["n_significant_one_sided"]} 个只在
一个队列显著，{summary["msigdb"]["n_significant_both"]} 个在双队列显著，
只有 {summary["msigdb"]["n_gene_level_replicated"]} 个通过名义基因级复核；
加入 permutation 和 FDR 后为 {summary["msigdb"]["n_replicated_fdr"]} 个。
15 对组织队列的中位基因级方向一致率为
{_pct(summary["pairwise_tissue"]["median_gene_concordance"])}，最高仅
{_pct(summary["pairwise_tissue"]["max_gene_concordance"])}。

**结论：** 椎间盘公共转录组中的模块级“一致性”不能替代基因级跨队列
复制。任何“replicated”或“consistent”表述，都应同时给出模块方向、
基因级方向一致率和内部可靠性；单队列模块只能写作探索性发现。
"""
    (manuscript_dir / "abstract_zh.md").write_text(abstract_zh, encoding="utf-8")

    supplement = f"""# Supplementary material

## Table S1. Primary comparison

{_markdown_table(primary_table)}

## Table S2. Cohort effect diagnostics

{_markdown_table(diagnostic_table)}

## Table S3. Internal split-half reliability

{_markdown_table(reliability)}

## Table S4. Full MSigDB audit

The complete audit of {len(msigdb)} modules is provided as
`results/msigdb_module_audit.csv`.

## Table S5. Pairwise tissue cohort concordance

{_markdown_table(pairwise_display)}

## Table S6. Prespecified mechanism modules

The complete comparison is provided as
`results/curated_module_audit.csv`.

## Table S7. Donor-level sensitivity

{_markdown_table(donor_table)}

## Table S8. Reliability attenuation

{_markdown_table(attenuation_table)}

## Table S9. Effective independent genes

{_markdown_table(effective_genes)}

## Table S10. Expression-matched ECM null

{_markdown_table(pd.DataFrame([expression_matched]).rename(columns={"index": "module"}))}

## Table S11. Cross-half positive controls

{_markdown_table(cross_half_table)}

## Table S12. Weighted concordance

{_markdown_table(weighted_table)}

## Table S13. Power calibration

{_markdown_table(power_table)}

## Table S14. Module score slopes

{_markdown_table(module_score_table)}

## Table S15. Permutation-method sensitivity

{_markdown_table(permutation_method_table)}

## Table S16. Exact-contrast cohort pairs

{_markdown_table(pairwise_exact_display)}

## Table S17. Compartment-matched cohort pairs

{_markdown_table(pairwise_compartment_display)}

## Table S18. GSE176205 NP directional validation

{_markdown_table(gse176205_display)}

## Table S19. GSE17077 paired senescence analysis

{_markdown_table(gse17077_display)}

## Table S20. Third-cohort registry summary

{_markdown_table(third_cohort_summary)}

## Table S21. Literature scoping audit

{_markdown_table(literature_table)}

## Table S22. Reproduced blood cohorts

{_markdown_table(blood_table)}

## Table S23. Probe-to-symbol collapsing sensitivity

{_markdown_table(probe_table)}

The primary analysis used the highest-mean probe per gene. Alternative
collapsing rules and 100 random-probe selections did not exceed 50% ECM
concordance, but they showed that the exact below-chance level in the primary
analysis was sensitive to probe selection.

## Table S24. Gene-identity sensitivity

{_markdown_table(gene_identity_table)}

The primary mapping retained supplied platform symbols. The alias-aware
mapping additionally used current synonyms and nomenclature-authority symbols
from human gene_info. It recovered 1,098 alias-only symbols but left 3,305
unresolved and removed 4,434 ambiguous alias keys. The strict FDR conclusion
remained zero modules, while broader nominal counts changed modestly.

## Table S25. Scale-invariant trend sensitivity

{_markdown_table(scale_table)}

Spearman trends are invariant to any strictly increasing transformation of
each gene across samples and therefore test whether the direction call is
driven by platform-specific scale assumptions. The stratified analysis
averages gene-wise Spearman trends within batch or source strata with at least
four samples and three observed grades.

## Table S26. Module-family FDR and overlap sensitivity

{_markdown_table(family_table)}

The module sets were not independent. Among 1,554 tested modules, 243,830
pairs had nonzero Jaccard overlap, 1,636 exceeded Jaccard 0.5 and 94 exceeded
0.8. Collection-local FDR was zero for Hallmark, KEGG and Reactome under both
primary and alias-aware mappings.

## Technical diagnostic tables

The grade, batch, processing-method and source crosstabs are provided in
`results/confound_*.csv`. These tables are part of the stopping rules: the
unrestricted GSE23130 comparison is not used as the primary replication test
because grade V occurs only in homogenized samples.
"""
    (manuscript_dir / "supplement.md").write_text(supplement, encoding="utf-8")

    cover = f"""# Cover letter

Dear Editor,

We submit a methodological audit and reporting framework for cross-cohort
reproducibility in public human intervertebral disc transcriptomes. The
central finding is that module-level significance is not replication. In a
strictly matched grade I-IV annulus fibrosus comparison, the ECM remodelling
module was significant and internally reproducible in GSE23130 but had only
{_pct(strict["ecm_sign_concordance"])} gene-level directional concordance with
GSE70362. This result persisted in donor-level one-sample and cluster-bootstrap
analyses.

The manuscript provides a reusable audit workflow and a reporting standard
for public-data studies in this field. It does not claim a new disease
mechanism and does not overstate the limited causal value of public
transcriptomes.

Sincerely,

The submitting author
"""
    (manuscript_dir / "cover_letter.md").write_text(cover, encoding="utf-8")
'''


def main() -> None:
    text = REPORT.read_text(encoding="utf-8")
    references = text.index("## References")
    end_quote = text.index('"""', references)
    REPORT.write_text(text[:end_quote] + TAIL, encoding="utf-8")


if __name__ == "__main__":
    main()
