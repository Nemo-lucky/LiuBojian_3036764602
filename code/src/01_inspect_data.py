"""Initial audit only. This does not reproduce the assigned tables or figure."""
from pathlib import Path
import json
import re
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]


def main():
    raw = ROOT / "data" / "raw" / "author"
    entries = []
    for line in (raw / "codebook").read_text(encoding="latin-1").splitlines():
        match = re.match(r"^([A-Z][A-Z0-9_]*)\s+(\d+)\s+(\d+)\s+\d+\.\d+\s+(.+)$", line)
        if match:
            name, start, end, description = match.groups()
            entries.append((name.lower(), int(start) - 1, int(end), description))
    if len(entries) != 46:
        raise ValueError(f"Expected 46 documented variables, found {len(entries)}")
    frame = pd.read_fwf(
        raw / "public.dat", colspecs=[(s, e) for _, s, e, _ in entries],
        names=[n for n, _, _, _ in entries], header=None, na_values=["."],
    )
    for column in frame:
        frame[column] = pd.to_numeric(frame[column], errors="raise")
    if len(frame) != 410:
        raise ValueError("Sample size does not match the codebook")
    # SHEET is not globally unique in the actual archive: 407 occurs in both states.
    # Keep both observations, preserve the source row, and verify the composite key.
    if frame.duplicated(["state", "sheet"]).any():
        raise ValueError("Duplicate state + sheet key requires investigation")
    frame.insert(0, "source_row_id", range(1, len(frame) + 1))
    if not frame.state.isin([0, 1]).all():
        raise ValueError("Invalid state code")
    if not frame.status2.isin([0, 1, 2, 3, 4, 5]).all():
        raise ValueError("Invalid second-interview status")

    # Original paper: full-time employees + managers + 0.5 * part-time employees.
    # Ordinary addition preserves missing components as missing total employment.
    frame["fte_before"] = frame.empft + frame.nmgrs + 0.5 * frame.emppt
    frame["fte_after"] = frame.empft2 + frame.nmgrs2 + 0.5 * frame.emppt2
    # Baseline paper convention: permanent closures have zero employment;
    # temporary closures / renovations remain missing in the baseline.
    frame.loc[frame.status2.eq(3), "fte_after"] = 0
    frame.loc[frame.status2.isin([2, 4, 5]), "fte_after"] = float("nan")
    frame["change_fte"] = frame.fte_after - frame.fte_before
    processed = ROOT / "data" / "processed"
    results = ROOT / 'outputs' / 'tables'
    processed.mkdir(parents=True, exist_ok=True)
    results.mkdir(parents=True, exist_ok=True)
    frame.to_csv(processed / "initial_analysis.csv", index=False)

    pd.DataFrame(entries, columns=["variable", "start_zero_based", "end_exclusive", "definition"]).to_csv(
        results / "variable_dictionary.csv", index=False
    )
    frame.isna().sum().rename("missing_count").to_csv(results / "missing_counts.csv")
    summary = frame.groupby("state").agg(
        stores=("sheet", "size"), fte_before_n=("fte_before", "count"),
        fte_before_mean=("fte_before", "mean"), fte_after_n=("fte_after", "count"),
        fte_after_mean=("fte_after", "mean"), paired_n=("change_fte", "count"),
        paired_change_mean=("change_fte", "mean"),
    )
    summary.index = summary.index.map({0: "PA", 1: "NJ"})
    summary.to_csv(results / "initial_state_summary.csv")
    status = frame.status2.value_counts().sort_index().to_dict()
    audit = {"stores": len(frame), "raw_variables": len(entries), "sheet_globally_unique": bool(frame.sheet.is_unique),
             "state_sheet_key_unique": True,
             "duplicate_sheet_records": frame.loc[frame.sheet.duplicated(keep=False), ["source_row_id", "sheet", "state", "chain"]].to_dict(orient="records"),
             "warning": "SHEET 407 occurs in two states; both records retained; source_row_id added.",
             "state_counts": summary.stores.to_dict(), "status_counts": {str(k): int(v) for k, v in status.items()},
             "status": "Initial audit passed; core replication and extension remain unfinished."}
    (results / "initial_audit.json").write_text(json.dumps(audit, indent=2), encoding="utf-8")
    print(summary.to_string())
    print("Initial audit passed. These are preliminary checks, not final replication results.")


if __name__ == "__main__":
    main()
