"""Ownership heterogeneity: pre-specified interaction models and HC3 inference.

This exploratory extension tests differential responses, not the causal effect
of ownership. Store-level uncertainty cannot account for arbitrary state shocks.
"""
import argparse
import hashlib
import json
from pathlib import Path
import numpy as np
import pandas as pd
from scipy import stats, linalg
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from course_data import ROOT, INPUT, load_course
(ROOT / 'outputs' / 'figures').mkdir(parents=True, exist_ok=True)

BRANDS = ['bk', 'kfc', 'roys']
REGIONS = ['centralj', 'southj', 'pa1', 'pa2']


def regression(sample, exposure, controls):
    names = ['constant', exposure, 'co_owned', 'interaction'] + controls
    x = np.column_stack([np.ones(len(sample)), sample[exposure], sample.co_owned,
                         sample[exposure]*sample.co_owned, sample[controls].to_numpy()])
    y = sample.change_fte.to_numpy(float)
    n, k = x.shape
    if not np.isfinite(x).all() or np.linalg.matrix_rank(x) != k:
        raise ValueError('Missing values or rank deficiency in model')
    beta = np.linalg.lstsq(x, y, rcond=None)[0]
    e = y-x@beta
    bread = np.linalg.inv(x.T@x)
    h = np.sum((x@bread)*x, axis=1)
    if np.any(h >= 1-1e-10):
        raise ValueError('HC3 undefined for leverage near one')
    covariance = bread @ (x.T @ ((e/(1-h))[:, None]**2*x)) @ bread
    # QR and whitened score construction provide independent numeric checks.
    q, r = np.linalg.qr(x, mode='reduced')
    rb = linalg.solve_triangular(r, q.T@y)
    rinv = linalg.solve_triangular(r, np.eye(k))
    hq = np.sum(q*q, axis=1)
    score = q*(e/(1-hq))[:, None]
    vcq = rinv@(score.T@score)@rinv.T
    if not np.allclose(beta, rb, atol=1e-9) or not np.allclose(covariance, vcq, atol=1e-8):
        raise AssertionError('QR coefficient / HC3 covariance cross-check failed')
    if not np.allclose(x.T@e, 0, atol=1e-8):
        raise AssertionError('Residual orthogonality failed')
    rows = []
    # Linear contrasts use covariance, not the sum of individual SEs.
    contrasts = {
        'franchise_effect': np.array([0, 1, 0, 0]+[0]*len(controls)),
        'company_effect': np.array([0, 1, 0, 1]+[0]*len(controls)),
        'company_minus_franchise': np.array([0, 0, 0, 1]+[0]*len(controls)),
    }
    for label, c in contrasts.items():
        estimate = float(c@beta)
        se = float(np.sqrt(c@covariance@c))
        critical = float(stats.t.ppf(.975, n-k))
        rows.append(dict(contrast=label, n=n, estimate=estimate, se_hc3=se,
                         ci95_low=estimate-critical*se, ci95_high=estimate+critical*se,
                         p=float(2*stats.t.sf(abs(estimate/se), n-k)),
                         exposure=exposure, max_leverage=float(h.max())))
    coefficients = pd.DataFrame({'variable': names, 'estimate': beta,
                                  'se_hc3': np.sqrt(np.diag(covariance))})
    return rows, coefficients


