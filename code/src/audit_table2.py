"""Audit displayed means, SEs and t statistics against published Table 2."""
import numpy as np
import pandas as pd

# Visually transcribed from printed page 776 (PDF page 5).
# None means no SE is printed; do not interpret it as zero.
PAPER_SE = {
    "2a": (.51, 1.35, 2), "2b": (1.3, 2.7, 1),
    "2c": (.02, .04, 2), "2d": (2.5, 5.3, 1),
    "2e": (.04, .07, 2), "2f": (.2, .3, 1), "2g": (2.3, 5.1, 1),
    "3a": (.52, .94, 2), "3b": (1.4, 2.8, 1),
    "3c": (.01, .04, 2), "3d": (None, 4.9, 1),
    "3e": (2.0, 1.3, 1), "3f": (.04, .07, 2),
    "3g": (.2, .3, 1), "3h": (2.3, 4.9, 1),
}


def audit(table, data, results):
    checks = []
    def compare(row, metric, value, paper, digits):
        if paper is None or pd.isna(paper):
            return
        rounded = float(f"{value:.{digits}f}")
        checks.append(dict(row=row, metric=metric, calculated=value,
                           calculated_display=rounded, published=paper,
                           digits=digits, matches=bool(abs(rounded-paper) < 1e-9)))
    for r in table.to_dict("records"):
        for state in ["nj", "pa"]:
            compare(r['row'], state+'_mean', r[state+'_mean'], r['paper_'+state], int(r['digits']))
        compare(r['row'], 't', r['t_unpooled'], r['paper_t'], 1)
        if r['row'] in PAPER_SE:
            nj, pa, digits = PAPER_SE[r['row']]
            compare(r['row'], 'nj_se', r['nj_se'], nj, digits)
            compare(r['row'], 'pa_se', r['pa_se'], pa, digits)
    check = pd.DataFrame(checks)
    check.to_csv(results/'table2_audit_cells.csv', index=False)

    variants = []
    for r in table.loc[table.row.isin(['3a','3e','3f','3g'])].to_dict('records'):
        n, m = r['nj_n'], r['pa_n']
        v1, v2 = r['nj_se']**2*n, r['pa_se']**2*m
        gap = r['nj_mean']-r['pa_mean']
        pooled = gap / np.sqrt(((n-1)*v1+(m-1)*v2)/(n+m-2)*(1/n+1/m))
        population = gap / np.sqrt(v1*(n-1)/n/n + v2*(m-1)/m/m)
        variants.append(dict(row=r['row'], published_t=r['paper_t'],
                             baseline_welch_t=r['t_unpooled'], pooled_t=pooled,
                             population_variance_t=population))
    variants = pd.DataFrame(variants)
    variants.to_csv(results/'table2_t_method_checks.csv',index=False)

    # Diagnostic only: remove the target-wage flag for NJ renovation store 65.
    # Preserve original wages and all baseline analysis outputs.
    indicator=100*data.wage_st2.eq(5.05).astype(float)
    candidate=data.state.eq(1)&data.sheet.eq(65)&data.status2.eq(2)&data.wage_st2.eq(5.05)
    scenario = None
    if candidate.sum() == 1:
        alternative=indicator.copy()
        alternative.loc[candidate]=0
        nj=alternative.loc[data.state.eq(1)]
        pa=alternative.loc[data.state.eq(0)]
        se1,se2=nj.std(ddof=1)/np.sqrt(len(nj)),pa.std(ddof=1)/np.sqrt(len(pa))
        scenario=dict(nj_mean=nj.mean(),nj_se=se1,t=(nj.mean()-pa.mean())/np.sqrt(se1**2+se2**2))
    differences=check.loc[~check.matches]
    from english_reports import write_report
    sections = [('Unmatched published cells', differences), ('Alternative t calculations', variants)]
    if scenario is not None:
        sections.append(('Renovation-store diagnostic only; baseline unchanged', pd.DataFrame([scenario])))
    write_report('table2_audit.md', 'table2_notes.md', sections)
    print(f"Table 2 audit: {int(check.matches.sum())}/{len(check)} published numeric cells match; {len(differences)} differences retained.")
