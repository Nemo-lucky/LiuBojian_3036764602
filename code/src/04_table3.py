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
    1:'Before FTE: all valid observations', 2:'After FTE: all valid observations',
    3:'Difference of available means (unbalanced sample)', 4:'Paired-store employment changes',
    5:'Paired changes with temporary closures set to zero',
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
    results=ROOT / 'outputs' / 'tables'
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
    from english_reports import write_report
    write_report('table3_replication.md', 'table3_notes.md', [('Employment estimates and SEs', numeric), ('Sample counts', pd.DataFrame(samples)), ('Unmatched published cells', mismatch)])
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
