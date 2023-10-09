"""
Script to visualize the weight
"""

import matplotlib.pyplot as plt

from scripts.process.result_agg import dict_result
from environ.constants import FIGURE_PATH

for strategy, strategy_info in dict_result.items():
    df_wgt = strategy_info["wgt"]
    plt.stackplot(
        strategy_info["wgt"]["quarter"].unique(),
        *[
            strategy_info["wgt"][strategy_info["wgt"]["name"] == name]["weight"]
            for name in ["Bitcoin", "Caash", "Others"]
        ],
        labels=["Bitcoin", "Cash", "Others"],
    )

    plt.legend()
    plt.tight_layout()
    plt.savefig(FIGURE_PATH / f"{strategy}_wgt.pdf", dpi=300)
    plt.close()
