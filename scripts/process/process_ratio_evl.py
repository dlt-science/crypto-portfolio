"""
Script to process the ratio of the evaluation metrics
"""

import pandas as pd

from environ.process.pfm_evl import cal_sharpe, cal_sortino
from environ.process.standarize import min_max_scaler
from scripts.process.result_agg import dict_result_with_benchmark

df_ratio_evl_latex = pd.DataFrame()

for cash_con in ["0.33", "0.1"]:
    for freq in ["weekly", "monthly", "quarterly"]:
        for strategy, strategy_info in dict_result_with_benchmark[cash_con][
            freq
        ].items():
            df_ret = strategy_info["wealth_daily"].reset_index()

            # append a row with index as strategy and columns as evaluation metrics
            df_ratio_evl_latex = pd.concat(
                [
                    df_ratio_evl_latex,
                    pd.DataFrame(
                        [
                            [
                                df_ret["wealth_ret"].mean(),
                                df_ret["wealth_ema"].iloc[-1],
                                cal_sharpe(df_ret),
                                cal_sortino(df_ret),
                            ]
                        ],
                        index=[f"{strategy},{cash_con},{freq}"],
                        columns=[
                            "Avg Return",
                            "Wealth EMA",
                            "Sharpe Ratio",
                            "Sortino Ratio",
                        ],
                    ),
                ]
            )

# standardize the dataframe
df_ratio_evl_whole_latex_scal = min_max_scaler(df_ratio_evl_latex.copy())

# calculate the mean of the evaluation metrics
df_ratio_evl_latex["Aggregate Index"] = (
    df_ratio_evl_whole_latex_scal["Avg Return"]
    + df_ratio_evl_whole_latex_scal["Wealth EMA"]
    + df_ratio_evl_whole_latex_scal["Sharpe Ratio"]
    + df_ratio_evl_whole_latex_scal["Sortino Ratio"]
) / 4

# sort the dataframe by the aggregate index
df_ratio_evl_latex.sort_values("Aggregate Index", ascending=False, inplace=True)
