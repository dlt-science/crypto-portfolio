"""
Script to visualize the cumulative return
"""

import matplotlib.pyplot as plt

from environ.constants import FIGURE_PATH
from scripts.process.boom_bust import BOOM_BUST
from scripts.process.result_agg import dict_result_with_benchmark

# plot the cumulative return
plt.figure(figsize=(12, 8))

# plot the strategy
for strategy, strategy_info in dict_result_with_benchmark.items():
    plt.plot(
        strategy_info["ret"]["cum_ret"],
        label=strategy,
    )


# # plot the boom bust periods and legend
# for i in BOOM_BUST:
#     if i["main_trend"] == "boom":
#         plt.axvspan(i["start"], i["end"], facecolor="g", alpha=0.2)
#     if i["main_trend"] == "bust":
#         plt.axvspan(i["start"], i["end"], facecolor="r", alpha=0.2)
#     if i["main_trend"] == "none":
#         plt.axvspan(i["start"], i["end"], facecolor="grey", alpha=0.2)

# # label the legend for boom bust periods
# plt.axvspan(
#     BOOM_BUST[0]["start"], BOOM_BUST[0]["start"], facecolor="g", alpha=0.2, label="Boom"
# )
# plt.axvspan(
#     BOOM_BUST[0]["start"], BOOM_BUST[0]["start"], facecolor="r", alpha=0.2, label="Bust"
# )
# plt.axvspan(
#     BOOM_BUST[0]["start"],
#     BOOM_BUST[0]["start"],
#     facecolor="grey",
#     alpha=0.2,
#     label="None",
# )

# plot the legend
plt.legend()

# tight layout
plt.tight_layout()

# save the figure
# plt.savefig(FIGURE_PATH / "cum_ret.pdf", dpi=300)
plt.show()
