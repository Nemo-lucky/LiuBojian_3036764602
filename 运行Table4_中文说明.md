# 在 VS Code 运行 Table 4

在你已经打开的桌面 `01_DID/Table2_Python` 项目终端中，依次运行：

```powershell
python -m pip install -r requirements.txt
python code/run_table4.py --data "..\data\public.csv"
```

这次新增 scipy 依赖，用于系数显著性和联合 F 检验。安装完成后再运行第二行。

预期五组都使用357家餐厅，系数依次约为2.33、2.30、15.65、14.92、11.98。
验证文件中的 published_matches 为16，published_numeric_cells为18。

打开 `outputs/tables/table4_replication.md`，按 Ctrl+Shift+V 查看表格及中文解释。
`outputs/tables/table4_numeric.csv` 保存未四舍五入的主要结果；
`outputs/tables/table4_all_coefficients.csv` 包含全部控制变量和截距系数；
`outputs/tables/table4_sample_flow.csv` 是样本筛选计数；
`outputs/tables/table4_audit_cells.csv` 逐格核对原文；
`outputs/tables/table4_author_sas_comparison.csv` 单独保存作者程序第五组未加入所有权的结果。

第五组主结果按论文表注含所有权，不能为匹配原文而隐瞒控制设定。
作者程序对照能匹配11.91 (7.39)，但其残差标准差8.74仍与原表8.75不同。

处理数据在 `data/processed/table4_analysis.csv`，包含逐店入样标记和排除原因，已被Git忽略，请勿公开课程原始或处理数据。

跑完这一阶段后，四项指定表图都有可运行版本；仍需独立拓展、完整报告、统一工作流与GitHub交付。
