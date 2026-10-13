"""Reproduce Table 2 from the course CSV; disclose sample and rounding differences."""
import hashlib
import argparse
import json
import re
from pathlib import Path
from datetime import datetime, timezone
import numpy as np
import pandas as pd
from course_data import ROOT, INPUT, load_course
from audit_table2 import audit


def compare_author(raw):
    directory = ROOT / "data/raw/author"
    if not (directory / "public.dat").exists() or not (directory / "codebook").exists():
        return {"status": "Author archive not present; comparison skipped, course analysis unaffected."}
    entries = []
    for line in (directory / "codebook").read_text(encoding="latin-1").splitlines():
        match = re.match(r"^([A-Z][A-Z0-9_]*)\s+(\d+)\s+(\d+)\s+\d+\.\d+\s+(.+)$", line)
        if match:
            name, start, end, _ = match.groups()
            entries.append((name.lower(), int(start) - 1, int(end)))
    author = pd.read_fwf(directory / "public.dat", colspecs=[(s, e) for n, s, e in entries],
                         names=[n for n, s, e in entries], header=None, na_values=["."])
    same_columns = list(author.columns) == list(raw.columns)
    same_missing = same_columns and raw.isna().equals(author.isna())
    same_values = same_columns and raw.shape == author.shape and bool(np.allclose(
        raw.to_numpy(), author.to_numpy(), rtol=0, atol=0, equal_nan=True))
    return {"same_column_order": same_columns, "same_missing_pattern": same_missing,
            "same_numeric_values_exactly": same_values, "raw_rows": len(raw), "raw_columns": len(raw.columns)}


