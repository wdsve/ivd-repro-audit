"""Validate citation order and reference coverage in the manuscripts."""

from __future__ import annotations

import argparse
import re
from pathlib import Path

PROJECT = Path(__file__).resolve().parents[1]


def _body_and_references(text: str, heading: str) -> tuple[str, str]:
    marker = f"## {heading}"
    if marker not in text:
        raise ValueError(f"missing heading: {marker}")
    body, references = text.split(marker, 1)
    return body, references


def _citation_order(body: str) -> list[int]:
    order: list[int] = []
    for match in re.finditer(r"\[([0-9,\s]+)\]", body):
        for value in re.findall(r"\d+", match.group(1)):
            number = int(value)
            if number not in order:
                order.append(number)
    return order


def _reference_numbers(references: str) -> list[int]:
    return [
        int(match.group(1))
        for match in re.finditer(r"(?m)^(\d+)\.\s", references)
    ]


def _reference_blocks(references: str) -> dict[int, str]:
    pattern = re.compile(r"(?ms)^(\d+)\.\s+(.*?)(?=^\d+\.\s|\Z)")
    return {
        int(match.group(1)): match.group(2).strip()
        for match in pattern.finditer(references)
    }


def _lint(path: Path, heading: str) -> list[str]:
    body, references = _body_and_references(
        path.read_text(encoding="utf-8"),
        heading,
    )
    order = _citation_order(body)
    reference_numbers = _reference_numbers(references)
    reference_blocks = _reference_blocks(references)
    errors: list[str] = []

    expected = list(range(1, len(order) + 1))
    if order != expected:
        errors.append(
            f"first-citation order is {order}, expected {expected}"
        )
    if sorted(reference_numbers) != reference_numbers:
        errors.append("reference list is not in ascending numeric order")
    if len(reference_numbers) != len(set(reference_numbers)):
        errors.append("reference list contains duplicate numbers")
    if set(order) != set(reference_numbers):
        errors.append(
            "inline citations and reference list differ: "
            f"inline={sorted(set(order))}, refs={sorted(set(reference_numbers))}"
        )
    missing_dois: list[int] = []
    duplicate_dois: list[tuple[int, list[str]]] = []
    seen_dois: dict[str, int] = {}
    for number, block in reference_blocks.items():
        dois = re.findall(r"\bdoi:(10\.\S+)", block, re.I)
        if not dois:
            missing_dois.append(number)
            continue
        if len(dois) != 1:
            duplicate_dois.append((number, dois))
        for doi in dois:
            key = doi.rstrip(".").lower()
            if key in seen_dois:
                errors.append(
                    f"DOI appears in refs {seen_dois[key]} and {number}: {doi}"
                )
            else:
                seen_dois[key] = number
    if missing_dois:
        errors.append(f"references without DOI: {missing_dois}")
    if duplicate_dois:
        errors.append(f"references containing multiple DOIs: {duplicate_dois}")
    return errors


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--project-root",
        type=Path,
        default=Path(__file__).resolve().parents[2],
    )
    args = parser.parse_args()
    root = args.project_root.resolve()
    manuscript_dir = root / "ivd_repro_audit" / "manuscript"

    checks = [
        (manuscript_dir / "manuscript.md", "References"),
        (manuscript_dir / "manuscript_zh.md", "参考文献"),
    ]
    failed = False
    for path, heading in checks:
        errors = _lint(path, heading)
        if errors:
            failed = True
            print(f"FAIL: {path.name}")
            for error in errors:
                print(f"  - {error}")
        else:
            print(f"OK: {path.name}")
    if failed:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
