"""
Function to evaluate the performance of the optimized portfolio
"""

import pandas as pd


def cal_sharpe(
    df_res: pd.DataFrame,
    ret_col: str = "wealth_ret",
):
    """
    Function to calculate the sharpe ratio
    """

    return df_res[ret_col].mean() / df_res[ret_col].std()


def cal_sortino(
    df_res: pd.DataFrame,
    ret_col: str = "wealth_ret",
):
    """
    Function to calculate the sortino ratio
    """

    return df_res[ret_col].mean() / df_res.loc[df_res[ret_col] < 0, ret_col].std()
