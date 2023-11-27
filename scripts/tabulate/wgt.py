"""
Scripts to generate the weight for the portfolio
"""

from environ.constants import TABLE_PATH
from environ.tabulate.latex_tab import gen_latex_tab
from scripts.process.preprocess_wgt import PLOT_DICT

for period, period_info in PLOT_DICT.items():
    for strategy, strategy_wgt in period_info.items():
        df_wgt = strategy_wgt
        df_wgt_pivot = df_wgt.pivot(index="quarter", columns="name", values="weight")
        gen_latex_tab(
            df_wgt_pivot,
            TABLE_PATH / f"{strategy}_{period}_wgt_0.33.tex".replace(" ", "_"),
        )
