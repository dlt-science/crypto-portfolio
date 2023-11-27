"""
Functions to optimization
"""

from typing import Callable, Literal

import pandas as pd
import numpy as np
from scipy.optimize import minimize

from environ.constants import glob_con
from environ.process.mat_op import _panel_to_pivot, get_pivot_mean_cov_mat
from environ.process.obj_fuc import (max_es_adj_sharpe, max_var_adj_sharpe,
                                     mean_var_obj)
from environ.process.txn_fee import wealth
from scripts.process.preprocess_crypto_panel import date_list

SIG_LIST = [0.1, 0.05, 0.01]


def freq_iterate(
    df_crypto_processed: pd.DataFrame,
    cash_con: Literal["0.1", "0.33"] = "0.1",
    slow_medium_pct: list[float] = [1, 0],
) -> dict[str, dict[str, pd.DataFrame]]:
    """
    Function to iterate through the frequency
    """

    # a dict to store the common result
    dict_common = {
        "ret": pd.DataFrame(),
        "wgt": pd.DataFrame(),
        "wealth": pd.DataFrame(),
    }

    # a dict to store the result
    dict_result = {
        "Mean-variance": {
            "file_name": "mean_var",
            "type": "mean_var_opt",
            "opt_func": mean_var_obj,
            **dict_common,
        },
        "Mcap-weighted": {
            "file_name": "mcap_weighted",
            "type": "mcap_weighted",
            "opt_func": None,
            **dict_common,
        },
        "All-Bitcoin": {
            "file_name": "btc",
            "type": "buy_and_hold",
            "opt_func": None,
            **dict_common,
        },
        **{
            f"VaR-adj sharpe {sig}": {
                "file_name": f"max_var_adj_sharpe_{sig}",
                "type": "var_related_opt",
                "opt_func": max_var_adj_sharpe,
                "sig": sig,
                **dict_common,
            }
            for sig in SIG_LIST
        },
        **{
            f"ES-adj sharpe {sig}": {
                "file_name": f"max_es_adj_sharpe_{sig}",
                "type": "var_related_opt",
                "opt_func": max_es_adj_sharpe,
                "sig": sig,
                **dict_common,
            }
            for sig in SIG_LIST
        },
    }

    # iterate through the date list since the second quarter
    for q_idx in range(len(date_list) - 2):
        df_test = df_crypto_processed[
            (df_crypto_processed["date"] >= date_list[q_idx + 1])
            & (df_crypto_processed["date"] < date_list[q_idx + 2])
        ].copy()

        # a dict to store the weight of three frequency
        dict_signal = {
            "slow": {
                "start_date": date_list[q_idx]
            },
            "medium": {
                "start_date": date_list[q_idx] + pd.Timedelta(weeks=2)
            },
            "fast": {
                "start_date": date_list[q_idx] + pd.Timedelta(weeks=3)
            },
        }

        for _, strategy_info in dict_result.items():

            signal_wgt_lst = []

            for _, signal_info in dict_signal.items():
                df_train = df_crypto_processed[
                    (df_crypto_processed["date"] >= signal_info["start_date"])
                    & (df_crypto_processed["date"] < date_list[q_idx + 1])
                ].copy()
                # get the return and weight
                match strategy_info["type"]:
                    case "mean_var_opt":
                        wgt_df = mean_var_opt(
                            df_train,
                            date_list[q_idx + 1],
                            strategy_info["opt_func"],
                            cash_con
                        )

                    case "var_related_opt":
                        wgt_df = var_related_opt(
                            df_train,
                            date_list[q_idx + 1],
                            strategy_info["opt_func"],
                            strategy_info["sig"],
                            cash_con
                        )
                    case "mcap_weighted":
                        wgt_df = mcap_weighted(
                            df_train,
                            date_list[q_idx + 1],
                        )
                    case _:
                        wgt_df = buy_and_hold(
                            df_train,
                            date_list[q_idx + 1],
                        )
                signal_wgt_lst.append(wgt_df["weight"].tolist())

            signal_wgt_lst = np.array(signal_wgt_lst)
            signal_pct_lst = slow_medium_pct + [1 - sum(slow_medium_pct)]

            wgt = pd.DataFrame(
                {
                    "quarter": wgt_df["quarter"],
                    "name": wgt_df["name"],
                    "weight": signal_pct_lst @ signal_wgt_lst,
                }
            )

            # get the return
            df_test_pivot = _panel_to_pivot(df_test)
            ret = df_test_pivot @ wgt["weight"].tolist()

            # save the return
            ret = ret.reset_index().rename(columns={"index": "date",  # type: ignore
                                                    0:"ret"}).set_index("date")
            strategy_info["ret"] = pd.concat([
                strategy_info["ret"], 
                ret # type: ignore
])

            # save the weight
            strategy_info["wgt"] = pd.concat([strategy_info["wgt"], wgt]) # type: ignore

    for _, strategy_info in dict_result.items():
        # calculate the cumulative return
        strategy_info["ret"]["cum_ret"] = (strategy_info["ret"] + 1).cumprod()

        # calculate the wealth
        strategy_info["wealth"] = pd.DataFrame(wealth(
                    strategy_info["ret"],
                    strategy_info["wgt"],
                ))

    return dict_result

