"""
Script to visualize the weight
"""

import matplotlib.pyplot as plt

from environ.constants import FIGURE_PATH
from scripts.process.preprocess_wgt import PLOT_DICT

cmap = plt.get_cmap("tab20")


for period, period_info in PLOT_DICT.items():
    for strategy, strategy_wgt in period_info.items():
        df_wgt = strategy_wgt
        df_wgt_pivot = df_wgt.pivot(index="quarter", columns="name", values="weight")

        # plot the stake bar chart using the token-color mapping
        df_wgt_pivot.plot.bar(stacked=True, colormap=cmap, figsize=(12, 10))

        plt.legend()
        plt.tight_layout()
        plt.savefig(
            FIGURE_PATH / f"{strategy}_{period}_wgt.pdf".replace(" ", "_"), dpi=300
        )
        plt.close()
