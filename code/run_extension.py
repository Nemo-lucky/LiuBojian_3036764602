"""Run ownership heterogeneity extension."""
from pathlib import Path
import subprocess
import sys

project=Path(__file__).resolve().parents[1]
subprocess.run([sys.executable,str(project/'code'/'src'/'06_extension_ownership.py'),*sys.argv[1:]],cwd=project,check=True)
