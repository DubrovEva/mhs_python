from typing import Iterable, List, Optional, Sequence, Tuple


_LATEX_ESCAPES = {
    "&": r"\&",
    "%": r"\%",
    "$": r"\$",
    "#": r"\#",
    "_": r"\_",
    "{": r"\{",
    "}": r"\}",
    "~": r"\textasciitilde{}",
    "^": r"\textasciicircum{}",
    "\\": r"\textbackslash{}",
}


def escape_latex(text: str) -> str:
    return "".join(_LATEX_ESCAPES.get(ch, ch) for ch in text)


def _normalize_table_rows(
    rows: Sequence[Sequence[object]],
) -> Tuple[List[List[str]], int]:
    if not rows:
        raise ValueError("table data must not be empty")

    max_cols = max(len(row) for row in rows)
    if max_cols == 0:
        raise ValueError("table rows must contain at least one column")

    normalized = [
        [escape_latex(str(value)) for value in row] + [""] * (max_cols - len(row))
        for row in rows
    ]
    return normalized, max_cols


def latex_table(rows: Sequence[Sequence[object]]) -> str:
    normalized, col_count = _normalize_table_rows(rows)
    column_spec = "|".join(["l"] * col_count)

    lines = [
        rf"\begin{{tabular}}{{|{column_spec}|}}",
        r"\hline",
    ]
    lines.extend(
        " & ".join(row) + r" \\ \hline" for row in normalized
    )
    lines.append(r"\end{tabular}")
    return "\n".join(lines)


def latex_image(
    path: str,
    caption: Optional[str] = None,
    label: Optional[str] = None,
    width: str = r"0.6\textwidth",
) -> str:
    lines = [r"\begin{figure}[h!]"]
    lines.append(r"\centering")
    lines.append(rf"\includegraphics[width={width}]{{{escape_latex(path)}}}")
    if caption:
        lines.append(rf"\caption{{{escape_latex(caption)}}}")
    if label:
        lines.append(rf"\label{{{escape_latex(label)}}}")
    lines.append(r"\end{figure}")
    return "\n".join(lines)


def latex_document(body: Iterable[str], packages: Iterable[str] = ()) -> str:
    package_lines = [rf"\usepackage{{{pkg}}}" for pkg in packages]
    lines = [r"\documentclass{article}", *package_lines, r"\begin{document}"]
    lines.extend(body)
    lines.append(r"\end{document}")
    return "\n".join(lines)
