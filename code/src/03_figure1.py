"""Reconstruct Figure 1 with documented 10-cent wage bins and a pooled upper tail.

The published figure does not specify exact edges or tail handling. These are
explicit reconstruction choices; exact original bar percentages are unverified.
"""
import argparse
import hashlib
import json
from pathlib import Path
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from course_data import ROOT, INPUT, load_course
(ROOT / 'outputs' / 'figures').mkdir(parents=True, exist_ok=True)


def main():
    parser = argparse.ArgumentParser(description="Reconstruct the starting-wage distributions")
    parser.add_argument("--data", type=Path, default=INPUT, help="Path to course public.csv")
    args = parser.parse_args()
    path = args.data.expanduser().resolve()
    raw, _ = load_course(path)
    results = ROOT / 'outputs' / 'tables'
    results.mkdir(parents=True, exist_ok=True)
    # Integer cents avoid floating-point ambiguity at 4.30, 4.40, etc.
    lower_edges = np.arange(420, 551, 10)
    labels = [f"{(lo+5)/100:.2f}" for lo in lower_edges[:-1]] + ["5.50+"]
    distributions, summaries = [], []
    for wave, variable in [(1, "wage_st"), (2, "wage_st2")]:
        for state, name in [(1, "NJ"), (0, "PA")]:
            all_values = raw.loc[raw.state.eq(state), variable]
            wages = all_values.dropna()
            if len(wages) == 0 or (wages < 4.20).any():
                raise ValueError("Missing valid wages or observed wages below the documented bins")
            cents = np.rint(wages.to_numpy()*100).astype(int)
            if not np.allclose(cents, wages.to_numpy()*100, atol=1e-7, rtol=0):
                raise ValueError("Wage precision exceeds one cent; review binning")
            groups = np.minimum((cents-420)//10, len(lower_edges)-1)
            counts = np.bincount(groups, minlength=len(lower_edges))
            # Independent interval counting verifies edge placement and the tail.
            manual = [int(((cents >= lo) & (cents < lo+10)).sum())
                      if lo < 550 else int((cents >= 550).sum()) for lo in lower_edges]
            if not np.array_equal(counts, manual) or int(counts.sum()) != len(wages):
                raise AssertionError("Bin counts fail independent interval/count checks")
            percent = 100*counts/len(wages)
            if not np.isclose(percent.sum(), 100, atol=1e-10):
                raise AssertionError("Distribution does not sum to 100%")
            summaries.append(dict(wave=wave, state=name, surveyed=len(all_values),
                                  valid_wages=len(wages), missing_wages=int(all_values.isna().sum()),
                                  minimum=wages.min(), maximum=wages.max(),
                                  high_tail_n=int(counts[-1]), percent_total=float(percent.sum())))
            for j, lo in enumerate(lower_edges):
                distributions.append(dict(wave=wave, state=name, bin_index=j,
                                          label=labels[j], lower_inclusive=lo/100,
                                          upper_exclusive=(lo+10)/100 if lo < 550 else np.nan,
                                          upper_tail=bool(lo == 550), count=int(counts[j]),
                                          valid_wage_n=len(wages), percent=float(percent[j])))
    distribution = pd.DataFrame(distributions)
    summary = pd.DataFrame(summaries)
    distribution.to_csv(results/'figure1_bin_counts.csv', index=False)
    summary.to_csv(results/'figure1_sample_checks.csv', index=False)

    plt.rcParams.update({'font.family':'DejaVu Sans','font.size':10,'axes.titlesize':13,
                         'axes.labelsize':11,'svg.fonttype':'none'})
    fig, axes = plt.subplots(2, 1, figsize=(10, 10.5))
    fig.subplots_adjust(top=.85, bottom=.23, left=.095, right=.97, hspace=.70)
    fig.suptitle('Figure 1. Distribution of starting wage rates', y=.97, fontsize=17)
    fig.text(.5,.934,'Card & Krueger (1994) | Reconstruction from the course survey data',
             ha='center', fontsize=10, color='#444444')
    x = np.arange(len(labels))
    for ax, wave, title, maximum in zip(axes,[1,2],
            ['Before the policy: February-March 1992','After the policy: November-December 1992'],[35,90]):
        for offset, name, color, hatch in [(-.19,'NJ','black',None),(.19,'PA','white','////')]:
            y = distribution.loc[distribution.wave.eq(wave)&distribution.state.eq(name), 'percent'].to_numpy()
            ax.bar(x+offset,y,width=.36,color=color,edgecolor='black',hatch=hatch,
                   linewidth=.7,label='New Jersey' if name=='NJ' else 'Pennsylvania',zorder=3)
        ns=summary.loc[summary.wave.eq(wave)].set_index('state').valid_wages
        ax.set_title(f'{title}\nValid wage observations: NJ = {ns["NJ"]}, PA = {ns["PA"]}',pad=10)
        ax.set_ylabel('Percent of stores')
        ax.set_xlabel('Starting wage bin ($ per hour)')
        ax.set_xticks(x,labels,rotation=45,ha='right')
        ax.set_ylim(0,maximum)
        ax.set_yticks(np.arange(0,maximum+1,5 if wave==1 else 10))
        ax.grid(axis='y',color='#dedede',linewidth=.6,zorder=0)
        ax.set_axisbelow(True)
    handles, legend_labels = axes[0].get_legend_handles_labels()
    fig.legend(handles,legend_labels,loc='lower center',bbox_to_anchor=(.5,.105),ncol=2,frameon=False)
    fig.text(.095,.060,'Each distribution excludes missing wages. Bins are [4.20, 4.30), [4.30, 4.40), ...; final bin is $5.50 and above.',fontsize=8)
    fig.text(.095,.040,'Tick labels show bin midpoints except the upper tail. Bin edges and tail grouping are explicit reconstruction choices.',fontsize=8)
    fig.savefig(ROOT / 'outputs' / 'figures' / 'figure1.png',dpi=200,facecolor='white')
    fig.savefig(ROOT / 'outputs' / 'figures' / 'figure1.svg',facecolor='white')
    plt.close(fig)

    key=distribution.loc[distribution.wave.eq(2)&distribution.state.eq('NJ')&distribution.bin_index.eq(8)].iloc[0]
    summary_rows=['| 调查 | 州 | 全部餐厅 | 有效工资 | 缺失工资 | 工资至少5.50的餐厅 |',
                  '|---|---|---:|---:|---:|---:|']
    for r in summaries:
        summary_rows.append(f"| {r['wave']} | {r['state']} | {r['surveyed']} | {r['valid_wages']} | {r['missing_wages']} | {r['high_tail_n']} |")
    note=['# Figure 1 复现说明','',
          '已生成政策前后两州起薪分布图，并检查每个州、每一轮的分组计数与比例。此图是公开数据下的透明重建，尚不能声称逐根柱子精确匹配原图。','',
          '## 数据与分母','',*summary_rows,'',
          '只剔除所画工资变量的缺失值，不要求该店就业或其他变量完整，也不要求两轮工资都完整。各州各轮分别归一化到 100%。不因第二轮装修状态而删除已报告的工资。','',
          '## 工资分组','',
          '按照原图横轴的 0.10 美元间隔重建分组：4.20≤工资<4.30、4.30≤工资<4.40，以此类推。最后一组为工资≥5.50，包含超过5.60的记录，避免悄悄丢弃尾部。原图最后一项标为5.55，本图明确标成5.50+。','',
          '区间端点和上尾合并是当前重建选择，原文图注没有完整说明，作者所附 check.sas 也未提供 Figure 1 的绘图程序。因此不能仅凭视觉接近认定完全复现。','',
          '用整数“分”分组，防止浮点误差把4.30等端点分错；另用逐区间计数独立校验所有分组。','',
          '## 如何理解与 Table 2 的区别','',
          f"政策后 NJ 在 [5.00,5.10) 区间有 {int(key['count'])} 家，有效工资记录为 {int(key['valid_wage_n'])} 家，因此柱高为 {key['percent']:.2f}%。",'',
          'Table 2 的目标工资指标是恰好等于5.05的283家，按照作者 SAS 指示变量口径除以全部331家，得到85.5%。Figure 1 则对工资区间计数并以有效工资为分母，两者不应强行相等。','',
          '## 原图比较与限制','',
          '原图与本次重建均呈现：政策前两州分布较分散，政策后 NJ 高度集中在新最低工资附近，PA 仍较分散。两张子图纵轴上限分别为35%和90%，沿用原图的不同刻度。','',
          '原图没有提供每根柱子的精确数值表，目前未完成逐柱数值验证。区间端点、尾部处理、有效样本口径或历史数据版本都可能造成高度差异；不以改变数据来追求视觉一致。图的边际分布不能证明同一餐厅的工资迁移，也不单独识别就业因果效果。','',
          '## 文件','',
          '- figure1.png：可预览的图片。','- figure1.svg：可缩放的矢量图片。',
          '- figure1_bin_counts.csv：所有柱子的区间、计数、分母与比例。',
          '- figure1_sample_checks.csv：样本、缺失、范围和比例合计。',
          '- figure1_validation.json：输入校验值和计算检查。']
    (results/'figure1_中文说明.md').write_text('\n'.join(note)+'\n',encoding='utf-8')
    validation={'input_filename':path.name,'sha256':hashlib.sha256(path.read_bytes()).hexdigest(),
                'binning':'10 cents, left-inclusive, from 4.20; final tail >=5.50',
                'denominator':'nonmissing wage, within state and wave',
                'independent_interval_counts_match':True,'all_distribution_totals_100_percent':True,
                'exact_original_figure_match_verified':False,'samples':summaries}
    (results/'figure1_validation.json').write_text(json.dumps(validation,indent=2),encoding='utf-8')
    print(summary.to_string(index=False))
    print(f'NJ wave 2, [5.00,5.10): {int(key["count"])}/{int(key["valid_wage_n"])} = {key["percent"]:.2f}%')
    print('Figure 1 PNG, SVG, counts and validation saved in outputs/tables/ and outputs/figures/.')


if __name__ == '__main__':
    main()
