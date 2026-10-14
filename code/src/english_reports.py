"""Build English stage reports from checked tables and shared interpretation notes."""
from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]

def markdown_table(frame):
    def cell(value):
        if pd.isna(value): return "-"
        if isinstance(value, float): return format(value, ".6g")
        return str(value).replace("|", "/").replace("\n", " ")
    lines = ["| " + " | ".join(map(str, frame.columns)) + " |", "| " + " | ".join(["---"] * len(frame.columns)) + " |"]
    lines.extend("| " + " | ".join(cell(v) for v in row) + " |" for row in frame.itertuples(index=False, name=None))
    return "\n".join(lines)

def write_report(filename, notes, sections, figures=()):
    text = (ROOT / "ui/reports" / notes).read_text(encoding="utf-8").rstrip()
    text += "\n\n## Current generated results\n\nThe tables below are generated from this run. Interpretation notes describe the assigned course dataset; consult the numeric files for full precision.\n"
    for title, frame in sections:
        text += "\n### " + title + "\n\n" + markdown_table(frame) + "\n"
    for name in figures:
        text += "\n![" + name.replace("_", " ") + "](../figures/" + name + ")\n"
    (ROOT / "outputs/tables" / filename).write_text(text, encoding="utf-8")
