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
    checks = dict(input_csv=str(path), input_sha256=hashlib.sha256(path.read_bytes()).hexdigest(),
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
    output = ROOT/'results'
    output.mkdir(exist_ok=True)
    processed = ROOT/'data'/'processed'
    processed.mkdir(parents=True, exist_ok=True)
    data.to_csv(processed/'table4_analysis.csv', index=False)
    result_frame.to_csv(output/'table4_numeric.csv', index=False)
    pd.concat(full).to_csv(output/'table4_all_coefficients.csv', index=False)
    audit_frame.to_csv(output/'table4_audit_cells.csv', index=False)
    pd.DataFrame([alternative]).to_csv(output/'table4_author_sas_comparison.csv', index=False)
    data.groupby(['state', 'table4_exclusion']).size().rename('n').reset_index().to_csv(output/'table4_sample_flow.csv', index=False)
    (output/'table4_validation.json').write_text(json.dumps(checks, ensure_ascii=False, indent=2), encoding='utf-8')
    lines = ['# Table 4：就业变化回归与原文比较', '',
             '因变量：同店政策后 FTE 减政策前 FTE。所有模型含截距，使用同一357家样本。', '',
             '| 模型 | 核心变量 | 系数（标准误） | 原文系数（标准误） | 回归标准误 | 控制变量联合检验 p |',
             '|---|---|---|---|---|---|']
    for i, row in enumerate(results):
        p = '—' if not np.isfinite(row['controls_p']) else f"{row['controls_p']:.2f}"
        lines.append(f"| {row['model']} | {row['variable'].upper()} | {row['estimate']:.2f} ({row['se']:.2f}) | {PAPER['estimate'][i]:.2f} ({PAPER['se'][i]:.2f}) | {row['regression_se']:.2f} | {p} |")
    lines += ['', '## 样本和变量', '',
              f"- 原始410家；就业变化有效{employment.sum()}家；再排除缺工资的{checks['excluded_wage_n']}家，保留357家（NJ290、PA67）。",
              f"- 永久关闭的{checks['closed_retained_n']}家保留，后期就业为0；按作者程序允许缺后期工资。暂时关闭仍为缺失。",
              '- 其他餐厅必须两轮就业和两轮起薪均有效。工资不是前两组回归的解释变量，但共同样本也应用这一筛选。',
              '- GAP：PA为0；NJ为 max((5.05 − 政策前工资)/政策前工资, 0)。例如4.25美元对应0.188235，即18.82%，不是0.80美元。',
              '- 模型(i)：NJ；(ii)：NJ加品牌和所有权；(iii)：GAP；(iv)：GAP加品牌和所有权；(v)：GAP再加地区。',
              '- 品牌以Wendy\'s为基准，加入BK、KFC、Roy Rogers三个虚拟变量；所有权为co_owned。',
              '- 地区以North NJ为基准，加入Central NJ、South NJ、PA1、PA2；第五组不另加NJ，否则与地区虚拟变量共线。',
              '- 复现使用传统OLS标准误：残差平方和/(N−参数数)乘(X\'X)逆矩阵。不是州聚类或异方差稳健标准误。',
              '- 回归标准误是残差标准差，不是核心系数的标准误。控制变量p值检验所有额外控制变量共同为0，不是政策系数p值。',
              f"- 因变量均值{checks['outcome_mean']:.6f}、样本标准差{checks['outcome_sd']:.6f}；原文为−0.237和8.825，均值按通常三位四舍五入为−0.238，原文显示有末位差异。", '',
              '## 核对和第五组差异', '',
              f"原表18个回归数值中，{checks['published_matches']}个按两位小数匹配。样本数与因变量描述统计另列，不纳入这18格。",
              '前四组所有已发表回归数值匹配。第五组按表注含所有权得到11.98 (7.42)，而原文11.91 (7.39)。',
              f"作者check.sas的第五个就业设定没有co_owned，按该程序得到{alternative['estimate']:.2f} ({alternative['se']:.2f})，回归标准误{alternative['regression_se']:.2f}、联合控制p={alternative['controls_p']:.2f}。",
              '该对照解释了核心系数与标准误差异，但未复现原文第五组回归标准误8.75，控制联合p值也为0.31而不是原文0.40。不能把两个设定的数值拼成一列，也不能确认原文全部差异的原因。',
              '全部不一致格见table4_audit_cells.csv；完整控制系数见table4_all_coefficients.csv；逐店筛选标记保存在被Git忽略的data/processed/table4_analysis.csv。', '',
              '## 结果怎么读', '',
              '模型(i)的NJ系数约2.33：共同样本中新泽西的同店就业变化比宾州高约2.33个FTE。它与Table 3的2.75不同，主要因为样本收窄到357家。',
              'GAP用比例而非百分点计量，模型(iii)中政策前工资4.25的NJ餐厅对应15.65×0.188235≈2.95个FTE的预测差异。',
              '品牌和所有权控制对主要系数影响较小；加入地区后GAP系数降低且标准误增大，第五组在通常5%水平下不显著。正的点估计不等于所有模型都证明就业增加。',
              '数值交叉检查通过不证明因果假设成立。单一政策前观测无法直接检验平行趋势，且这里只有两个州。']
    (output/'table4_replication.md').write_text('\n'.join(lines)+'\n', encoding='utf-8')
    print(result_frame[['model', 'variable', 'n', 'estimate', 'se', 'regression_se', 'controls_p']].to_string(index=False))
    print(json.dumps(checks, ensure_ascii=False, indent=2))
    print('Table 4 saved in results/. Author-SAS fifth model exported separately.')


if __name__ == '__main__':
    main()
