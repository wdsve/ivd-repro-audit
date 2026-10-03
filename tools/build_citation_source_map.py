"""Build a traceability map from manuscript citations to source quotations."""

from __future__ import annotations

import re
from pathlib import Path

PROJECT = Path(__file__).resolve().parents[1]
ROOT = PROJECT.parent

SOURCES = {
    "1": {
        "title": "NCBI GEO: archive for functional genomics data sets",
        "doi": "10.1093/nar/gks1193",
        "pdf": "Published abstract via Europe PMC: https://europepmc.org/article/MED/23193258",
        "quote": (
            "The Gene Expression Omnibus (GEO) is an international public "
            "repository for high-throughput microarray and next-generation "
            "sequence functional genomic data sets. The resource supports "
            "archiving of raw data, processed data and metadata."
        ),
        "source_location": "Published abstract, Europe PMC",
    },
    "2": {
        "title": "limma powers differential expression analyses for RNA-sequencing and microarray studies",
        "doi": "10.1093/nar/gkv007",
        "pdf": "Published abstract via Europe PMC: https://europepmc.org/article/MED/25605792",
        "quote": (
            "limma is an R/Bioconductor software package that provides an "
            "integrated solution for analysing data from gene expression "
            "experiments. It contains rich features for handling complex "
            "experimental designs and for information borrowing to overcome "
            "the problem of small sample sizes."
        ),
        "source_location": "Published abstract, Europe PMC",
    },
    "3": {
        "title": "Gene set enrichment analysis: a knowledge-based approach for interpreting genome-wide expression profiles",
        "doi": "10.1073/pnas.0506580102",
        "pdf": "Published abstract via Europe PMC: https://europepmc.org/article/MED/16199517",
        "quote": (
            "The method derives its power by focusing on gene sets, that is, "
            "groups of genes that share common biological function, "
            "chromosomal location, or regulation."
        ),
        "source_location": "Published abstract, Europe PMC",
    },
    "4": {
        "title": "The sva package for removing batch effects and other unwanted variation in high-throughput experiments",
        "doi": "10.1093/bioinformatics/bts034",
        "pdf": "Published abstract via Europe PMC: https://europepmc.org/article/MED/22257669",
        "quote": (
            "Heterogeneity and latent variables are now widely recognized as "
            "major sources of bias and variability in high-throughput "
            "experiments."
        ),
        "source_location": "Published abstract, Europe PMC",
    },
    "5": {
        "title": "Why most published research findings are false",
        "doi": "10.1371/journal.pmed.0020124",
        "pdf": "Published abstract via Europe PMC: https://europepmc.org/article/MED/16060722",
        "quote": (
            "There is increasing concern that most current published research "
            "findings are false. In this framework, a research finding is less "
            "likely to be true when the studies conducted in a field are "
            "smaller; when effect sizes are smaller; when there is greater "
            "flexibility in designs, definitions, outcomes, and analytical "
            "modes."
        ),
        "source_location": "Published abstract, Europe PMC",
    },
    "6": {
        "title": "Investigating the replicability of preclinical cancer biology",
        "doi": "10.7554/eLife.71601",
        "pdf": "Published abstract via Europe PMC: https://europepmc.org/article/MED/34874005",
        "quote": (
            "For positive effects, the median effect size in the replications "
            "was 85% smaller than the median effect size in the original "
            "experiments, and 92% of replication effect sizes were smaller "
            "than the original."
        ),
        "source_location": "Published abstract, Europe PMC",
    },
    "7": {
        "title": "Comparative evaluation of gene selection approaches in transcriptomics: bias correction and visualization with TransPro",
        "doi": "10.1093/gigascience/giag057",
        "pdf": ROOT
        / "12篇文章"
        / "Comparative evaluation of gene selection approaches in transcriptomics bias correction and visualization with TransPro.pdf",
        "quote": (
            "Although multifactor designs can be accommodated, gene–gene "
            "interactions are not explicitly modeled, rendering results "
            "susceptible to systematic bias driven by coexpression patterns."
        ),
        "source_location": "PDF p. 1, Abstract",
    },
    "8": {
        "title": "Cross-Omic Comparative Analysis Identifies Transcriptomic Signatures and Exploratory Gene Set-Level Signals in Sporadic Creutzfeldt-Jakob Disease",
        "doi": "10.3390/ijms27156560",
        "pdf": ROOT
        / "12篇文章"
        / "Cross-Omic Comparative Analysis Identifies Transcriptomic Signatures and Exploratory Gene Set-Level Signals in Sporadic Creutzfeldt-Jakob Disease.pdf",
        "quote": (
            "Under FDR-controlled criteria, cross-omic GO-BP gene set overlap "
            "was not observed. Exploratory nominal-threshold analyses identified "
            "recurrent gene set-level signals, mainly between transcriptomic and "
            "DNA methylation datasets."
        ),
        "source_location": "PDF p. 1, Abstract",
    },
    "9": {
        "title": "Evaluating a Glioma Transcriptomic Signature Against a Clinical Reference Model and a Random-Signature Null Distribution",
        "doi": "10.3390/diagnostics16172803",
        "pdf": ROOT
        / "12篇文章"
        / "Evaluating a Glioma Transcriptomic Signature Against a Clinical Reference Model and a Random-Signature Null Distribution A Leakage-Controlled Internal Audit and a Survey of the Field.pdf",
        "quote": (
            "The signature made no measurable contribution beyond the clinical "
            "reference model. Against a null distribution of 1000 random "
            "20-gene sets drawn from the same candidate pool, the signature "
            "exceeded the null internally (p=0.015) but was indistinguishable "
            "from it in external validation (p=0.154)."
        ),
        "source_location": "PDF p. 1, Abstract",
    },
    "10": {
        "title": "Integrating cross-omics research through FAIR Digital Objects with DataPLANT",
        "doi": "10.1515/jib-2025-0056",
        "pdf": ROOT
        / "12篇文章"
        / "Integrating cross-omics research through FAIR Digital Objects with DataPLANT.pdf",
        "quote": (
            "Parameter variations can be easily tested and results linked "
            "correctly without manual editing of the workflows themselves."
        ),
        "source_location": "PDF p. 1, Abstract",
    },
    "11": {
        "title": "Annotation of cell types in single-cell sequencing for cardiovascular disease",
        "doi": "10.1016/j.biocel.2026.107027",
        "pdf": ROOT
        / "12篇文章"
        / "P5ZvVo_10.1016_j.biocel.2026.107027(科研通-ablesci.com).pdf",
        "quote": (
            "Benchmarking evidence indicates that annotation accuracy depends "
            "more on reference data quality than on algorithmic sophistication. "
            "SingleR, CellTypist, and Azimuth have emerged as leading performers, "
            "whereas ensemble consensus approaches that integrate two or more "
            "independent methods enhance robustness."
        ),
        "source_location": "PDF p. 1, Abstract",
    },
    "12": {
        "title": "Cell-Type-Resolved Pseudobulk Classification Across Independent Cohorts Identifies Microglial PTPRG as a Transcriptional Hub in Alzheimer's Disease",
        "doi": "10.64898/2026.04.07.717029",
        "pdf": ROOT
        / "12篇文章"
        / "Cell-Type-Resolved Pseudobulk Classification Across Independent Cohorts Identifies Microglial PTPRG as a Transcriptional Hub in Alzheimer's Disease.pdf",
        "quote": (
            "A logistic regression model trained on 228 highly variable genes "
            "achieved robust classification performance on held-out ROSMAP "
            "samples and generalized to an independent cohort from the Seattle "
            "Alzheimer's Disease Brain Cell Atlas (balanced accuracy 0.86, "
            "AUC 0.92), demonstrating cross-cohort reproducibility."
        ),
        "source_location": "PDF p. 2, Abstract",
    },
    "13": {
        "title": "Single-cell and spatial transcriptomics characterisation of RSPO2+ nucleus pulposus cells",
        "doi": "10.1016/j.jot.2026.101203",
        "pdf": ROOT
        / "12篇文章"
        / "Single-cell and spatial transcriptomics characterisation of RSPO2+ nucleus pulposus cells reveals.pdf",
        "quote": (
            "Single-cell transcriptomics identified R-spondin 2 (RSPO2) as a "
            "selective marker of a homeostatic NP-resident Cluster 1 compartment "
            "whose proportion contracted after mechanical injury, while "
            "RSPO2-related WNT/FN1–CD44 signalling scores increased across "
            "expanded degenerative effector populations."
        ),
        "source_location": "PDF p. 1, Abstract",
    },
    "14": {
        "title": "ITGBL1 and RPN1 Mark a Fibrotic NP Subpopulation with Coupled Integrin Signaling and N-Glycosylation Programs in IVDD",
        "doi": "10.2147/JIR.S629922",
        "pdf": ROOT
        / "12篇文章"
        / "ITGBL1 and RPN1 Mark a Fibrotic NP Subpopulation with Coupled Integrin Signaling and N-Glycosylation Programs in IVDD.pdf",
        "quote": (
            "Single cell mapping preferentially localized both genes to a "
            "FibroNPC subpopulation and associated this cell state with coupled "
            "integrin/focal adhesion and ER protein processing/N-glycosylation "
            "programs."
        ),
        "source_location": "PDF p. 1, Abstract",
    },
    "15": {
        "title": "An 11-gene blood transcriptomic signature reflects a sepsis-associated host-response pattern across public cohorts",
        "doi": "10.3389/fmed.2026.1844619",
        "pdf": ROOT
        / "12篇文章"
        / "An 11-gene blood transcriptomic signature reflects a sepsis-associated host-response pattern across public cohorts.pdf",
        "quote": (
            "In GSE236713, the standardized fixed-coefficient score showed "
            "moderate discrimination between Day1 OOHCA-SIRS and sepsis "
            "(AUC=0.7676; P=4.74×10−7), whereas the abdominal vs. pulmonary "
            "sepsis and Day 1 survival analyses showed near-null discrimination "
            "(AUC=0.5126 and 0.5291; P=0.8119 and 0.6334, respectively)."
        ),
        "source_location": "PDF p. 1, Abstract",
    },
    "16": {
        "title": "An NLRP3 inflammasome-anchored Astragalus mechanistic prior yields a mortality-associated transcriptomic signal in ICU sepsis",
        "doi": "10.1007/s00011-026-02352-0",
        "pdf": ROOT
        / "12篇文章"
        / "An NLRP3 inflammasome-anchored Astragalus mechanistic prior yields a mortality-associated transcriptomic signal in ICU sepsis a secondary analysis with exploratory cross-cohort assessment.pdf",
        "quote": (
            "Joint MCP-counter adjustment attenuated the association to an OR of "
            "0.79 (95% CI 0.58–1.06), whereas xCell neutrophil adjustment "
            "strengthened it to an OR of 0.64 (95% CI 0.50–0.83), indicating "
            "method-sensitive dependence on estimated cell composition."
        ),
        "source_location": "PDF p. 1, Abstract",
    },
    "17": {
        "title": "Moderated designs can balance between batch-effect mitigation and cell loss due to hashtag-assisted pooling in single-cell experiments",
        "doi": "10.1101/gr.281624.125",
        "pdf": ROOT
        / "12篇文章"
        / "Genome Res.-2026-Chatterjee-gr.281624.125(科研通-ablesci.com).pdf",
        "quote": (
            "We find a linear relationship - the percentage of cells lost is "
            "double the number of hashtags used in the experiment. We use these "
            "analyses to identify experimental designs that can successfully "
            "mitigate batch effects while minimizing multiplexing, hence the "
            "cell loss, in each well."
        ),
        "source_location": "PDF p. 2, Abstract",
    },
    "18": {
        "title": "Estimating the reproducibility of psychological science",
        "doi": "10.1126/science.aac4716",
        "pdf": "Published abstract via Europe PMC: https://europepmc.org/article/MED/26315443",
        "quote": (
            "Replication effects were half the magnitude of original effects, "
            "representing a substantial decline."
        ),
        "source_location": "Published abstract, Europe PMC",
    },
    "19": {
        "title": "Gene Expression Profiling Identifies Interferon Signalling Molecules and IGFBP3 in Human Degenerative Annulus Fibrosus",
        "doi": "10.1038/srep15662",
        "pdf": "Published abstract via Europe PMC: https://europepmc.org/article/MED/26489762",
        "quote": (
            "Microarray analysis revealed 238 differentially expressed genes "
            "in the degenerative annulus fibrosus."
        ),
        "source_location": "Published abstract, Europe PMC",
    },
    "20": {
        "title": "Genome-wide analysis of pain-, nerve- and neurotrophin-related gene expression in the degenerating human annulus",
        "doi": "10.1186/1744-8069-8-63",
        "pdf": "Published abstract via Europe PMC: https://europepmc.org/article/MED/22963171",
        "quote": (
            "Analyses were performed on more generated (Thompson grade IV and V) "
            "discs vs. less degenerated discs (grades I-III)."
        ),
        "source_location": "Published abstract, Europe PMC",
    },
    "21": {
        "title": "Differentially-expressed mRNAs, microRNAs and long noncoding RNAs in intervertebral disc degeneration identified by RNA-sequencing",
        "doi": "10.1080/21655979.2021.1899533",
        "pdf": "Published abstract via Europe PMC: https://europepmc.org/article/MED/33764282",
        "quote": (
            "We randomly selected three samples each from an IDD and a spinal "
            "cord injury group (control) for RNA-sequencing."
        ),
        "source_location": "Published abstract, Europe PMC",
    },
    "22": {
        "title": "Controlling the False Discovery Rate: A Practical and Powerful Approach to Multiple Testing",
        "doi": "10.1111/j.2517-6161.1995.tb02031.x",
        "pdf": "Published metadata and abstract via Crossref: https://doi.org/10.1111/j.2517-6161.1995.tb02031.x",
        "quote": (
            "A different approach to problems of multiple significance testing "
            "is presented. It calls for controlling the expected proportion of "
            "falsely rejected hypotheses - the false discovery rate."
        ),
        "source_location": "Published abstract, Crossref",
    },
    "23": {
        "title": "A Nonstochastic Interpretation of Reported Significance Levels",
        "doi": "10.1080/07350015.1983.10509354",
        "pdf": "Publisher metadata: https://doi.org/10.1080/07350015.1983.10509354",
        "quote": (
            "Publisher metadata does not expose an abstract. This is the "
            "original method citation for residual permutation procedures."
        ),
        "source_location": "Original method paper; publisher abstract unavailable",
    },
    "24": {
        "title": "Adjusting batch effects in microarray expression data using empirical Bayes methods",
        "doi": "10.1093/biostatistics/kxj037",
        "pdf": "Published abstract via Europe PMC: https://europepmc.org/article/MED/16632515",
        "quote": (
            "Non-biological experimental variation or \"batch effects\" are "
            "commonly observed across multiple batches of microarray "
            "experiments, often rendering the task of combining data from "
            "these batches difficult."
        ),
        "source_location": "Published abstract, Europe PMC",
    },
    "25": {
        "title": "Adjusting multiple testing in multilocus analyses using the eigenvalues of a correlation matrix",
        "doi": "10.1038/sj.hdy.6800717",
        "pdf": "Published abstract via Europe PMC: https://europepmc.org/article/MED/16077740",
        "quote": (
            "We propose a more accurate estimate of the M(eff), and design "
            "M(eff)-based procedures to control the experiment-wise significant "
            "level and the false discovery rate."
        ),
        "source_location": "Published abstract, Europe PMC",
    },
    "26": {
        "title": "The MicroArray Quality Control (MAQC) project shows inter- and intraplatform reproducibility of gene expression measurements",
        "doi": "10.1038/nbt1239",
        "pdf": "Published abstract via Europe PMC: https://europepmc.org/article/MED/16964229",
        "quote": (
            "We show intraplatform consistency across test sites as well as a "
            "high level of interplatform concordance in terms of genes "
            "identified as differentially expressed."
        ),
        "source_location": "Published abstract, Europe PMC",
    },
    "27": {
        "title": "Most random gene expression signatures are significantly associated with breast cancer outcome",
        "doi": "10.1371/journal.pcbi.1002240",
        "pdf": "Published abstract via Europe PMC: https://europepmc.org/article/MED/22028643",
        "quote": (
            "Twenty-eight of them (60%) were not significantly better outcome "
            "predictors than random signatures of identical size and 11 (23%) "
            "were worst predictors than the median random signature."
        ),
        "source_location": "Published abstract, Europe PMC",
    },
    "28": {
        "title": "The Strengthening the Reporting of Observational Studies in Epidemiology (STROBE) statement",
        "doi": "10.1016/S0140-6736(07)61602-X",
        "pdf": "Published abstract via Europe PMC: https://europepmc.org/article/MED/18064739",
        "quote": (
            "The reporting of such research is often inadequate, which hampers "
            "the assessment of a study's strengths and weaknesses and of a "
            "study's generalisability."
        ),
        "source_location": "Published abstract, Europe PMC",
    },
    "29": {
        "title": "The FAIR Guiding Principles for scientific data management and stewardship",
        "doi": "10.1038/sdata.2016.18",
        "pdf": "Published abstract via Europe PMC: https://europepmc.org/article/MED/26978244",
        "quote": (
            "The FAIR Principles put specific emphasis on enhancing the ability "
            "of machines to automatically find and use the data, in addition "
            "to supporting its reuse by individuals."
        ),
        "source_location": "Published abstract, Europe PMC",
    },
}

