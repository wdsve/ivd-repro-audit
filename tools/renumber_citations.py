"""Renumber manuscript citations by first occurrence and reorder references."""

from __future__ import annotations

import argparse
import re
from pathlib import Path

PROJECT = Path(__file__).resolve().parents[1]


def _citation_order(body: str) -> list[int]:
    order: list[int] = []
    for match in re.finditer(r"\[([1-9][0-9,\s]*)\]", body):
        for value in re.findall(r"\d+", match.group(1)):
            number = int(value)
            if number not in order:
                order.append(number)
    return order


def _reference_blocks(references: str) -> dict[int, str]:
    pattern = re.compile(
        r"(?ms)^(\d+)\.\s+(.*?)(?=^\d+\.\s|\Z)"
    )
    blocks = {
        int(match.group(1)): match.group(2).strip()
        for match in pattern.finditer(references)
    }
    if not blocks:
        raise ValueError("no numbered references found")
    return blocks


def _replace_citations(text: str, mapping: dict[int, int]) -> str:
    def replacement(match: re.Match[str]) -> str:
        old_numbers = [int(value) for value in re.findall(r"\d+", match.group(1))]
        return "[" + ",".join(str(mapping[value]) for value in old_numbers) + "]"

    return re.sub(r"\[([1-9][0-9,\s]*)\]", replacement, text)


def _renumber(
    text: str,
    *,
    start_marker: str,
    reference_heading: str,
    end_marker: str | None,
) -> str:
    start = text.index(start_marker) + len(start_marker)
    end = text.rindex(end_marker, start) if end_marker else len(text)
    segment = text[start:end]
    body, references = segment.split(f"## {reference_heading}", 1)
    order = _citation_order(body)
    blocks = _reference_blocks(references)
    if set(order) != set(blocks):
        raise ValueError(
            f"inline citations {sorted(set(order))} do not match "
            f"references {sorted(blocks)}"
        )
    mapping = {old: new for new, old in enumerate(order, start=1)}
    renumbered_body = _replace_citations(body, mapping)
    renumbered_references = "\n\n".join(
        f"{mapping[old]}. {re.sub(r'\\s+', ' ', blocks[old])}"
        for old in order
    )
    new_segment = (
        renumbered_body
        + f"## {reference_heading}\n\n"
        + renumbered_references
        + "\n"
    )
    return text[:start] + new_segment + text[end:]


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--project-root",
        type=Path,
        default=Path(__file__).resolve().parents[2],
    )
    args = parser.parse_args()
    root = args.project_root.resolve()
    project = root / "ivd_repro_audit"

    report_path = project / "ivd_audit" / "report.py"
    report_path.write_text(
        _renumber(
            report_path.read_text(encoding="utf-8"),
            start_marker='manuscript = f"""',
            reference_heading="References",
            end_marker='"""',
        ),
        encoding="utf-8",
    )

    zh_path = project / "manuscript" / "manuscript_zh.md"
    zh_path.write_text(
        _renumber(
            zh_path.read_text(encoding="utf-8"),
            start_marker="# ",
            reference_heading="参考文献",
            end_marker=None,
        ),
        encoding="utf-8",
    )


if __name__ == "__main__":
    main()
