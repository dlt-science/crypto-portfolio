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


def cal_sortino(
    df_res: pd.DataFrame,
):
    """
    Function to calculate the sortino ratio
    """

    return (df_res.mean() / df_res[df_res < 0].std()).values[0]