OLD_TO_NEW = {
    "8": 1,
    "9": 2,
    "5": 3,
    "6": 4,
    "18": 5,
    "7": 6,
    "1": 7,
    "19": 8,
    "20": 9,
    "21": 10,
    "2": 11,
    "3": 12,
    "22": 13,
    "23": 14,
    "4": 15,
    "24": 16,
    "25": 17,
    "26": 18,
    "27": 19,
    "28": 20,
    "29": 21,
    "15": 22,
    "16": 23,
    "13": 24,
    "14": 25,
    "11": 26,
    "12": 27,
    "10": 28,
    "17": 29,
}
SOURCES = {
    str(OLD_TO_NEW[old]): SOURCES[old]
    for old in sorted(SOURCES, key=lambda value: OLD_TO_NEW[value])
}


def _citation_pattern(reference: str) -> re.Pattern[str]:
    number = re.escape(reference)
    return re.compile(rf"\[(?:\d+,)*{number}(?:,\d+)*\]")


def _paragraphs(path: Path) -> list[dict[str, object]]:
    lines = path.read_text(encoding="utf-8").splitlines()
    current_section = "Title"
    current_subsection = ""
    counts: dict[str, int] = {}
    paragraphs: list[dict[str, object]] = []
    buffer: list[str] = []

    def flush() -> None:
        if not buffer:
            return
        text = " ".join(part.strip() for part in buffer if part.strip())
        buffer.clear()
        if not text:
            return
        key = f"{current_section}::{current_subsection}"
        counts[key] = counts.get(key, 0) + 1
        paragraphs.append(
            {
                "section": current_section,
                "subsection": current_subsection,
                "paragraph": counts[key],
                "text": text,
            }
        )

    for line in lines:
        if line.startswith("## "):
            flush()
            current_section = line[3:].strip()
            current_subsection = ""
        elif line.startswith("### "):
            flush()
            current_subsection = line[4:].strip()
        elif not line.strip():
            flush()
        elif line.startswith("|") or line.startswith("!") or line.startswith("#"):
            flush()
        else:
            buffer.append(line)
    flush()
    return paragraphs


