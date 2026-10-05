"""Table 3 入口：python run_table3.py --data 路径/public.csv。"""
from pathlib import Path
import subprocess
import sys

if __name__ == "__main__":
    root = Path(__file__).resolve().parent
    subprocess.run([sys.executable, str(root / "src/04_table3.py"), *sys.argv[1:]],
                   cwd=root, check=True)
