"""
Script to visualize the average weight
"""

import matplotlib.pyplot as plt

from environ.constants import FIGURE_PATH
from scripts.process.result_agg import dict_result_with_benchmark

# plot the cumulative return
plt.figure(figsize=(12, 8))

# plot the strategy
for cash_con in ["0.33", "0.1"]:
    for freq in ["weekly", "monthly", "quarterly"]:
        dict_result = dict_result_with_benchmark[cash_con][freq].copy()
        for strategy, strategy_info in dict_result.items():
            # plot the wealth in line and wealth_ema in dashed line in the color
            # of the strategy

            df_plot = (
                strategy_info["wgt"].groupby(["name"])["weight"].mean().reset_index()
            )

            plt.bar(
                df_plot["name"],
                df_plot["weight"],
            )
            plt.xticks(rotation=90)
            plt.ylabel("Average Weight")

            # tight layout
            plt.tight_layout()

            # save the figure
            plt.savefig(
                FIGURE_PATH / f"avg_wgt_{cash_con}_{freq}_{strategy}.pdf", dpi=300
            )

            plt.close()
