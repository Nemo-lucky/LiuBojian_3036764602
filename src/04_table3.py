"""Table 3 replication, published-cell audit and independent regression checks.

Row 3 estimates a difference of available-case means. Its uncertainty uses a
store-level influence-function variance accounting for overlapping observations,
with G/(G-1) correction. The paper does not state its exact unbalanced-row SE
algorithm, so this defensible reconstruction is not claimed to be the original.
"""
import argparse
import hashlib
import json
from pathlib import Path
import numpy as np
import pandas as pd
from course_data import ROOT, INPUT, load_course

COLS = ['PA', 'NJ', 'NJ-PA', 'NJ_low', 'NJ_mid', 'NJ_high', 'Low-High', 'Mid-High']
ROW_LABELS = {
    1:'政策前 FTE：全部有效记录', 2:'政策后 FTE：全部有效记录',
    3:'两轮可用均值之差（非平衡样本）', 4:'同店就业变化（平衡样本）',
    5:'同店就业变化（暂时关店按零处理）',
}
# Visually transcribed from printed page 780, Table 3. Never used as estimates.
PAPER_MEAN = [
    [23.33,20.44,-2.89,19.56,20.08,22.25,-2.69,-2.17],
    [21.17,21.03,-.14,20.88,20.96,20.21,.67,.75],
    [-2.16,.59,2.76,1.32,.87,-2.04,3.36,2.91],
    [-2.28,.47,2.75,1.21,.71,-2.16,3.36,2.87],
    [-2.28,.23,2.51,.90,.49,-2.39,3.29,2.88],
]
PAPER_SE = [
    [1.35,.51,1.44,.77,.84,1.14,1.37,1.41],
    [.94,.52,1.07,1.01,.76,1.03,1.44,1.27],
    [1.25,.54,1.36,.95,.84,1.14,1.48,1.41],
    [1.25,.48,1.34,.82,.69,1.01,1.30,1.22],
    [1.25,.49,1.35,.87,.69,1.02,1.34,1.23],
]


def mean_se(series):
    values=series.dropna()
    if len(values)<2:
        raise ValueError('At least two observations are required')
    return float(values.mean()),float(values.sem())


def available_change(before, after):
    b,a=before.dropna(),after.dropna()
    union=before.notna()|after.notna()
    # Missing terms contribute nothing to the estimator's score. This does not
    # fill missing employment with zero in either the raw or processed dataset.
    score=(after-a.mean()).fillna(0)/len(a)-(before-b.mean()).fillna(0)/len(b)
    g=int(union.sum())
    se=float(np.sqrt(g/(g-1)*np.square(score.loc[union]).sum()))
    return float(a.mean()-b.mean()),se


def check_stacked_regression(group, estimate, se):
    """Independent stacked OLS with store-cluster scores and G/(G-1)."""
    frames=[]
    for period,column in [(0,'fte'),(1,'fte2')]:
        selected=group.loc[group[column].notna(),['source_row_id',column]].copy()
        selected.columns=['id','y']
        selected['after']=period
        frames.append(selected)
    long=pd.concat(frames,ignore_index=True)
    x=np.column_stack([np.ones(len(long)),long.after.to_numpy()])
    y=long.y.to_numpy()
    beta=np.linalg.lstsq(x,y,rcond=None)[0]
    residual=y-x@beta
    scores=pd.DataFrame(x*residual[:,None],columns=['intercept','after'])
    scores['id']=long.id.to_numpy()
    clusters=scores.groupby('id')[['intercept','after']].sum().to_numpy()
    bread=np.linalg.inv(x.T@x)
    g=len(clusters)
    covariance=g/(g-1)*bread@(clusters.T@clusters)@bread
    if not np.allclose([beta[1],np.sqrt(covariance[1,1])],[estimate,se],rtol=1e-9,atol=1e-9):
        raise AssertionError('Stacked-regression validation failed')


def check_balanced_regression(data, outcome, estimate, se):
    """OLS NJ coefficient and HC2 SE equal the two-sample change estimate/SE."""
    valid=outcome.notna()
    y=outcome.loc[valid].to_numpy()
    x=np.column_stack([np.ones(valid.sum()),data.loc[valid,'state'].to_numpy()])
    beta=np.linalg.lstsq(x,y,rcond=None)[0]
    bread=np.linalg.inv(x.T@x)
    residual=y-x@beta
    leverage=np.sum((x@bread)*x,axis=1)
    meat=x.T@((residual**2/(1-leverage))[:,None]*x)
    covariance=bread@meat@bread
    if not np.allclose([beta[1],np.sqrt(covariance[1,1])],[estimate,se],rtol=1e-9,atol=1e-9):
        raise AssertionError('Balanced regression validation failed')


