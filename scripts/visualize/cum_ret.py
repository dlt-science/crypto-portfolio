"""
Script to visualize the cumulative return
"""

import matplotlib.pyplot as plt
from scripts.process.result_agg import dict_result
from environ.constants import FIGURE_PATH

# plot the cumulative return
plt.figure(figsize=(12, 8))

for strategy, strategy_info in dict_result.items():
    plt.plot(
        strategy_info["ret"]["cum_ret"],
        label=strategy,
    )

plt.legend()
plt.tight_layout()

# save the figure
plt.savefig(FIGURE_PATH / "cum_ret.pdf", dpi=300)