def main():
    parser = argparse.ArgumentParser(description="Reproduce Table 2 from the course CSV")
    parser.add_argument("--data", type=Path, default=INPUT, help="Path to public.csv")
    args = parser.parse_args()
    input_path = args.data.expanduser().resolve()
    raw, data = load_course(input_path)
    results = ROOT / 'outputs' / 'tables'
    results.mkdir(parents=True, exist_ok=True)
    processed = ROOT / "data/processed"
    processed.mkdir(parents=True, exist_ok=True)
    (ROOT / "docs").mkdir(exist_ok=True)
    data.to_csv(processed / "course_analysis.csv", index=False)
    # Record a portable project path when possible. External inputs retain their filename;
    # the runtime command printed below identifies the actual file used locally.
    input_label = input_path.relative_to(ROOT).as_posix() if input_path.is_relative_to(ROOT) else input_path.name
    print(f"Input CSV: {input_path}")
    provenance = {"input": input_label, "source": "Course Package 01 supplied by student",
                  "checked_at_utc": datetime.now(timezone.utc).isoformat(),
                  "sha256": hashlib.sha256(input_path.read_bytes()).hexdigest(),
                  "author_archive_comparison": compare_author(raw),
                  "state_counts": {"NJ": int(raw.state.eq(1).sum()), "PA": int(raw.state.eq(0).sum())},
                  "status_counts": {str(k): int(v) for k, v in raw.status2.value_counts().sort_index().items()},
                  "duplicate_sheet_records": raw.loc[raw.sheet.duplicated(keep=False), ["sheet", "state", "chain"]].to_dict("records")}
    (ROOT / "docs/course_data_validation.json").write_text(json.dumps(provenance, indent=2), encoding="utf-8")
    rows = []
    def add(key, label, series, published_nj, published_pa, published_t, digits):
        nj = series.loc[data.state.eq(1)].dropna()
        pa = series.loc[data.state.eq(0)].dropna()
        nj_se, pa_se = nj.std(ddof=1)/np.sqrt(len(nj)), pa.std(ddof=1)/np.sqrt(len(pa))
        denominator = np.sqrt(nj_se**2 + pa_se**2)
        t = (nj.mean()-pa.mean())/denominator if denominator > 0 else np.nan
        rows.append(dict(row=key, variable=label, nj_mean=nj.mean(), nj_se=nj_se, nj_n=len(nj),
                         pa_mean=pa.mean(), pa_se=pa_se, pa_n=len(pa), t_unpooled=t,
                         paper_nj=published_nj, paper_pa=published_pa, paper_t=published_t,
                         digits=digits))
    for chain, key, label, nj, pa, t in [
        (1, "1a", "Burger King (%)", 41.1, 44.3, -.5),
        (2, "1b", "KFC (%)", 20.5, 15.2, 1.2),
        (3, "1c", "Roy Rogers (%)", 24.8, 21.5, .6),
        (4, "1d", "Wendy's (%)", 13.6, 19.0, -1.1)]:
        add(key, label, 100*data.chain.eq(chain).astype(float), nj, pa, t, 1)
    add("1e", "Company-owned (%)", 100*data.co_owned, 34.1, 35.4, -.2, 1)
    add("2a", "Before: FTE employment", data.fte, 20.4, 23.3, -2.0, 1)
    add("2b", "Before: full-time employees (% of FTE)", data.fracft, 32.8, 35.0, -.7, 1)
    add("2c", "Before: starting wage ($/hour)", data.wage_st, 4.61, 4.63, -.4, 2)
    # Reproduce the author's SAS indicator convention: missing wage produces
    # false, hence denominator is all surveyed stores. Also export the valid-only
    # alternative explicitly; never silently treat unknown wages as observed wages.
    add("2d", "Before: reported wage = $4.25 (%)", 100*data.wage_st.eq(4.25).astype(float), 30.5, 32.9, -.4, 1)
    add("2e", "Before: full meal price ($)", data.meal_price, 3.35, 3.04, 4.0, 2)
    add("2f", "Before: hours open", data.hrsopen, 14.4, 14.5, -.3, 1)
    add("2g", "Before: recruiting bonus (%)", 100*data.bonus, 23.6, 29.1, -1.0, 1)
    add("3a", "After: FTE employment", data.fte2, 21.0, 21.2, -.2, 1)
    add("3b", "After: full-time employees (% of FTE)", data.fracft2, 35.9, 30.4, 1.8, 1)
    add("3c", "After: starting wage ($/hour)", data.wage_st2, 5.08, 4.62, 10.8, 2)
    add("3d", "After: reported wage = $4.25 (%)", 100*data.wage_st2.eq(4.25).astype(float), 0.0, 25.3, np.nan, 1)
    add("3e", "After: reported wage = $5.05 (%)", 100*data.wage_st2.eq(5.05).astype(float), 85.2, 1.3, 36.1, 1)
    add("3f", "After: full meal price ($)", data.meal_price2, 3.41, 3.03, 5.0, 2)
    add("3g", "After: hours open", data.hrsopen2, 14.4, 14.7, -.8, 1)
    add("3h", "After: recruiting bonus (%)", 100*data.special2, 20.3, 23.4, -.6, 1)
    table = pd.DataFrame(rows)
    table.to_csv(results / "table2_numeric.csv", index=False)
    differences = []
    lines = ["# Table 2 — replication and comparison", "", f"Input: unmodified course `{input_label}`.", "",
             "NJ and PA entries show mean (standard error). N is available in the numeric output. Published values were transcribed from Table 2, printed page 776.", "",
             "| Row | Variable | Replicated NJ (SE) | Replicated PA (SE) | t | Paper NJ / PA / t |",
             "|---|---|---:|---:|---:|---:|"]
    for row in rows:
        digits = row['digits']
        se_digits = 2 if row['row'] in ['2a', '3a'] or digits == 2 else 1
        nj = f"{row['nj_mean']:.{digits}f} ({row['nj_se']:.{se_digits}f})"
        pa = f"{row['pa_mean']:.{digits}f} ({row['pa_se']:.{se_digits}f})"
        t = "—" if row['row'] == '3d' else f"{row['t_unpooled']:.1f}"
        paper_t = "—" if pd.isna(row['paper_t']) else f"{row['paper_t']:.1f}"
        lines.append(f"| {row['row']} | {row['variable']} | {nj} | {pa} | {t} | {row['paper_nj']:.{digits}f} / {row['paper_pa']:.{digits}f} / {paper_t} |")
        for state in ['nj', 'pa']:
            if abs(round(row[state+'_mean'], digits)-row['paper_'+state]) > 1e-8:
                differences.append(f"- {row['row']} {state.upper()} mean: {row[state+'_mean']:.{digits}f}, paper {row['paper_'+state]:.{digits}f}.")
        if not pd.isna(row['paper_t']) and abs(round(row['t_unpooled'],1)-row['paper_t']) > 1e-8:
            differences.append(f"- {row['row']} t: {row['t_unpooled']:.1f}, paper {row['paper_t']:.1f}.")
    lines += ["", "## Definitions and sample choices", "",
              "- FTE = full-time employees + managers + 0.5 × part-time employees. Missing components stay missing.",
              "- Permanent closures have zero follow-up FTE; temporary closures / renovations have missing follow-up FTE.",
              "- Full-time percentage follows author check.sas: 100 × EMPFT / FTE, excluding zero/missing FTE. This is not the full-time share of raw headcount.",
              "- Meal price = soda + fries + entree; a missing component produces a missing total.",
              "- Means otherwise use the available observations separately for each variable, not one globally complete-case sample.",
              "- Wage-equality indicators follow check.sas: proportion of all surveyed stores reporting the target wage. Missing wages contribute zero to this indicator only. The valid-wage denominator alternative is exported separately.",
              "- SE = sample SD / sqrt(N). t uses sqrt(SE_NJ² + SE_PA²); no equal-variance assumption. Row 3d t is omitted in the display as in the paper; the computed t remains in the numeric output.",
              "", "## Differences at the paper's displayed precision", ""]
    lines += differences or ["All displayed means and t statistics match."]
    lines += ["", "The 3e NJ difference corresponds to 283/331 stores in the data (85.5%), versus approximately 282/331 in the paper (85.2%). Renovation store SHEET 65 reports WAGE_ST2 = 5.05; classifying its wage indicator as unavailable/false would remove one count. This is a possible explanation, not a verified original-paper coding rule; baseline values are preserved.",
              "", "These descriptive results alone do not establish a causal policy effect. Employment effects and the ownership extension are examined in the separate stage outputs."]
    lines += ["", "The comparison above covers means and t statistics. The complete audit including published standard errors is in table2_audit_中文.md (82 of 88 published values match at displayed precision)."]
    (results / "table2_replication.md").write_text("\n".join(lines)+"\n", encoding="utf-8")
    sensitivity = []
    for variable, target in [("wage_st",4.25),("wage_st2",4.25),("wage_st2",5.05)]:
        for state in [1,0]:
            wages=data.loc[data.state.eq(state),variable]
            sensitivity.append(dict(variable=variable,target=target,state="NJ" if state==1 else "PA",
                                    all_store_n=len(wages),valid_wage_n=wages.count(),
                                    reported_target_n=int(wages.eq(target).sum()),
                                    percent_all_stores=100*wages.eq(target).mean(),
                                    percent_valid_wages=100*wages.dropna().eq(target).mean()))
    pd.DataFrame(sensitivity).to_csv(results / "table2_wage_denominators.csv", index=False)
    print(json.dumps(provenance['author_archive_comparison']))
    print(table[['row','nj_mean','pa_mean','t_unpooled','nj_n','pa_n']].to_string(index=False))
    print('Differences at published precision:', differences)
    audit(table, data, results)


if __name__ == "__main__":
    main()
