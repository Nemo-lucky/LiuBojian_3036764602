"""Run Table 4 with the current Python interpreter."""
from pathlib import Path
import subprocess
import sys

project = Path(__file__).resolve().parent
subprocess.run([sys.executable, str(project/'src'/'05_table4.py'), *sys.argv[1:]],
               cwd=project, check=True)
