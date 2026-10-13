"""Table 2 一键入口：在项目目录运行 python run_table2.py。"""
from pathlib import Path
import subprocess
import sys


if __name__ == "__main__":
    # 使用启动本文件的同一个 Python，运行实际的 Table 2 分析代码。
    project = Path(__file__).resolve().parents[1]
    subprocess.run(
        [sys.executable, str(project / "code" / "src" / "02_table2.py"), *sys.argv[1:]],
        cwd=project,
        check=True,
    )