def buy_and_hold(
    df_train_q: pd.DataFrame,
    test_start_date: pd.Timestamp,
) -> pd.DataFrame:
    """
    Function to buy and hold one crypto
    """

    # get the mean return and covariance matrix
    df_crypto_processed_q_pivot, _, _ = get_pivot_mean_cov_mat(df_train_q)

    df_weight = {
        "quarter": [test_start_date for _ in range(len(df_crypto_processed_q_pivot.columns))],
        "name": df_crypto_processed_q_pivot.columns,
        "weight": [1] + [0 for _ in range(len(df_crypto_processed_q_pivot.columns) - 1)],
    }

    return pd.DataFrame(df_weight)

def mcap_weighted(
    df_train_q: pd.DataFrame,
    test_start_date: pd.Timestamp,
) -> pd.DataFrame:
    """
    Function to calculate the mcap weighted return
    """

    df_weight = {
        "quarter": [],
        "name": [],
        "weight": [],
    }

    df_last = df_train_q[df_train_q["date"] == df_train_q["date"].max()].copy()
    df_last["weight"] = df_last["mcap"] / df_last["mcap"].sum()

    # get the mean return and covariance matrix
    df_crypto_processed_q_pivot, _, _ = get_pivot_mean_cov_mat(df_train_q)

    for crypto_name in df_crypto_processed_q_pivot.columns:
        df_weight["quarter"].append(test_start_date)
        df_weight["name"].append(crypto_name)
        df_weight["weight"].append(df_last[df_last["name"] == crypto_name]["weight"].iloc[0])

    return pd.DataFrame(df_weight)



def var_related_opt(
    df_train_q: pd.DataFrame,
    test_start_date: pd.Timestamp,
    obj_fuc: Callable,
    sig: float,
    cash_con = Literal["0.1", "0.33"],
) -> pd.DataFrame:
    """
    Function to optimize VaR-related functions
    """

    # get the mean return and covariance matrix
    df_crypto_processed_q_pivot, mean_ret, _ = get_pivot_mean_cov_mat(df_train_q)

    # optimize the weight
    res = minimize(
        obj_fuc,
        # weight init
        # [0, 1] + [0 for _ in range(len(mean_ret) - 2)],
        # [1 / len(mean_ret) for _ in range(len(mean_ret))],
        [0.5, 0.3] + [0.2 / (len(mean_ret) - 2) for _ in range(len(mean_ret) - 2)],
        args=(df_crypto_processed_q_pivot, mean_ret, sig),
        constraints=glob_con[cash_con],
        bounds=[(0, 1) for _ in range(len(mean_ret))],
    )

    # return the return and weight
    return pd.DataFrame(
            {
            "quarter": [test_start_date for _ in range(len(df_crypto_processed_q_pivot.columns))],
            "name": df_crypto_processed_q_pivot.columns,
            "weight": res.x,
            }
        )


def mean_var_opt(
    df_train_q: pd.DataFrame,
    test_start_date: pd.Timestamp,
    obj_fuc: Callable,
    cash_con = Literal["0.1", "0.33"],
) -> pd.DataFrame:
    """
    Function to optimize mean-variance-related functions
    """

    # get the mean return and covariance matrix
    df_crypto_processed_q_pivot, mean_ret, cov_mat = get_pivot_mean_cov_mat(df_train_q)

    # optimize the weight
    res = minimize(
        obj_fuc,
        # weight init
        # [0, 1] + [0 for _ in range(len(mean_ret) - 2)],
        # [1 / len(mean_ret) for _ in range(len(mean_ret))],
        [0.5, 0.3] + [0.2 / len(mean_ret) for _ in range(len(mean_ret) - 2)],
        args=(mean_ret, cov_mat),
        constraints=glob_con[cash_con],
        bounds=[(0, 1) for _ in range(len(mean_ret))],
    )

    # return the return and weight
    return pd.DataFrame(
        {
            "quarter": [test_start_date for _ in range(len(df_crypto_processed_q_pivot.columns))],
            "name": df_crypto_processed_q_pivot.columns,
            "weight": res.x,
        }
    )
