"""Run this analysis stage with the current Python interpreter."""
from pathlib import Path
import subprocess
import sys


if __name__ == "__main__":
    # Use the current interpreter for the analytical implementation.
    project = Path(__file__).resolve().parents[1]
    subprocess.run(
        [sys.executable, str(project / "code" / "src" / "02_table2.py"), *sys.argv[1:]],
        cwd=project,
        check=True,
    )
