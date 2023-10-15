"""
Script to visualize the weight
"""

import matplotlib.pyplot as plt

from environ.constants import FIGURE_PATH
from scripts.process.boom_bust import BOOM_BUST
from scripts.process.result_agg import dict_result

for strategy, strategy_info in dict_result.items():
    if strategy == "S\&P" or strategy == "BTC":
        continue

    df_wgt = strategy_info["wgt"]
    plt.stackplot(
        strategy_info["wgt"]["quarter"].unique(),
        *[
            strategy_info["wgt"][strategy_info["wgt"]["name"] == name]["weight"]
            for name in ["Bitcoin", "Cash", "Others"]
        ],
        labels=["Bitcoin", "Cash", "Others"],
        colors=["#F7931A", "#F7F7F7", "#4F4F4F"],
        alpha=0.5,
    )

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

    plt.legend()
    plt.tight_layout()
    plt.savefig(FIGURE_PATH / f"{strategy}_wgt.pdf".replace(" ", "_"), dpi=300)
    plt.close()
