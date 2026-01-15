from pathlib import Path
from hw2.task1.latex_gen import latex_document, latex_table


def main():
    rows = [
        ["Name", "Value", "Note"],
        ["alpha", 3.14, "example"],
        ["beta", 42, "another example"],
        ["gamma", "x & y", "escaping"],
    ]

    table = latex_table(rows)
    document = latex_document([table])

    output_dir = Path(__file__).resolve().parent.parent / "artifacts"
    output_dir.mkdir(parents=True, exist_ok=True)
    (output_dir / "table.tex").write_text(document, encoding="utf-8")


if __name__ == "__main__":
    main()
