"""
Script to empirically test the minimum-variance optimization
"""
import pandas as pd
from scipy.optimize import minimize

from environ.constants import glob_con
from environ.process.mat_op import _panel_to_pivot, get_pivot_mean_cov_mat
from environ.process.obj_fuc import min_var_obj
from scripts.process.preprocess_crypto_panel import date_list, df_crypto_processed

df_res = pd.DataFrame()

# iterate through the date list since the second quarter
for q_idx in range(len(date_list) - 2):
    # isolate the data for the quarter
    df_train_q = df_crypto_processed[
        (df_crypto_processed["date"] >= date_list[q_idx] + pd.Timedelta(days=1))
        & (df_crypto_processed["date"] <= date_list[q_idx + 1])
    ].copy()

    df_test_q = df_crypto_processed[
        (df_crypto_processed["date"] >= date_list[q_idx + 1] + pd.Timedelta(days=1))
        & (df_crypto_processed["date"] <= date_list[q_idx + 2])
    ].copy()

    # get the mean return and covariance matrix
    df_crypto_processed_q_pivot, mean_ret, cov_mat = get_pivot_mean_cov_mat(df_train_q)

    # optimize the weight
    res = minimize(
        min_var_obj,
        # weight init
        [0, 1] + [0 for _ in range(len(mean_ret) - 2)],
        args=(cov_mat),
        constraints=glob_con,
        bounds=[(0, 1) for _ in range(len(mean_ret))],
    )

    # get the pivot table for the test set
    # test set might have some crypto that is not in the train set
    df_test_q = df_test_q[
        df_test_q["name"].isin(df_crypto_processed_q_pivot.columns)
    ].copy()
    df_test_q_pivot = _panel_to_pivot(df_test_q)

    # save the result
    df_res = pd.concat([df_res, df_test_q_pivot @ res.x])
