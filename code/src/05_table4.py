"""Table 4 OLS, common sample, published audit and author-code sensitivity."""
import argparse
import hashlib
import json
from pathlib import Path
import numpy as np
import pandas as pd
from scipy import stats, linalg
from course_data import ROOT, INPUT, load_course

CHAIN = ['bk', 'kfc', 'roys', 'co_owned']
REGION = ['centralj', 'southj', 'pa1', 'pa2']
SPECS = [('i', 'nj', []), ('ii', 'nj', CHAIN), ('iii', 'gap', []),
         ('iv', 'gap', CHAIN), ('v', 'gap', CHAIN + REGION)]
# Printed page 780; benchmark numbers do not enter estimation.
PAPER = {'estimate': [2.33, 2.30, 15.65, 14.92, 11.91],
         'se': [1.19, 1.20, 6.08, 6.21, 7.39],
         'regression_se': [8.79, 8.78, 8.76, 8.76, 8.75],
         'controls_p': [np.nan, .34, np.nan, .44, .40]}


def fit(sample, main, controls):
    names = ['constant', main] + controls
    x = np.column_stack([np.ones(len(sample)), sample[[main] + controls].to_numpy(float)])
    y = sample.change_fte.to_numpy(float)
    n, k = x.shape
    if not np.isfinite(x).all() or np.linalg.matrix_rank(x) != k:
        raise ValueError('Missing or collinear regressors')
    beta = np.linalg.lstsq(x, y, rcond=None)[0]
    residual = y - x @ beta
    rss = float(residual @ residual)
    mse = rss / (n-k)
    bread = np.linalg.inv(x.T @ x)
    se = np.sqrt(np.diag(mse * bread))
    # Independent QR coefficient and covariance check, not published-value check.
    q, r = np.linalg.qr(x, mode='reduced')
    qr_beta = linalg.solve_triangular(r, q.T @ y)
    r_inverse = linalg.solve_triangular(r, np.eye(k))
    qr_se = np.sqrt(np.diag(mse * r_inverse @ r_inverse.T))
    if not np.allclose(beta, qr_beta, atol=1e-9) or not np.allclose(se, qr_se, atol=1e-9):
        raise AssertionError('Independent QR verification failed')
    if not np.allclose(x.T @ residual, 0, atol=1e-8):
        raise AssertionError('OLS residual orthogonality failed')
    p_controls = np.nan
    if controls:
        restricted = np.column_stack([np.ones(n), sample[main].to_numpy()])
        b0 = np.linalg.lstsq(restricted, y, rcond=None)[0]
        rss0 = float(np.sum((y-restricted @ b0)**2))
        f_stat = ((rss0-rss)/len(controls))/mse
        p_controls = float(stats.f.sf(f_stat, len(controls), n-k))
        # Equivalent Wald test of all controls jointly equal to zero.
        bc = beta[2:]
        vc = (mse*bread)[2:, 2:]
        wald_f = float(bc @ np.linalg.solve(vc, bc))/len(controls)
        if not np.isclose(f_stat, wald_f, atol=1e-9):
            raise AssertionError('Joint F/Wald cross-check failed')
    t = float(beta[1]/se[1])
    main_result = dict(estimate=float(beta[1]), se=float(se[1]),
                       regression_se=float(np.sqrt(mse)), controls_p=p_controls,
                       n=n, residual_df=n-k, t=t,
                       coefficient_p=float(2*stats.t.sf(abs(t), n-k)),
                       ci95_low=float(beta[1]-stats.t.ppf(.975, n-k)*se[1]),
                       ci95_high=float(beta[1]+stats.t.ppf(.975, n-k)*se[1]))
    full = pd.DataFrame({'variable': names, 'estimate': beta, 'se': se})
    return main_result, full


