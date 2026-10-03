"""Append the canonical DOI to every numbered reference."""

from __future__ import annotations

import re
from pathlib import Path

PROJECT = Path(__file__).resolve().parents[1]

DOIS = {
    1: "10.3390/ijms27156560",
    2: "10.3390/diagnostics16172803",
    3: "10.1371/journal.pmed.0020124",
    4: "10.7554/eLife.71601",
    5: "10.1126/science.aac4716",
    6: "10.1093/gigascience/giag057",
    7: "10.1093/nar/gks1193",
    8: "10.1038/srep15662",
    9: "10.1186/1744-8069-8-63",
    10: "10.1080/21655979.2021.1899533",
    11: "10.1093/nar/gkv007",
    12: "10.1073/pnas.0506580102",
    13: "10.1111/j.2517-6161.1995.tb02031.x",
    14: "10.1080/07350015.1983.10509354",
    15: "10.1093/bioinformatics/bts034",
    16: "10.1093/biostatistics/kxj037",
    17: "10.1038/sj.hdy.6800717",
    18: "10.1038/nbt1239",
    19: "10.1371/journal.pcbi.1002240",
    20: "10.3389/fmed.2026.1844619",
    21: "10.1007/s00011-026-02352-0",
    22: "10.1016/j.jot.2026.101203",
    23: "10.2147/JIR.S629922",
    24: "10.1016/j.biocel.2026.107027",
    25: "10.64898/2026.04.07.717029",
    26: "10.1515/jib-2025-0056",
    27: "10.1101/gr.281624.125",
    28: "10.1016/S0140-6736(07)61602-X",
    29: "10.1038/sdata.2016.18",
}


def _add_dois(text: str) -> str:
    pattern = re.compile(r"(?ms)^(\d+)\.\s+(.*?)(?=^\d+\.\s|\Z)")
    blocks: dict[int, str] = {}
    for match in pattern.finditer(text):
        number = int(match.group(1))
        content = re.sub(r"\s+", " ", match.group(2)).strip()
        content = re.sub(r"\bdoi:\S+", "", content)
        content = re.sub(r"\s+([.;])", r"\1", content)
        content = re.sub(r"\s{2,}", " ", content).strip()
        content = re.sub(r"\s+Preprint\.\s*$", " Preprint.", content)
        blocks[number] = f"{number}. {content} doi:{DOIS[number]}"
    if set(blocks) != set(DOIS):
        raise ValueError(
            f"expected references {sorted(DOIS)}, found {sorted(blocks)}"
        )
    return "\n\n".join(blocks[number] for number in sorted(blocks)) + "\n"


def _update(path: Path, heading: str, end_marker: str | None) -> None:
    text = path.read_text(encoding="utf-8")
    marker = f"## {heading}"
    start = text.index(marker) + len(marker)
    end = text.index(end_marker, start) if end_marker else len(text)
    references = _add_dois(text[start:end])
    path.write_text(
        text[:start] + "\n\n" + references + text[end:],
        encoding="utf-8",
    )


def main() -> None:
    _update(
        PROJECT / "ivd_audit" / "report.py",
        heading="References",
        end_marker='"""',
    )
    _update(
        PROJECT / "manuscript" / "manuscript_zh.md",
        heading="参考文献",
        end_marker=None,
    )


if __name__ == "__main__":
    main()
