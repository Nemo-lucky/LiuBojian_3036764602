# 拓展A：所有权异质性

在桌面 `01_DID/Table2_Python` 项目终端运行：

```powershell
python run_extension.py --data "..\data\public.csv"
```

使用现有requirements.txt里的pandas、numpy、scipy、matplotlib，不需要额外下载数据。
主结果是 `NJ_brands_primary`：357家餐厅，直营店效果减加盟店效果约−0.942，HC3标准误约2.641，近似p值约0.721。
这表示没有足够证据确认所有权分组的效果不同，不是证明差异为零。

打开 `results/extension_ownership_report.md`，按Ctrl+Shift+V查看中文说明、分组表和两张图。
主回归：就业变化 = 截距 + NJ + 直营店 + NJ×直营店 + 品牌控制。
其中NJ×直营店的系数才是直接检验两类店差异的关键。

输出：

- `extension_ownership_groups.csv`：四组样本和就业变化。
- `extension_ownership_effects.csv`：所有模型的组别效果、差异、HC3区间和p值。
- `extension_ownership_coefficients.csv`：全部回归系数。
- `extension_ownership_brand_counts.csv`：所有权、州、品牌交叉样本数。
- `extension_ownership_changes.png/svg`：分组变化图。
- `extension_ownership_effects.png/svg`：主结果和区间图。
- `extension_ownership_validation.json`：输入校验和、模型计划和计算检查。

这些结果是探索性的。店级HC3不能解决两个州共同冲击带来的推断问题；所有权也不是随机分配。说明文件中完整保留限制。
逐店文件 `data/processed/extension_ownership_analysis.csv` 被Git忽略，请勿公开。

拓展已有计算与验证版本；仍需你本地运行、理解结果，再纳入正式报告。最终提交还需要完整报告、统一流程、可复用工作流和GitHub仓库。
