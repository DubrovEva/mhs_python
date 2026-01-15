from __future__ import annotations

from pathlib import Path

from hw2.task1.latex_gen import latex_document, latex_image, latex_table


def main() -> None:
    rows = [
        ["Name", "Value", "Note"],
        ["alpha", 3.14, "example"],
        ["beta", 42, "another example"],
        ["gamma", "x & y", "escaping"],
    ]

    artifacts_dir = Path(__file__).resolve().parent.parent / "artifacts"
    artifacts_dir.mkdir(parents=True, exist_ok=True)

    image_path = artifacts_dir / "sample.png"
    table = latex_table(rows)
    image_block = latex_image(
        image_path.name,
        caption="Sample image",
        label="fig:sample",
    )

    document = latex_document([table, "", image_block], packages=["graphicx"])
    (artifacts_dir / "report.tex").write_text(document, encoding="utf-8")


if __name__ == "__main__":
    main()
