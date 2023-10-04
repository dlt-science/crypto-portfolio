"""
Constants for the project
"""

from pathlib import Path

from environ.settings import PROJECT_ROOT

# Paths
DATA_PATH: Path = PROJECT_ROOT / "data"
PROCESSED_DATA_PATH: Path = DATA_PATH / "processed"
TABLE_PATH: Path = DATA_PATH / "tables"
