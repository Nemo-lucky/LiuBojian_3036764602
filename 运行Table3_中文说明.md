# 运行 Table 3

在桌面 `01_DID/Table2_Python` 的 VS Code 终端运行：

```powershell
python run_table3.py --data "..\data\public.csv"
```

Table 3 使用已经安装的 pandas 和 numpy，不需要增加依赖。

运行后打开 `results/table3_replication.md`，按 Ctrl+Shift+V 预览。

- `src/04_table3.py`：完整计算、原文对照和验证代码。
- `results/table3_numeric.csv`：所有5行×8列的完整精度估计和标准误。
- `results/table3_samples.csv`：每组在不同口径下的样本数。
- `results/table3_audit_cells.csv`：80个原文数值的逐项核对。
- `results/table3_validation.json`：回归形式独立校验与输入校验值。
- `data/processed/table3_analysis.csv`：含样本标记的处理数据，只留本地。

第3行是两轮可用均值之差；第4行仅比较同一家店前后变化；第5行将暂时关店的政策后就业设零再计算。第3行的标准误采用考虑同店两轮相关性的透明重建方法，原文具体算法尚未确认，详见生成报告。
