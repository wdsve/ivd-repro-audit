# JBI 投稿包修订报告（2026-10-03）

对象：*Module-level agreement is not replication*（投 Journal of Biomedical Informatics，Special Communication）

## 一、已完成修改

### 1. 结构与合规（违反 JBI 硬性要求项）
| 问题 | 处理 |
|---|---|
| Box 1（五级声明阶梯表）被构建脚本删除，正文 4.3/5.4 悬空引用 | 修改 `tools/build_jbi_submission.py`，Box 1 表保留为正文第 3 个展示项 |
| 全文无任何图表引用（JBI 要求 cite all figures/tables in text） | 源稿 `manuscript/manuscript.md` 补了 25+ 处引用：Table 1/2、Figure 1-5、Table S2-S27、Figure S1 |
| 图+表上限 8：恢复 Box 1 后超限 | Figure 6（阳性对照+功效校准）移至补充材料为 Figure S1 → 正文 5 图 + 3 表 = 8 |
| JBI_Manuscript 缺 Keywords 行 | 摘要后插入，与标题页一致：reproducibility; transcriptomics; bioinformatics; gene-sets; intervertebral-disc |
| JBI_Manuscript.md 与 docx 不同步（md 无表、docx 有 2 表） | 构建脚本把 Table 1/Table 2 同时写入 md 与 docx |
| Table 2 把 probe 敏感性 3 条规则压缩成 1 行，正文讨论无数据支撑 | Table 2 扩为 6 行（全样本/严格调整/仅分级/first/median/random probe） |
| Cover letter "lower-than-chance concordance" 与正文弱化结论矛盾 | 改为 "gene-level concordance that does not exceed chance" |
| 标题页 Figures/Tables 计数过时 | 更新为 Figures: 5、Tables: 3 (Tables 1-2 and Box 1)、Supplementary: Tables S1-S27, Figure S1 |
| 补充材料缺名义复制模块清单（正文表无处可引） | supplement.md 新增 Table S27（top 10，注明假设生成性质）与 Figure S1 图例；S1/S23 注明已合并进正文 Table 2 |

### 2. 参考文献联网核实（Crossref API 逐条核对元数据）
**10 条 2026 年新文献全部真实存在**，作者、期刊、卷期均匹配：

| Ref | DOI | 结论 |
|---|---|---|
| 1 | 10.3390/ijms27156560 | 真实（IJMS 2026;27(15):6560，作者 Oberoi/Gurung/Harris 匹配）|
| 2 | 10.3390/diagnostics16172803 | 真实 |
| 6 | 10.1093/gigascience/giag057 | 真实（GigaScience 2026;15）|
| 22 | 10.3389/fmed.2026.1844619 | 真实 |
| 23 | 10.1007/s00011-026-02352-0 | 真实（Inflamm Res 2026;75:201）|
| 24 | 10.1016/j.jot.2026.101203 | 真实（JOT 2026;60）|
| 25 | 10.2147/JIR.S629922 | 真实，但 "19:629922" 页码错误（Crossref 页码 1-20 为占位）→ 已改为 `2026;19. doi:...` |
| 26 | 10.1016/j.biocel.2026.107027 | 真实（IJBCB 2026;201）|
| 27 | 10.64898/2026.04.07.717029 | 真实——10.64898 是 bioRxiv/openRxiv 2026 年新前缀，非伪造 |
| 29 | 10.1101/gr.281624.125 | 真实，已有正式卷期页 → 更新为 `2026;36:2027-2036` |

注意：ref 1/2/22/23 是与本文风格相似的"审计"类文章，若其中有作者本人的工作，投稿时建议在 cover letter 中主动说明关联，避免编辑误判。

### 3. 重新生成的文件
- `jbi_submission/JBI_Manuscript.docx`（4 表：Significance + Table 1 + Table 2 + Box 1；5 张正文图）
- `JBI_Manuscript.md`、`JBI_Title_Page.*`、`JBI_Cover_Letter.*`、`JBI_Declarations.*`、`JBI_Supplement.docx`
- `figures/Figure_1..5.png/pdf` + `figures/Figure_S1.png/pdf`（旧 Figure_6 文件已删除）
- 合规数字：摘要 220 词（≤300 ✓）、正文 4,794 词（≤6,000 ✓）、Significance 46 词（≤150 ✓）、正文展示项 5 图 + 3 表 = 8（≤8 ✓）

## 二、仍需人工完成（投稿前 checklist）
1. ~~PDF 全部过期~~ → **已解决（2026-10-03 10:50）**：安装 LibreOffice 26.8 到 `D:\LibreOffice`，5 个 PDF 已用 soffice 重新生成；`qa/` 31 页逐页校对图已用 `tools/render_qa.py`（PyMuPDF, 150 dpi）重新渲染，抽查页面渲染正常。中文稿 manuscript_zh.md / abstract_zh.md 已与英文版同步。
2. **作者信息**：JBI_Title_Page 中 Authors/Affiliations/Corresponding author 及 Declarations 中 CRediT 角色仍为占位符。
3. **数据可用性**：Elsevier Option C 要求寄存并引用——建议 GitHub 存档 + Zenodo 打 DOI，填入 Data Statement 和正文 Data Availability（当前为 `[repository URL and DOI]` 占位）。
4. **利益声明**：JBI 要求用 Elsevier 在线声明工具（https://declarations.elsevier.com）生成正式 Word 文件，替换脚本生成的 JBI_Declarations.docx。
5. **图形摘要**：JBI_Graphical_Abstract 为程序生成的简易图，建议人工美化；尺寸 1328x531 符合要求。
6. 若投稿系统要求可编辑源文件，提交 docx 即可（JBI 不收 PDF 源文件）。

## 三、未改动项
- 分析结果与数字未动（未重跑 run_audit.py）
- manuscript_zh.md 中文稿未同步（如需可后续处理）
- ldh_pipeline/ 与本文无关，未触碰
