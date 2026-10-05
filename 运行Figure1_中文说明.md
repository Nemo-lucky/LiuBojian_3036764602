# 运行 Figure 1

你在 VS Code 打开的桌面 `01_DID/Table2_Python` 项目已增加 Figure 1。文件夹名称不影响使用。

在当前终端先安装新增的绘图库：

```powershell
python -m pip install -r requirements.txt
```

然后运行：

```powershell
python run_figure1.py --data "..\data\public.csv"
```

在 `results` 中打开 `figure1.png` 查看图片；`figure1_中文说明.md` 解释分组、分母、核验和局限。完整分析代码在 `src/03_figure1.py`。

程序从原始 CSV 自动生成图片和核验表，不需要手动编辑数据。PNG 和 SVG 均可用于报告，引用原论文并说明本图为自行重建。
