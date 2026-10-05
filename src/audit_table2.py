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
    lines=['# Table 2 逐项核对记录（当前数据版本）','',
           '核对范围：原文第 776 页的均值、已发表标准误和已发表 t 统计量。原文没有打印的标准误或 t 不按零处理。', '',
           f'共核对 {len(check)} 个已发表数值，其中 {int(check.matches.sum())} 个在原文显示精度下一致，{len(differences)} 个不同。', '',
           '| 行 | 指标 | 本次计算（显示值） | 原文 |','|---|---|---:|---:|']
    for r in differences.to_dict('records'):
        d=int(r['digits'])
        lines.append(f"| {r['row']} | {r['metric']} | {r['calculated_display']:.{d}f} | {r['published']:.{d}f} |")
    lines += ['', '## 能够确认的事实', '',
              '- 40 个州均值中 39 个一致；29 个已发表标准误中 28 个一致；19 个已发表 t 中 15 个一致。',
              '- 政策前各行的已发表均值、标准误和 t 均匹配；差异集中在政策后。',
              '- 老师 CSV 与作者公开数据的 410 × 46 个原始数值、缺失位置已逐项验证一致，不能把当前差异解释为 CSV 转换错误。',
              '- baseline 使用完整精度计算，再做四舍五入。不能仅以“四舍五入”笼统解释不匹配。', '',
              '## 3e：一个记录可能解释均值和标准误差异', '']
    if scenario is not None:
        lines += [f"NJ 的装修餐厅 SHEET=65 报告起薪 5.05。仅在诊断情景中把这家店的目标工资指示变量改为 0、仍以 331 家店为分母，会得到：均值 {scenario['nj_mean']:.1f}%，标准误 {scenario['nj_se']:.1f}，t={scenario['t']:.1f}。均值和标准误匹配原文，但 t 仍未匹配原文的 36.1。", '',
                  '这说明一条记录的处理可以解释该行的两项差异，但尚无原始程序或版本记录证明论文确实采用此处理。不能据此更改基准代码；当前 85.5% 的基准结果保留。']
    lines += ['', '## t 统计量的口径检查', '',
              '另计算等方差合并 t 和总体方差（ddof=0）口径。完整数值见 table2_t_method_checks.csv。', '',
              '| 行 | 原文 t | 基准 Welch | 合并方差 | ddof=0 |',
              '|---|---:|---:|---:|---:|']
    for r in variants.to_dict('records'):
        lines.append(f"| {r['row']} | {r['published_t']:.1f} | {r['baseline_welch_t']:.3f} | {r['pooled_t']:.3f} | {r['population_variance_t']:.3f} |")
    lines += ['', '3a、3f、3g 的原文 t 与当前数据的计算差异仍未得到有来源支持的解释。可能涉及原文底层数据版本、样本或计算细节，但这些只是待核实的可能性。没有证据支持逐行挑选最接近原文的算法。', '',
              '## 本阶段状态', '',
              'Table 2 的计算流程、已发表数值的逐项核对和差异记录已完成；当前公开数据不能完全匹配原文。保留基准、展示差异后，可以继续 Figure 1 和 Tables 3–4。后续若找到新证据再修订解释。', '',
              '原文第 1 组未打印标准误，本次表格额外提供；3d NJ 标准误原文省略，本次计算为 0。这些是展示差异，不计入上述数值不匹配。']
    (results/'table2_audit_中文.md').write_text('\n'.join(lines)+'\n',encoding='utf-8')
    print(f"Table 2 audit: {int(check.matches.sum())}/{len(check)} published numeric cells match; {len(differences)} differences retained.")
