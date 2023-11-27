"""
Constants for the project
"""

from pathlib import Path

from environ.settings import PROJECT_ROOT

# Paths
DATA_PATH: Path = PROJECT_ROOT / "data"
PROCESSED_DATA_PATH: Path = PROJECT_ROOT / "processed_data"
TABLE_PATH: Path = PROJECT_ROOT / "tables"
FIGURE_PATH: Path = PROJECT_ROOT / "figures"


# Crypto to exclude from swiss quote
LOW_VOL_LIST = ["0x", "Audius", "Bancor"]
STABLE_COIN_LIST = ["USD Coin"]

# Asset classes
ASSET_CLASSES = ["Bitcoin", "Cash", "Other Crypto"]

# Initial Weath
INITIAL_WEALTH = 1_000_000

# Transaction cost
TRANSACTION_COST = 0.008

glob_con = {
    "0.1": (
        {
            "type": "eq",
            "fun": lambda weight: weight.sum() - 1,
        },
        {
            "type": "ineq",
            "fun": lambda weight: 1 / 10 - weight[1],
        },
        {
            "type": "ineq",
            "fun": lambda weight: 1 / 3 - weight[2:].sum(),
        },
    ),
    "0.33": (
        {
            "type": "eq",
            "fun": lambda weight: weight.sum() - 1,
        },
        {
            "type": "ineq",
            "fun": lambda weight: 1 / 3 - weight[1],
        },
        {
            "type": "ineq",
            "fun": lambda weight: 1 / 3 - weight[2:].sum(),
        },
    ),
}
