"""Synchronize the report generator reference list from the Chinese manuscript."""

from pathlib import Path

PROJECT = Path(__file__).resolve().parents[1]
REPORT = PROJECT / "ivd_audit" / "report.py"
ZH = PROJECT / "manuscript" / "manuscript_zh.md"


def main() -> None:
    zh_text = ZH.read_text(encoding="utf-8")
    references = zh_text.split("## 参考文献", 1)[1].strip() + "\n"

    report_text = REPORT.read_text(encoding="utf-8")
    heading = report_text.index("## References")
    content_start = heading + len("## References")
    closing_quote = report_text.index('"""', content_start)
    REPORT.write_text(
        report_text[:content_start] + "\n\n" + references + report_text[closing_quote:],
        encoding="utf-8",
    )


if __name__ == "__main__":
    main()