def _sentence_with_citation(text: str, reference: str, language: str) -> str:
    pattern = _citation_pattern(reference)
    match = pattern.search(text)
    if not match:
        return ""
    del language
    boundary_pattern = (
        r"(?<=[。！？])"
        if re.search(r"[\u4e00-\u9fff]", text)
        else r"(?<=[.!?])\s+"
    )
    boundaries = [
        boundary
        for boundary in re.finditer(boundary_pattern, text)
        if boundary.start() <= match.start()
    ]
    start = 0
    for boundary in reversed(boundaries):
        prefix = text[max(0, boundary.start() - 12) : boundary.end()]
        if re.search(r"(?:et al|vs|e\.g|i\.e|Dr|No)\.\s*$", prefix, re.I):
            continue
        start = boundary.end()
        break
    following = [
        boundary
        for boundary in re.finditer(boundary_pattern, text)
        if boundary.start() >= match.end()
        and not re.search(
            r"(?:et al|vs|e\.g|i\.e|Dr|No)\.\s*$",
            text[max(0, boundary.start() - 12) : boundary.end()],
            re.I,
        )
    ]
    end = following[0].end() if following else len(text)
    return text[start:end].strip()


def _locations(path: Path, language: str) -> dict[str, list[str]]:
    output: dict[str, list[str]] = {reference: [] for reference in SOURCES}
    for paragraph in _paragraphs(path):
        for reference in SOURCES:
            if not _citation_pattern(reference).search(str(paragraph["text"])):
                continue
            section = str(paragraph["section"])
            subsection = str(paragraph["subsection"])
            heading = f"{section} > {subsection}" if subsection else section
            location = f"{heading}, paragraph {paragraph['paragraph']}"
            sentence = _sentence_with_citation(
                str(paragraph["text"]),
                reference,
                language,
            )
            output[reference].append(f"{location}: {sentence}")
    return output


