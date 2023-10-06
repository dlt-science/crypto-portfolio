"""
Objective functions for optimization
"""

import numpy as np


# define the objective function
def mean_var_obj(weight: np.ndarray, mean_ret: np.ndarray, cov_mat: np.ndarray):
    """
    Objective function for the mean-variance optimization
    """

    # maximize the sharpe ratio
    return -((mean_ret @ weight) / np.sqrt(weight @ cov_mat @ weight))
