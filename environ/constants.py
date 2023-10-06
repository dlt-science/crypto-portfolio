"""
Constants for the project
"""

from pathlib import Path

from environ.settings import PROJECT_ROOT

# Paths
DATA_PATH: Path = PROJECT_ROOT / "data"
PROCESSED_DATA_PATH: Path = PROJECT_ROOT / "processed_data"
TABLE_PATH: Path = PROJECT_ROOT / "tables"

# Crypto to exclude from swiss quote
LOW_VOL_LIST = ["0x", "Audius", "Bancor"]
STABLE_COIN_LIST = ["USD Coin"]

# Asset classes
ASSET_CLASSES = ["Bitcoin", "Cash", "Other Crypto"]
