# Table 2：代码与运行说明

这份代码读取老师提供的 `01_DID/data/public.csv`，计算 Table 2 的 20 行统计量，并与原文对照。
当前版本仍有已列明的数值差异，尚不能称为完全匹配原文；Tables 3–4、Figure 1 和独立拓展未包含在此入口中。

## 文件如何对应

| 文件 | 作用 |
|---|---|
| `run_table2.py` | 一键运行入口 |
| `src/course_data.py` | 读取原始 CSV、检查数据、构造 FTE 和餐价等变量 |
| `src/02_table2.py` | 分州计算均值、标准误、t 统计量，输出原文对照与分母检查 |
| `src/audit_table2.py` | 逐项核对原文均值、标准误和 t，记录差异与口径诊断 |
| `requirements.txt` | 需要安装的 Python 库 |

## 输入文件位置

把原来的 `01_DID` 文件夹放在 `run_table2.py` 旁边，保留内部文件名和结构：

```text
项目文件夹/
  run_table2.py
  requirements.txt
  src/
    course_data.py
    02_table2.py
    audit_table2.py
  01_DID/
    data/
      public.csv
```

当前电脑上的完整项目已经具备这一结构，不需要再次复制数据。
单独下载代码 ZIP 时，需自行把课程 `01_DID` 文件夹放入解压目录；代码 ZIP 不附带课程原始数据。

## 运行

使用 Python 3.10 或更新版本。在项目文件夹打开终端，首次安装依赖：

```powershell
python -m pip install -r requirements.txt
```

然后运行：

```powershell
python run_table2.py
```

若 Windows 的 Python 命令名是 `py`，将上述两条命令开头的 `python` 换成 `py`。

也可以直接读取桌面上的原始 CSV，无需复制：

```powershell
python run_table2.py --data "C:\Users\ber寨\Desktop\01_DID\data\public.csv"
```

`--data` 后填写 CSV 文件的完整路径，不是 `01_DID` 文件夹路径。程序只读取输入，结果仍生成在代码项目的 `results` 文件夹中。

在 VS Code 中选择“文件 → 打开文件夹”，打开包含 `run_table2.py` 的项目文件夹，再选择“终端 → 新建终端”，执行上面的命令。不能只复制某一行循环，也不要把这些终端命令粘贴进 Python 的 `>>>` 提示符。

## 计算过程

1. 读取 CSV，核对 410 行、46 列，以及州、品牌、第二轮营业状态等编码。
2. 原始 SHEET 编号 407 在不同州出现两次，因此检查 `(STATE, SHEET)` 组合键，不直接删除重复 SHEET。
3. 构造 FTE = 全职员工 + 经理 + 0.5 × 兼职员工。
4. 第二轮永久关店 FTE 设为 0，暂时关闭或装修的 FTE 设为缺失；普通缺失不当作 0。
5. 构造餐价 = 饮料 + 薯条 + 主食。任一项缺失，餐价保持缺失。
6. 按 STATE 分成 NJ 和 PA，为每个指标分别选择有效样本，计算均值与样本数。
7. 标准误 SE = 样本标准差 / sqrt(N)。两州差异的 t = (NJ均值 − PA均值) / sqrt(SE_NJ² + SE_PA²)。
8. 输出所有计算结果，再与手工录入的原文对照值比较。原文数字仅用于对照，不参与复现均值、标准误或 t 的计算。

两个特殊口径：全职占比按作者 SAS 程序用 `EMPFT / FTE`；工资恰好等于特定金额的指标按全部调查餐厅作为分母，缺失工资作为“未报告该金额”。后者另输出只用有效工资作为分母的结果，供检查。

## 生成的结果

- `results/table2_replication.md`：可阅读的表格、原文对照、计算口径和差异记录。
- `results/table2_numeric.csv`：完整精度的均值、标准误、t 与各项有效样本数。
- `results/table2_wage_denominators.csv`：工资比例在不同分母下的对照。
- `docs/course_data_validation.json`：输入文件校验值、样本检查；若作者原始数据存在，额外比较两份数据。
- `data/processed/course_analysis.csv`：带派生变量的分析数据，仅供本地使用，不放入公开 GitHub。

完整核对覆盖原文的 88 个已发表数值，82 个在显示精度下一致。差异为 1 处均值、1 处标准误和 4 处 t，详见 `results/table2_audit_中文.md`。诊断发现一条装修店记录可以解释均值和标准误差异，但不能确认原文实际采用该处理，4 处 t 的差异也未完全解释。代码保留基准结果，不通过改动数据强行匹配原文。