def main() -> None:
    english = _locations(
        PROJECT / "manuscript" / "manuscript.md",
        "en",
    )
    chinese = _locations(
        PROJECT / "manuscript" / "manuscript_zh.md",
        "zh",
    )

    lines = [
        "# Citation Source Map",
        "",
        "This note maps every inserted citation to its source quotation and to "
        "the exact manuscript section and paragraph. PDF page numbers refer to "
        "the local PDF files, not the printed journal page numbers.",
        "",
        "## Quick map",
        "",
        "| Ref | Source quotation | Source location | English manuscript | Chinese manuscript |",
        "|---|---|---|---|---|",
    ]
    for reference, source in SOURCES.items():
        en = "<br>".join(english[reference]) or "Not found"
        zh = "<br>".join(chinese[reference]) or "Not found"
        lines.append(
            f"| [{reference}] | {source['quote']} | {source['source_location']} | "
            f"{en} | {zh} |"
        )

    lines.extend(["", "## Detailed traceability", ""])
    for reference, source in SOURCES.items():
        lines.extend(
            [
                f"### [{reference}] {source['title']}",
                "",
                f"- DOI: `{source['doi']}`",
                f"- Source file/link: `{source['pdf']}`",
                f"- Source location: {source['source_location']}",
                "",
                "**Original quotation**",
                "",
                f"> {source['quote']}",
                "",
                "**English manuscript citations**",
                "",
            ]
        )
        lines.extend(f"- {item}" for item in english[reference])
        lines.extend(["", "**Chinese manuscript citations**", ""])
        lines.extend(f"- {item}" for item in chinese[reference])
        lines.append("")

    output = PROJECT / "docs" / "citation_source_map.md"
    output.write_text("\n".join(lines), encoding="utf-8")
    print(output)


if __name__ == "__main__":
    main()