def main():
    parser = argparse.ArgumentParser(description='Ownership heterogeneity extension')
    parser.add_argument('--data', type=Path, default=INPUT)
    path = parser.parse_args().data.expanduser().resolve()
    _, data = load_course(path)
    data['nj'] = data.state
    data['gap'] = 0.0
    nj = data.nj.eq(1)
    data.loc[nj, 'gap'] = ((5.05-data.loc[nj, 'wage_st'])/data.loc[nj, 'wage_st']).clip(lower=0)
    for code, name in [(1, 'bk'), (2, 'kfc'), (3, 'roys')]:
        data[name] = data.chain.eq(code).astype(int)
    paired = data.change_fte.notna()
    common = paired & (data.status2.eq(3) | (data.wage_st.notna() & data.wage_st2.notna()))
    primary = data.loc[common].copy()
    sensitivity = data.loc[paired].copy()
    if len(primary) != 357 or len(sensitivity) != 384:
        raise AssertionError('Sample definitions differ from validated Tables 3/4')
    # Model plan fixed before viewing results; all models exported.
    specs = [('NJ_unadjusted', primary, 'nj', []),
             ('NJ_brands_primary', primary, 'nj', BRANDS),
             ('GAP_brands_support', primary, 'gap', BRANDS),
             ('GAP_brands_regions', primary, 'gap', BRANDS+REGIONS),
             ('NJ_brands_384_sensitivity', sensitivity, 'nj', BRANDS)]
    estimates, full = [], []
    for model, sample, exposure, controls in specs:
        rows, coef = regression(sample, exposure, controls)
        for row in rows:
            row['model'] = model
            estimates.append(row)
        coef.insert(0, 'model', model)
        full.append(coef)
    estimates = pd.DataFrame(estimates)
    group_rows = []
    for (state, ownership), group in primary.groupby(['state', 'co_owned']):
        group_rows.append(dict(state='NJ' if state else 'PA', co_owned=int(ownership),
                               ownership='Company-owned' if ownership else 'Franchise/non-company',
                               n=len(group), before_fte=float(group.fte.mean()),
                               after_fte=float(group.fte2.mean()),
                               mean_change=float(group.change_fte.mean()),
                               change_se=float(group.change_fte.sem())))
    groups = pd.DataFrame(group_rows)
    raw_dids = {}
    for ownership, label in [(0, 'franchise_effect'), (1, 'company_effect')]:
        g=primary.loc[primary.co_owned.eq(ownership)]
        means=g.groupby('state').change_fte.mean()
        raw_dids[label] = float(means.loc[1]-means.loc[0])
    raw_dids['company_minus_franchise'] = raw_dids['company_effect']-raw_dids['franchise_effect']
    for label, value in raw_dids.items():
        observed = estimates.loc[(estimates.model=='NJ_unadjusted') & (estimates.contrast==label), 'estimate'].iloc[0]
        if not np.isclose(value, observed, atol=1e-9):
            raise AssertionError('Group DID versus saturated regression check failed')
    # Balanced long-panel triple interaction confirms ownership difference.
    n=len(primary)
    state=primary.nj.to_numpy(); owner=primary.co_owned.to_numpy()
    post=np.r_[np.zeros(n),np.ones(n)]
    nj_long=np.tile(state,2); owner_long=np.tile(owner,2)
    xlong=np.column_stack([np.ones(2*n), nj_long, owner_long, nj_long*owner_long,
                           post,post*nj_long,post*owner_long,post*nj_long*owner_long])
    ylong=np.r_[primary.fte.to_numpy(),primary.fte2.to_numpy()]
    blong=np.linalg.lstsq(xlong,ylong,rcond=None)[0]
    if not np.isclose(blong[-1],raw_dids['company_minus_franchise'],atol=1e-9):
        raise AssertionError('Long-panel triple-interaction check failed')
    out=ROOT / 'outputs' / 'tables'; out.mkdir(parents=True, exist_ok=True)
    estimates.to_csv(out/'extension_ownership_effects.csv',index=False)
    groups.to_csv(out/'extension_ownership_groups.csv',index=False)
    pd.concat(full).to_csv(out/'extension_ownership_coefficients.csv',index=False)
    pd.crosstab([primary.state,primary.co_owned],primary.chain).to_csv(out/'extension_ownership_brand_counts.csv')
    data['extension_primary']=common
    data['extension_employment_sample']=paired
    processed=ROOT/'data'/'processed'; processed.mkdir(parents=True,exist_ok=True)
    data.to_csv(processed/'extension_ownership_analysis.csv',index=False)
    fig,ax=plt.subplots(figsize=(8,5.2))
    for state,color,offset in [('PA','#888888',-.16),('NJ','#2266aa',.16)]:
        g=groups.loc[groups.state.eq(state)].sort_values('co_owned')
        ax.bar(np.arange(2)+offset,g.mean_change,width=.3,label=state,color=color)
    ax.axhline(0,color='black',linewidth=.8)
    ax.set_xticks([0,1],['Franchise / non-company','Company-owned'])
    ax.set_ylabel('Mean change in FTE employment')
    ax.set_title('Employment changes by state and ownership\nCommon Table 4 sample (N = 357)')
    ax.legend(); ax.spines[['top','right']].set_visible(False)
    fig.tight_layout(); fig.savefig(ROOT / 'outputs' / 'figures' / 'extension_ownership_changes.png',dpi=180)
    fig.savefig(ROOT / 'outputs' / 'figures' / 'extension_ownership_changes.svg'); plt.close(fig)
    primary_results=estimates.loc[estimates.model.eq('NJ_brands_primary')].set_index('contrast')
    fig,ax=plt.subplots(figsize=(8,4.8))
    labels=['Franchise effect','Company-owned effect','Company minus franchise']
    order=['franchise_effect','company_effect','company_minus_franchise']
    for y,label in enumerate(order):
        row=primary_results.loc[label]
        ax.errorbar(row.estimate,y,xerr=[[row.estimate-row.ci95_low],[row.ci95_high-row.estimate]],fmt='o',color='#2266aa',capsize=4)
    ax.set_yticks(range(3),labels); ax.invert_yaxis(); ax.axvline(0,color='black',linestyle='--')
    ax.set_xlabel('FTE estimate and 95% HC3 interval')
    ax.set_title('Ownership heterogeneity: NJ interaction model\nBrand controls; N = 357')
    ax.spines[['top','right']].set_visible(False); fig.tight_layout()
    fig.savefig(ROOT / 'outputs' / 'figures' / 'extension_ownership_effects.png',dpi=180)
    fig.savefig(ROOT / 'outputs' / 'figures' / 'extension_ownership_effects.svg'); plt.close(fig)
    checks=dict(input_csv=path.name,input_sha256=hashlib.sha256(path.read_bytes()).hexdigest(),
                primary_n=357,sensitivity_n=384,models=[m[0] for m in specs],
                inference='Store-level HC3 with t(N-k) approximate intervals; not state-cluster inference.',
                checks_passed=['common_samples','QR_coefficients_HC3','OLS_orthogonality',
                               'group_DID_saturated_regression','long_panel_triple_interaction'],
                primary_model='NJ_brands_primary',
                hypothesis='NJ x company ownership interaction = 0; two-sided test.',
                originality_scope='Ownership interaction extension of this paper; no claim of novelty in all literature.')
    (out/'extension_ownership_validation.json').write_text(json.dumps(checks,ensure_ascii=False,indent=2),encoding='utf-8')
    from english_reports import write_report
    write_report('extension_ownership_report.md', 'ownership_notes.md', [('State and ownership groups', pd.DataFrame(group_rows)), ('All effects and interactions', estimates)], ['extension_ownership_changes.png', 'extension_ownership_effects.png'])
    print(estimates.loc[estimates.contrast.eq('company_minus_franchise'),['model','n','estimate','se_hc3','ci95_low','ci95_high','p']].to_string(index=False))
    print('Primary contrast: company-owned effect minus franchise effect.')
    print('All computation checks passed. Outputs saved in outputs/tables/ and outputs/figures/.')


if __name__=='__main__':
    main()
