"""Run this analysis stage with the current Python interpreter."""
from pathlib import Path
import subprocess
import sys

if __name__ == "__main__":
    root = Path(__file__).resolve().parents[1]
    subprocess.run([sys.executable, str(root / "code/src/04_table3.py"), *sys.argv[1:]],
                   cwd=root, check=True)
