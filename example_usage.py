"""Compatibility wrapper for legacy example script path."""

import runpy
from pathlib import Path


if __name__ == "__main__":
    target = Path(__file__).resolve().parent / "examples" / "example_usage.py"
    runpy.run_path(str(target), run_name="__main__")

