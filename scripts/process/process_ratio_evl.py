"""
Script to process the ratio of the evaluation metrics
"""

import pandas as pd

from environ.process.boom_split import boom_split
from environ.process.pfm_evl import cal_sharpe, cal_sortino
from scripts.process.result_agg import dict_result_with_benchmark

ratio_evl_dict = {}

df_ratio_evl_whole_latex, df_ratio_evl_boom_latex, df_ratio_evl_bust_latex = (
    pd.DataFrame(),
    pd.DataFrame(),
    pd.DataFrame(),
)

for strategy, strategy_info in dict_result_with_benchmark.items():
    df_ret = strategy_info["ret"].reset_index()

    # append a row with index as strategy and columns as evaluation metrics
    df_ratio_evl_whole_latex = pd.concat(
        [
            df_ratio_evl_whole_latex,
            pd.DataFrame(
                [
                    [
                        df_ret["ret"].mean(),
                        df_ret["ret"].std(),
                        cal_sharpe(df_ret),
                        cal_sortino(df_ret),
                    ]
                ],
                index=[strategy],
                columns=["Avg Return", "Std", "Sharpe Ratio", "Sortino Ratio"],
            ),
        ]
    )

    df_ratio_evl_boom_latex = pd.concat(
        [
            df_ratio_evl_boom_latex,
            pd.DataFrame(
                [
                    [
                        boom_split(df_ret)[0]["ret"].mean(),
                        boom_split(df_ret)[0]["ret"].std(),
                        cal_sharpe(boom_split(df_ret)[0]),
                        cal_sortino(boom_split(df_ret)[0]),
                    ]
                ],
                index=[strategy],
                columns=["Avg Return", "Std", "Sharpe Ratio", "Sortino Ratio"],
            ),
        ]
    )

    df_ratio_evl_bust_latex = pd.concat(
        [
            df_ratio_evl_bust_latex,
            pd.DataFrame(
                [
                    [
                        boom_split(df_ret)[1]["ret"].mean(),
                        boom_split(df_ret)[1]["ret"].std(),
                        cal_sharpe(boom_split(df_ret)[1]),
                        cal_sortino(boom_split(df_ret)[1]),
                    ]
                ],
                index=[strategy],
                columns=["Avg Return", "Std", "Sharpe Ratio", "Sortino Ratio"],
            ),
        ]
    )

ratio_evl_dict["whole"] = df_ratio_evl_whole_latex
ratio_evl_dict["boom"] = df_ratio_evl_boom_latex
ratio_evl_dict["bust"] = df_ratio_evl_bust_latex
