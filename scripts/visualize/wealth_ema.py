"""
Script to visualize the wealth dynamics
"""

import matplotlib.pyplot as plt

from environ.constants import FIGURE_PATH
from scripts.process.boom_bust import BOOM_BUST
from scripts.process.result_agg import dict_result_with_benchmark

# plot the strategy
for cash_con in ["0.33", "0.1"]:
    for freq in ["weekly", "monthly", "quarterly"]:
        # plot the boom bust periods and legend
        for i in BOOM_BUST:
            if i["main_trend"] == "boom":
                plt.axvspan(i["start"], i["end"], facecolor="g", alpha=0.2)
            if i["main_trend"] == "bust":
                plt.axvspan(i["start"], i["end"], facecolor="r", alpha=0.2)
            if i["main_trend"] == "none":
                plt.axvspan(i["start"], i["end"], facecolor="grey", alpha=0.2)

        # label the legend for boom bust periods
        plt.axvspan(
            BOOM_BUST[0]["start"],
            BOOM_BUST[0]["start"],
            facecolor="g",
            alpha=0.2,
            label="Boom",
        )
        plt.axvspan(
            BOOM_BUST[0]["start"],
            BOOM_BUST[0]["start"],
            facecolor="r",
            alpha=0.2,
            label="Bust",
        )
        plt.axvspan(
            BOOM_BUST[0]["start"],
            BOOM_BUST[0]["start"],
            facecolor="grey",
            alpha=0.2,
            label="None",
        )
        dict_result = dict_result_with_benchmark[cash_con][freq].copy()
        for strategy, strategy_info in dict_result.items():
            # plot the wealth in line and wealth_ema in dashed line in the color
            # of the strategy
            plt.plot(
                strategy_info["wealth_daily"]["wealth_ema"],
                label=strategy,
            )
        # plot the legend on the upper left corner
        plt.legend(loc="upper left")

        plt.xticks(rotation=90)
        plt.ylabel("Exponential Moving Average of Daily Wealth")
        # grid layout
        plt.grid(
            alpha=0.5,
        )

        # tight layout
        plt.tight_layout()

        # save the figure
        plt.savefig(FIGURE_PATH / f"wealth_{cash_con}_{freq}_ema.pdf", dpi=300)

        plt.close()
