"""
Objective functions for optimization
"""

import numpy as np
import pandas as pd


# mean-variance optimization
def mean_var_obj(
    weight: np.ndarray, mean_ret: pd.DataFrame, cov_mat: pd.DataFrame
) -> float:
    """
    Objective function for the mean-variance optimization
    """

    # maximize the sharpe ratio
    return -((mean_ret @ weight) / np.sqrt(weight @ cov_mat @ weight))


# minimum variance optimization
def min_var_obj(weight: np.ndarray, cov_mat: pd.DataFrame) -> float:
    """
    Objective function for the minimum variance optimization
    """

    # minimize the variance
    return weight @ cov_mat @ weight


# maximum VaR-adjusted sharpe ratio optimization
def max_var_adj_sharpe(
    weight: np.ndarray, pivot: pd.DataFrame, mean_ret: pd.DataFrame, sig: float
) -> float:
    """
    Objective function for the minimum VaR
    """

    return -(mean_ret @ weight) / (
        (pivot @ weight)
        .sort_values(ascending=True)
        .iloc[int(len(pivot @ weight) * sig)]
    )


# maximum ES-adjusted sharpe ratio optimization
def max_es_adj_sharpe(
    weight: np.ndarray, pivot: pd.DataFrame, mean_ret: pd.DataFrame, sig: float
) -> float:
    """
    Objective function for the minimum ES
    """

    return -(mean_ret @ weight) / (
        (pivot @ weight)
        .sort_values(ascending=True)
        .head(int(len(pivot @ weight) * sig))
        .mean()
    )
