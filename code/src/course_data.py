"""Load unmodified course CSV and construct explicitly documented variables."""
from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
_INPUT_CANDIDATES = [ROOT / "data/raw/01_DID/data/public.csv", ROOT / "data/raw/public.csv", ROOT / "01_DID/data/public.csv", ROOT.parent / "data/public.csv"]
INPUT = next((p for p in _INPUT_CANDIDATES if p.is_file()), _INPUT_CANDIDATES[0])


def load_course(input_path=INPUT):
    raw = pd.read_csv(input_path)
    raw.columns = raw.columns.str.lower()
    if raw.shape != (410, 46):
        raise ValueError(f"Unexpected course data dimensions: {raw.shape}")
    required = {"sheet", "state", "chain", "co_owned", "empft", "emppt", "nmgrs",
                "empft2", "emppt2", "nmgrs2", "status2", "wage_st", "wage_st2",
                "bonus", "special2", "hrsopen", "hrsopen2", "psoda", "pfry", "pentree",
                "psoda2", "pfry2", "pentree2"}
    if not required.issubset(raw.columns):
        raise ValueError(f"Missing required columns: {required - set(raw.columns)}")
    for name in raw:
        raw[name] = pd.to_numeric(raw[name], errors="raise")
    if raw.duplicated(["state", "sheet"]).any():
        raise ValueError("Investigate duplicate (state, sheet) before analysis")
    for name, allowed in [("state", [0, 1]), ("chain", [1, 2, 3, 4]),
                          ("co_owned", [0, 1]), ("status2", [0, 1, 2, 3, 4, 5])]:
        if not raw[name].isin(allowed).all():
            raise ValueError(f"Invalid or missing category in {name}")
    for name in ["empft", "emppt", "nmgrs", "empft2", "emppt2", "nmgrs2"]:
        if raw[name].dropna().lt(0).any():
            raise ValueError(f"Negative employment in {name}")
    data = raw.copy()
    data.insert(0, "source_row_id", range(1, len(data) + 1))
    for suffix in ["", "2"]:
        total = data["empft" + suffix] + data["nmgrs" + suffix] + .5 * data["emppt" + suffix]
        if suffix == "2":
            total.loc[data.status2.eq(3)] = 0
            total.loc[data.status2.isin([2, 4, 5])] = float("nan")
        data["fte" + suffix] = total
        # Author's check.sas uses EMPFT / FTE, not a headcount denominator.
        data["fracft" + suffix] = 100 * data["empft" + suffix] / total.where(total.gt(0))
        data["meal_price" + suffix] = data["psoda" + suffix] + data["pfry" + suffix] + data["pentree" + suffix]
    data["change_fte"] = data.fte2 - data.fte
    return raw, data
