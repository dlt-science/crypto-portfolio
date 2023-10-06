"""
Function to evaluate the performance of the optimized portfolio
"""

import pandas as pd


def cal_sharpe(
    df_res: pd.DataFrame,
):
    """
    Function to calculate the sharpe ratio
    """

    return (df_res.mean() / df_res.std()).values[0]
