"""
Script to generate the performance heatmap
"""
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from tqdm import tqdm
from environ.constants import FIGURE_PATH

from environ.process.optimization import freq_iterate
from scripts.process.preprocess_crypto_panel import df_crypto_processed

CMAP = sns.color_palette("rocket_r", as_cmap=True)
pct_list = [0, 0.25, 0.5, 0.75, 1]

result_dict = {}

# a dict to store the result

for slow_weight in tqdm(pct_list):
    for medium_in_medium_fast_weight in pct_list:
        dict_result = freq_iterate(
            df_crypto_processed,
            slow_medium_pct=[
                slow_weight,
                (1 - slow_weight) * medium_in_medium_fast_weight,
            ],
        )

        for strategy, strategy_info in dict_result.items():
            if strategy not in result_dict.keys():
                result_dict[strategy] = pd.DataFrame(columns=pct_list, index=pct_list)

            result_dict[strategy].loc[
                slow_weight, medium_in_medium_fast_weight
            ] = strategy_info["ret"]["ret"].mean()

for strategy, df in result_dict.items():
    sns.heatmap(df.astype(float), annot=True, cmap=CMAP)
    # save the figure
    plt.tight_layout()
    plt.savefig(f"{FIGURE_PATH}/{strategy}_heatmap.pdf", dpi=300)
    plt.close()
