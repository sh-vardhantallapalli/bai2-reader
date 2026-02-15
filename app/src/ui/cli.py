"""This is a CLI entry point which run the streamlit in subprocess.
Not so efficient but works!
"""

import subprocess

from pathlib import Path


def run_streamlit() -> None:
    """Function which is called from CLI. Check [tool.poetry.scripts] section in pyproject.toml"""
    curr_path = Path(__file__).parent
    command = ["streamlit", "run", str(Path(curr_path, "home.py").resolve())]
    print(f"Running command: {command}")
    proc = subprocess.run(command)
    print(proc.returncode)