def main():
    parser=argparse.ArgumentParser(description='Reproduce Table 3 from course CSV')
    parser.add_argument('--data',type=Path,default=INPUT)
    args=parser.parse_args()
    path=args.data.expanduser().resolve()
    raw,data=load_course(path)
    results=ROOT/'results'
    results.mkdir(parents=True,exist_ok=True)
    processed=ROOT/'data/processed'
    processed.mkdir(parents=True,exist_ok=True)
    masks={'PA':data.state.eq(0),'NJ':data.state.eq(1),
           'NJ_low':data.state.eq(1)&data.wage_st.eq(4.25),
           'NJ_mid':data.state.eq(1)&data.wage_st.gt(4.25)&data.wage_st.lt(5),
           'NJ_high':data.state.eq(1)&data.wage_st.ge(5)}
    expected={'PA':79,'NJ':331,'NJ_low':101,'NJ_mid':140,'NJ_high':73}
    for name,mask in masks.items():
        if int(mask.sum())!=expected[name]:
            raise AssertionError(f'Unexpected group size: {name}')
    temporary=data.status2.isin([2,4,5])
    if int(temporary.sum())!=4 or not data.loc[temporary,'state'].eq(1).all():
        raise AssertionError('Unexpected temporary closures')
    if int(data.status2.eq(3).sum())!=6:
        raise AssertionError('Unexpected permanent closures')
    data['fte2_temp_zero']=data.fte2.mask(temporary,0)
    data['change_temp_zero']=data.fte2_temp_zero-data.fte
    for name,mask in masks.items():
        data['group_'+name]=mask
    data['balanced_baseline']=data.change_fte.notna()
    data['balanced_temp_zero']=data.change_temp_zero.notna()
    data.to_csv(processed/'table3_analysis.csv',index=False)
    cells={}
    samples=[]
    for name,mask in masks.items():
        group=data.loc[mask]
        cells[(1,name)]=mean_se(group.fte)
        cells[(2,name)]=mean_se(group.fte2)
        cells[(3,name)]=available_change(group.fte,group.fte2)
        cells[(4,name)]=mean_se(group.change_fte)
        cells[(5,name)]=mean_se(group.change_temp_zero)
        check_stacked_regression(group,*cells[(3,name)])
        samples.append(dict(group=name,all_stores=len(group),before_n=int(group.fte.count()),
                            after_n=int(group.fte2.count()),paired_n=int(group.change_fte.count()),
                            temp_zero_paired_n=int(group.change_temp_zero.count())))
    for row in range(1,6):
        for name,left,right in [('NJ-PA','NJ','PA'),('Low-High','NJ_low','NJ_high'),('Mid-High','NJ_mid','NJ_high')]:
            m1,s1=cells[(row,left)];m0,s0=cells[(row,right)]
            cells[(row,name)]=(m1-m0,float(np.hypot(s1,s0)))
    check_balanced_regression(data,data.change_fte,*cells[(4,'NJ-PA')])
    check_balanced_regression(data,data.change_temp_zero,*cells[(5,'NJ-PA')])
    output=[]
    audit=[]
    for row in range(1,6):
        for j,column in enumerate(COLS):
            estimate,se=cells[(row,column)]
            output.append(dict(row=row,column=column,estimate=estimate,se=se,
                               published_estimate=PAPER_MEAN[row-1][j],published_se=PAPER_SE[row-1][j]))
            for metric,value,paper in [('estimate',estimate,PAPER_MEAN[row-1][j]),('se',se,PAPER_SE[row-1][j])]:
                display=float(f'{value:.2f}')
                audit.append(dict(row=row,column=column,metric=metric,value=value,display=display,
                                  published=paper,matches=bool(abs(display-paper)<1e-9)))
    numeric=pd.DataFrame(output)
    audited=pd.DataFrame(audit)
    numeric.to_csv(results/'table3_numeric.csv',index=False)
    audited.to_csv(results/'table3_audit_cells.csv',index=False)
    pd.DataFrame(samples).to_csv(results/'table3_samples.csv',index=False)
    mismatch=audited.loc[~audited.matches]
    lines=['# Table 3：就业变化与双重差分','',
           '单位：每家餐厅的全职等价就业人数（FTE）；括号为标准误。基准数据为未经修改的课程 public.csv。','',
           '| 行与样本口径 | PA | NJ | NJ−PA | NJ低工资 | NJ中工资 | NJ高工资 | 低−高 | 中−高 |',
           '|---|---:|---:|---:|---:|---:|---:|---:|---:|']
    for row in range(1,6):
        formatted=[f'{cells[(row,c)][0]:.2f} ({cells[(row,c)][1]:.2f})' for c in COLS]
        lines.append('| '+f'{row}. {ROW_LABELS[row]}'+' | '+' | '.join(formatted)+' |')
    lines += ['', '## 三个核心双重差分', '', '| 口径 | 本次计算 | 原文 |', '|---|---:|---:|']
    for row in [3,4,5]:
        lines.append(f'| {ROW_LABELS[row]} | {cells[(row,"NJ-PA")][0]:.6f} | {PAPER_MEAN[row-1][2]:.2f} |')
    lines += ['', '## 样本数', '', '| 组别 | 全部 | 政策前有效 | 政策后有效 | 两轮均有效 | 暂时关店按零后两轮有效 |',
              '|---|---:|---:|---:|---:|---:|']
    for r in samples:
        lines.append(f"| {r['group']} | {r['all_stores']} | {r['before_n']} | {r['after_n']} | {r['paired_n']} | {r['temp_zero_paired_n']} |")
    lines += ['', '## 变量与样本规则', '',
              '- FTE = EMPFT + NMGRS + 0.5 × EMPPT；不把缺失人数当零。',
              '- 6家永久关闭餐厅的政策后FTE为0。第1–4行暂时关闭/装修的政策后FTE保持缺失。仅第5行把4家暂时关闭/装修店的政策后FTE改为0，重新确定平衡样本。',
              '- NJ工资组按政策前起薪确定：低=4.25，中为4.25以上且5.00以下，高≥5.00。初始工资缺失的17家NJ店保留在州比较中，但不进入工资组比较。',
              '- 第3行：政策后可用样本均值减政策前可用样本均值。第4行：先对同一家店计算就业变化，再对两轮都有就业数据的店求平均。', '',
              '## 标准误：第3行须特别说明', '',
              '第1、2、4、5行的组内标准误为样本标准差/sqrt(n)。州或工资组之间互不重叠，其差异标准误为sqrt(SE₁²+SE₀²)。', '',
              '第3行的两轮样本有重叠，不能简单当作相互独立。当前使用餐厅层面的影响函数方差，并乘G/(G−1)小样本校正：', '',
              '`u_i = I_after × (FTE_after − mean_after)/n_after − I_before × (FTE_before − mean_before)/n_before`',
              '`SE = sqrt[G/(G−1) × sum(u_i²)]`', '',
              'G为至少一轮就业有效的餐厅数。缺失项对该得分贡献为0，并不是把缺失就业填成0。此方法已用两轮堆叠OLS及按餐厅汇总的协方差独立验证；第4、5行的州差异也用OLS和HC2标准误独立验证。', '',
              '原文未明确提供第3行非平衡样本标准误的计算细节，作者附带SAS只提供部分Table 3统计。因此该标准误是透明重建方法，不能声称是作者原算法，差异不应隐藏。', '',
              '## 与原文逐项核对', '',
              f'共核对80个已发表数值（40个估计值和40个标准误），{int(audited.matches.sum())}个在两位小数下一致，{len(mismatch)}个不同。', '',
              '| 行 | 列 | 指标 | 本次 | 原文 |','|---|---|---|---:|---:|']
    for r in mismatch.to_dict('records'):
        lines.append(f"| {r['row']} | {r['column']} | {r['metric']} | {r['display']:.2f} | {r['published']:.2f} |")
    lines += ['', '## 差异解释与局限', '',
              f'第3行州差异从当前数据算得 {cells[(3,"NJ-PA")][0]:.9f}，四舍五入为2.75，原文为2.76。此前讲解称2.76来自未四舍五入数值，这个说法没有证据支持，现予以纠正。原文与当前公开数据可能存在版本、样本或计算细节差异，但目前未确认原因。', '',
              '第3行的标准误差异与未确定的原文算法有关；其余行也保留所有小差异，不为凑原文数值调整数据或计算过程。', '',
              '这些正向差分依赖比较组、趋势等识别假设；历史表格的餐厅层面标准误不消除只有两个政策地区的推断局限。此处先复现并说明方法，不把正估计直接当作普遍政策结论。']
    (results/'table3_replication.md').write_text('\n'.join(lines)+'\n',encoding='utf-8')
    validation={'input_filename':path.name,'sha256':hashlib.sha256(path.read_bytes()).hexdigest(),
                'group_counts_match_paper':True,'row3_stacked_ols_validation':True,
                'rows4_5_ols_hc2_validation':True,'original_row3_se_method_confirmed':False,
                'numeric_cells_checked':len(audited),'numeric_cells_matched':int(audited.matches.sum()),
                'numeric_cells_different':len(mismatch),'samples':samples}
    (results/'table3_validation.json').write_text(json.dumps(validation,indent=2),encoding='utf-8')
    print(numeric.loc[numeric.column.eq('NJ-PA'),['row','estimate','se','published_estimate','published_se']].to_string(index=False))
    print(pd.DataFrame(samples).to_string(index=False))
    print(f'Table 3: {int(audited.matches.sum())}/80 published cells match at displayed precision; all independent calculation checks passed.')


if __name__=='__main__':
    main()
