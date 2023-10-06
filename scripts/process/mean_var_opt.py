"""
Script to empirically test the mean-variance optimization
"""
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy.optimize import minimize

from environ.process.mat_op import get_pivot_mean_cov_mat
from environ.process.obj_fuc import mean_var_obj
from environ.process.constraint import mean_var_con
from scripts.process.preprocess_crypto_panel import date_list, df_crypto_processed

RES_DICT = {
    "date": [],
    "protfolio_ret": [],
}

# iterate through the date list since the second quarter
for q_idx in range(len(date_list) - 1):
    # isolate the data for the quarter
    q_start = date_list[q_idx] + pd.Timedelta(days=1)
    q_end = date_list[q_idx + 1]
    df_crypto_processed_q = df_crypto_processed[
        (df_crypto_processed["date"] >= q_start)
        & (df_crypto_processed["date"] <= q_end)
    ].copy()

    # get the mean return and covariance matrix
    df_crypto_processed_q_pivot, mean_ret, cov_mat = get_pivot_mean_cov_mat(
        df_crypto_processed_q
    )

    # initialize the weight
    weight_init = np.ones(len(mean_ret)) / len(mean_ret)

    # optimize the weight
    res = minimize(
        mean_var_obj,
        weight_init,
        args=(mean_ret, cov_mat),
        constraints=mean_var_con,
        bounds=[(0, 1) for _ in range(len(mean_ret))],
    )

    # save the result
    RES_DICT["date"].append(df_crypto_processed_q["date"].iloc[-1])
    RES_DICT["protfolio_ret"].append(df_crypto_processed_q_pivot.iloc[-1] @ res.x)

# convert the result to dataframe
df_res = pd.DataFrame(RES_DICT)

# cumulate the return
df_res["protfolio_ret_cum"] = (1 + df_res["protfolio_ret"]).cumprod()

# plot the result
plt.plot(df_res["date"], df_res["protfolio_ret_cum"])
