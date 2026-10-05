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
    out=ROOT/'results'; out.mkdir(exist_ok=True)
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
    fig.tight_layout(); fig.savefig(out/'extension_ownership_changes.png',dpi=180)
    fig.savefig(out/'extension_ownership_changes.svg'); plt.close(fig)
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
    fig.savefig(out/'extension_ownership_effects.png',dpi=180)
    fig.savefig(out/'extension_ownership_effects.svg'); plt.close(fig)
    checks=dict(input_csv=str(path),input_sha256=hashlib.sha256(path.read_bytes()).hexdigest(),
                primary_n=357,sensitivity_n=384,models=[m[0] for m in specs],
                inference='Store-level HC3 with t(N-k) approximate intervals; not state-cluster inference.',
                checks_passed=['common_samples','QR_coefficients_HC3','OLS_orthogonality',
                               'group_DID_saturated_regression','long_panel_triple_interaction'],
                primary_model='NJ_brands_primary',
                hypothesis='NJ x company ownership interaction = 0; two-sided test.',
                originality_scope='Ownership interaction extension of this paper; no claim of novelty in all literature.')
    (out/'extension_ownership_validation.json').write_text(json.dumps(checks,ensure_ascii=False,indent=2),encoding='utf-8')
    lines=['# 独立拓展：直营店与非直营店的就业反应', '',
           '研究问题：最低工资提高后的就业变化，在公司直营店和非直营店（本文简称加盟店）之间是否不同？',
           '数据严格定义是CO_OWNED=1与0；它没有进一步区分加盟合同形式，也没有两期所有权变化记录。', '',
           '## 经济动机与事先设定', '',
           '两类餐厅可能在资金条件、决策权限和成本承担方式上不同，因此就业调整可能不同。这些是待讨论的可能机制，当前数据不能直接验证。',
           '原论文在就业回归中控制所有权；本拓展直接检验政策暴露与所有权的交互项。没有把原文控制变量系数当作异质性检验。',
           '主分析固定为357家共同样本、NJ交互模型、品牌控制。GAP、地区控制和384家样本均为补充，所有设定完整报告，不按显著性挑选。', '',
           '## 样本和描述统计', '',
           '| 州 | 所有权 | N | 政策前FTE | 政策后FTE | 同店平均变化 |',
           '|---|---|---:|---:|---:|---:|']
    for row in group_rows:
        owner='直营店' if row['co_owned'] else '非直营/加盟店'
        lines.append(f"| {row['state']} | {owner} | {row['n']} | {row['before_fte']:.2f} | {row['after_fte']:.2f} | {row['mean_change']:.2f} |")
    lines += ['', '![分组变化](extension_ownership_changes.png)', '', '## 回归设定', '',
              'ΔFTE = α + β NJ + γ OWN + δ(NJ×OWN) + 品牌控制 + ε。',
              'OWN=1表示直营店。加盟店政策对照系数是β，直营店是β+δ，两类店差异是δ。γ是PA中两类店就业变化的差异，不是最低工资差异效应。',
              'GAP补充模型把NJ替换成GAP；两类店差异的单位是每一单位GAP，不能直接与NJ系数比较。对起薪4.25的NJ店，乘0.188235才能得到相应FTE差异。',
              '品牌控制以Wendy\'s为基准。GAP地区模型以North NJ为基准。NJ模型不同时加入全部地区虚拟变量，以免共线。', '',
              '## 主结果：品牌控制NJ模型', '',
              '| 比较 | 系数 | HC3标准误 | 95%区间 | p值 |',
              '|---|---:|---:|---|---:|']
    for label,chinese in [('franchise_effect','加盟店：NJ−PA'),('company_effect','直营店：NJ−PA'),('company_minus_franchise','直营店效果−加盟店效果')]:
        row=primary_results.loc[label]
        lines.append(f"| {chinese} | {row.estimate:.3f} | {row.se_hc3:.3f} | [{row.ci95_low:.3f}, {row.ci95_high:.3f}] | {row.p:.3f} |")
    diff=primary_results.loc['company_minus_franchise']
    conclusion=('差异在本模型的5%近似检验下显著，但不能据此证明所有权本身造成差异。' if diff.p<.05
                else '差异在本模型的5%近似检验下不显著。当前样本没有提供足够证据确认两类店反应不同；这不等于证明两类店效果相同。')
    lines += ['',conclusion,'', '![效果及区间](extension_ownership_effects.png)', '',
              '## 所有设定的交互项', '',
              '| 设定 | N | 差异系数 | HC3标准误 | p值 |',
              '|---|---:|---:|---:|---:|']
    for row in estimates.loc[estimates.contrast.eq('company_minus_franchise')].itertuples():
        lines.append(f'| {row.model} | {row.n} | {row.estimate:.3f} | {row.se_hc3:.3f} | {row.p:.3f} |')
    lines += ['', '## 推断与局限', '',
              '- 拓展使用店级HC3异方差稳健标准误，区间和p值使用t(N−k)近似。Table 4复现仍使用传统OLS标准误，两者目的和口径分别标明。',
              '- 只有两个州，店级HC3不能处理任意的州内共同冲击；这些p值和区间是条件性的探索结果，不是稳健的州级政策显著性证明。',
              '- 交互项直接检验差异，不能用“一组显著、另一组不显著”替代它。',
              '- 所有权不是随机分配，品牌控制也不能排除全部经营条件差异。只有一期政策前数据，不能直接检验所有权分组的平行趋势。',
              '- 不检验政策后变量作为控制，不按结果删极端值，不做以显著性为目标的模型筛选。',
              '- 保留六家永久关店、后期FTE为0；暂时关店在基准中为缺失。357家样本要求两轮工资有效（永久关店例外）；384家补充只要求就业变化有效。',
              '- 公开输出含分组汇总和回归结果；逐店分析文件被Git忽略，不能公开课程数据。', '',
              '## 验证', '',
              'QR分解核对系数和HC3协方差；无控制的回归与分组DID一致；两期堆叠模型三重交互系数与所有权DID之差一致。计算验证不证明因果假设成立。']
    (out/'extension_ownership_report.md').write_text('\n'.join(lines)+'\n',encoding='utf-8')
    print(estimates.loc[estimates.contrast.eq('company_minus_franchise'),['model','n','estimate','se_hc3','ci95_low','ci95_high','p']].to_string(index=False))
    print('Primary contrast: company-owned effect minus franchise effect.')
    print('All computation checks passed. Outputs saved in results/.')


if __name__=='__main__':
    main()