def main():
    parser = argparse.ArgumentParser(description='Reproduce Table 4 with documented samples')
    parser.add_argument('--data', type=Path, default=INPUT)
    path = parser.parse_args().data.expanduser().resolve()
    _, data = load_course(path)
    data['nj'] = data.state
    data['gap'] = 0.0
    nj = data.nj.eq(1)
    data.loc[nj, 'gap'] = ((5.05-data.loc[nj, 'wage_st'])/data.loc[nj, 'wage_st']).clip(lower=0)
    for code, name in [(1, 'bk'), (2, 'kfc'), (3, 'roys')]:
        data[name] = data.chain.eq(code).astype(int)
    employment = data.change_fte.notna()
    wages = data.wage_st.notna() & data.wage_st2.notna()
    closed = data.status2.eq(3)
    selected = employment & (wages | closed)
    sample = data.loc[selected].copy()
    if len(sample) != 357 or sample.gap.isna().any():
        raise AssertionError('Common Table 4 sample is not the expected 357 stores')
    if not sample[REGION+CHAIN].notna().all().all():
        raise AssertionError('Missing controls in common sample')
    if not data[['northj', 'centralj', 'southj', 'pa1', 'pa2']].sum(axis=1).eq(1).all():
        raise AssertionError('Region dummy classification failed')
    data['table4_included'] = selected
    data['table4_exclusion'] = np.select([~employment, employment & ~(wages | closed)],
                                        ['employment_missing', 'wage_missing'], default='included')
    results, full, audit = [], [], []
    for index, (model, variable, controls) in enumerate(SPECS):
        result, coefficients = fit(sample, variable, controls)
        result.update(model=model, variable=variable)
        results.append(result)
        coefficients.insert(0, 'model', model)
        full.append(coefficients)
        for metric in PAPER:
            target = PAPER[metric][index]
            if np.isfinite(target):
                value = result[metric]
                audit.append(dict(model=model, metric=metric, replicated=value, published=target,
                                  match_at_precision=f'{value:.2f}' == f'{target:.2f}'))
    result_frame = pd.DataFrame(results)
    audit_frame = pd.DataFrame(audit)
    # Author's check.sas omits ownership from the fifth employment model.
    alternative, _ = fit(sample, 'gap', ['bk', 'kfc', 'roys']+REGION)
    alternative['model'] = 'v_author_sas_without_ownership'
    # NJ-only OLS must equal difference in mean paired employment changes.
    contrast = sample.groupby('nj').change_fte.mean().diff().iloc[-1]
    if not np.isclose(contrast, results[0]['estimate'], atol=1e-10):
        raise AssertionError('NJ difference-of-means check failed')
    checks = dict(input_csv=path.name, input_sha256=hashlib.sha256(path.read_bytes()).hexdigest(),
                  sample_n=len(sample), nj_n=int(sample.nj.sum()), pa_n=int(sample.nj.eq(0).sum()),
                  paired_employment_n=int(employment.sum()),
                  excluded_wage_n=int((employment & ~selected).sum()),
                  closed_retained_n=int((selected & closed).sum()),
                  outcome_mean=float(sample.change_fte.mean()), outcome_sd=float(sample.change_fte.std()),
                  published_matches=int(audit_frame.match_at_precision.sum()),
                  published_numeric_cells=len(audit_frame),
                  checks_passed=['common_sample', 'region_classification', 'QR_OLS_and_SE',
                                 'residual_orthogonality', 'joint_F_Wald', 'NJ_mean_contrast'],
                  fifth_model_rule='Paper table note: include ownership. Author SAS comparison exported separately.')
    output = ROOT / 'outputs' / 'tables'
    output.mkdir(parents=True, exist_ok=True)
    processed = ROOT/'data'/'processed'
    processed.mkdir(parents=True, exist_ok=True)
    data.to_csv(processed/'table4_analysis.csv', index=False)
    result_frame.to_csv(output/'table4_numeric.csv', index=False)
    pd.concat(full).to_csv(output/'table4_all_coefficients.csv', index=False)
    audit_frame.to_csv(output/'table4_audit_cells.csv', index=False)
    pd.DataFrame([alternative]).to_csv(output/'table4_author_sas_comparison.csv', index=False)
    data.groupby(['state', 'table4_exclusion']).size().rename('n').reset_index().to_csv(output/'table4_sample_flow.csv', index=False)
    (output/'table4_validation.json').write_text(json.dumps(checks, ensure_ascii=False, indent=2), encoding='utf-8')
    from english_reports import write_report
    write_report('table4_replication.md', 'table4_notes.md', [('Regression results', result_frame), ('Published-cell audit', audit_frame), ('Author-SAS fifth model', pd.DataFrame([alternative]))])
    print(result_frame[['model', 'variable', 'n', 'estimate', 'se', 'regression_se', 'controls_p']].to_string(index=False))
    print(json.dumps(checks, ensure_ascii=False, indent=2))
    print('Table 4 saved in outputs/tables/ and outputs/figures/. Author-SAS fifth model exported separately.')


if __name__ == '__main__':
    main()
