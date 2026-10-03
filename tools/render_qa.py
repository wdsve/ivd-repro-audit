"""Re-render per-page QA proof images for the JBI submission PDFs.

For each document folder under jbi_submission/qa/:
1. Copy the latest PDF from jbi_submission/ into the folder.
2. Render every page to page-XX.png at 150 dpi with PyMuPDF.
Old page-*.png files are removed first so stale pages cannot survive.
"""

from __future__ import annotations

import re
import shutil
from pathlib import Path

import pymupdf

PROJECT = Path(__file__).resolve().parents[1]
SUBMISSION = PROJECT / "jbi_submission"
QA = SUBMISSION / "qa"

DOCUMENTS = {
    "manuscript": "JBI_Manuscript.pdf",
    "title_page": "JBI_Title_Page.pdf",
    "cover_letter": "JBI_Cover_Letter.pdf",
    "declarations": "JBI_Declarations.pdf",
    "supplement": "JBI_Supplement.pdf",
}

DPI = 150


def render_folder(folder: Path, pdf_name: str) -> int:
    source_pdf = SUBMISSION / pdf_name
    if not source_pdf.exists():
        print(f"SKIP {pdf_name}: source missing")
        return 0
    folder.mkdir(parents=True, exist_ok=True)
    target_pdf = folder / pdf_name
    shutil.copy2(source_pdf, target_pdf)
    for old_png in folder.glob("page-*.png"):
        old_png.unlink()
    document = pymupdf.open(target_pdf)
    page_count = document.page_count
    digits = max(2, len(str(page_count)))
    zoom = DPI / 72.0
    matrix = pymupdf.Matrix(zoom, zoom)
    for index in range(page_count):
        pixmap = document.load_page(index).get_pixmap(matrix=matrix, alpha=False)
        pixmap.save(folder / f"page-{index + 1:0{digits}d}.png")
    document.close()
    print(f"OK {pdf_name}: {page_count} pages -> {folder.name}/")
    return page_count


def main() -> None:
    total = 0
    for folder_name, pdf_name in DOCUMENTS.items():
        total += render_folder(QA / folder_name, pdf_name)
    print(f"Done. {total} pages rendered across {len(DOCUMENTS)} documents.")


if __name__ == "__main__":
    main()
