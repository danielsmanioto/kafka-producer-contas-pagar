"""Compatibility wrapper for legacy test script path."""

import runpy
from pathlib import Path


if __name__ == "__main__":
    target = Path(__file__).resolve().parent / "tests" / "test_kafka_producer.py"
    runpy.run_path(str(target), run_name="__main__")

