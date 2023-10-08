"""
Script to empirically test the mean-variance optimization
"""
import pandas as pd
from scipy.optimize import minimize

from environ.constants import glob_con
from environ.process.mat_op import _panel_to_pivot, get_pivot_mean_cov_mat
from environ.process.obj_fuc import tail_risk_opt
from scripts.process.preprocess_crypto_panel import date_list, df_crypto_processed

df_ret = pd.DataFrame()
df_wgt = pd.DataFrame()

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
        tail_risk_opt,
        # weight init
        # [0, 1] + [0 for _ in range(len(mean_ret) - 2)],
        [1 / len(mean_ret) for _ in range(len(mean_ret))],
        args=(df_crypto_processed_q_pivot, 0.1),
        constraints=glob_con,
        bounds=[(0, 1) for _ in range(len(mean_ret))],
    )

    # get the pivot table for the test set
    # test set might have some crypto that is not in the train set
    df_test_q = df_test_q[
        df_test_q["name"].isin(df_crypto_processed_q_pivot.columns)
    ].copy()
    df_test_q_pivot = _panel_to_pivot(df_test_q)

    # save the return
    df_ret = pd.concat([df_ret, df_test_q_pivot @ res.x])

    # save the weight
    df_wgt = pd.concat(
        [
            df_wgt,
            pd.DataFrame(
                {
                    "quarter": [date_list[q_idx + 1] for _ in range(3)],
                    "name": ["Bitcoin", "Caash", "Others"],
                    "weight": list(res.x[:2]) + [res.x[2:].sum()],
                }
            ),
        ]
    )

# calculate the cumulative return
df_ret = df_ret.rename(columns={0: "ret"})
df_ret["cum_ret"] = (df_ret["ret"] + 1).cumprod()
