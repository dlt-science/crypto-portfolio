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


def tail_risk_opt(weight: np.ndarray, pivot: pd.DataFrame, sig: float) -> float:
    """
    Objective function for the minimum VaR
    """

    return (
        (pivot @ weight)
        .sort_values(ascending=True)
        .iloc[int(len(pivot @ weight) * sig)]
    )
