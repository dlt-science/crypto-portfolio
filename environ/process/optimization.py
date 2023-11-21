"""
Functions to optimization
"""

from typing import Callable

import pandas as pd
from scipy.optimize import minimize

from environ.constants import INITIAL_WEALTH, TRANSACTION_COST, glob_con
from environ.process.mat_op import _panel_to_pivot, get_pivot_mean_cov_mat
from environ.process.obj_fuc import (max_es_adj_sharpe, max_var_adj_sharpe,
                                     mean_var_obj)
from scripts.process.preprocess_crypto_panel import date_list

SIG_LIST = [0.1, 0.05, 0.01]


def freq_iterate(
    df_crypto_processed: pd.DataFrame,
) -> dict[str, dict[str, pd.DataFrame]]:
    """
    Function to iterate through the frequency
    """

    # a dict to store the common result
    dict_common = {
        "ret": pd.DataFrame(),
        "wgt": pd.DataFrame(),
        "q_ret": pd.DataFrame(),
    }

    # a dict to store the result
    dict_result = {
        "Mean-variance": {
            "file_name": "mean_var",
            "type": "mean_var_opt",
            "opt_func": mean_var_obj,
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
        # isolate the data for the quarter
        df_train_q = df_crypto_processed[
            (df_crypto_processed["date"] >= date_list[q_idx] + pd.Timedelta(days=1))
            & (df_crypto_processed["date"] <= date_list[q_idx + 1])
        ].copy()

        df_test_q = df_crypto_processed[
            (df_crypto_processed["date"] >= date_list[q_idx + 1] + pd.Timedelta(days=1))
            & (df_crypto_processed["date"] <= date_list[q_idx + 2])
        ].copy()

        for _, strategy_info in dict_result.items():
            # get the return and weight
            match strategy_info["type"]:
                case "mean_var_opt":
                    ret, wgt = mean_var_opt(
                        df_train_q,
                        df_test_q,
                        date_list[q_idx + 1] + pd.Timedelta(days=1),
                        strategy_info["opt_func"],
                    )

                case "var_related_opt":
                    ret, wgt = var_related_opt(
                        df_train_q,
                        df_test_q,
                        date_list[q_idx + 1] + pd.Timedelta(days=1),
                        strategy_info["opt_func"],
                        strategy_info["sig"]
                    )

            ret = ret.reset_index().rename(columns={"index": "date", 0:"ret"}).set_index("date")

            # save the return
            strategy_info["ret"] = pd.concat([strategy_info["ret"], ret])

            # save the weight
            strategy_info["wgt"] = pd.concat([strategy_info["wgt"], wgt])

    # calculate the cumulative return
    for _, strategy_info in dict_result.items():

        # a dataframe to store the investment value
        investment_value_df = pd.DataFrame(
            {
                "date": [strategy_info["ret"].index[0]],
                "investment_value": [INITIAL_WEALTH],
            }
        )     

        # get the pivot table for the wgt
        df_wgt = strategy_info["wgt"]
        df_wgt_pivot = df_wgt.pivot(index="quarter", columns="name", values="weight").drop(columns="Cash")
        df_ret = strategy_info["ret"].reset_index().rename(columns={"index": "date"})


        # iterate throught the df_wgt_pivot
        for idx in range(len(df_wgt_pivot)-1):

            # get the date for the idx
            date = df_wgt_pivot.index[idx]
            date_next = df_wgt_pivot.index[idx + 1]

            # get the weight
            wgt = df_wgt_pivot.loc[date]
            wgt_next = df_wgt_pivot.loc[date_next]

            # get the investment value before the period
            investment_value_before = (
                investment_value_df.iloc[-1]["investment_value"]
            )
            # get the investment value after the period before transaction cost
            investment_value_after = (
                investment_value_before * (df_ret.loc[(df_ret["date"] >= date) & (df_ret["date"] < date_next), "ret"] + 1).cumprod().iloc[-1]
            )

            # get the transaction cost
            transaction_cost = (
                abs(wgt_next * investment_value_after - wgt * investment_value_before).sum() * TRANSACTION_COST
            )

            # get the investment value after the period after transaction cost
            investment_value_after = investment_value_after - transaction_cost

            # calculate the quarter return
            strategy_info["q_ret"] = pd.concat(
                [
                    strategy_info["q_ret"],
                    pd.DataFrame(
                        {
                            "date": date,
                            "ret": [(investment_value_after - investment_value_before) / investment_value_before],
                        }
                    ),
                ]
            )

            # append the investment value
            investment_value_df = pd.concat(
                [
                    investment_value_df,
                    pd.DataFrame(
                        {
                            "date": date,
                            "investment_value": [investment_value_after],
                        }
                    ),
                ]
            )


        strategy_info["ret"] = (strategy_info["ret"]
                                .reset_index()
                                .rename(columns={"index": "date"})
        )
        # calculate the cumulative return
        strategy_info["ret"]["cum_ret"] = (strategy_info["ret"]["ret"] + 1).cumprod()
        strategy_info["q_ret"]["cum_ret"] = (strategy_info["q_ret"]["ret"] + 1).cumprod()

    return dict_result


def var_related_opt(
    df_train_q: pd.DataFrame,
    df_test_q: pd.DataFrame,
    test_start_date: pd.Timestamp,
    obj_fuc: Callable,
    sig: float,
) -> tuple[pd.DataFrame, pd.DataFrame]:
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
        constraints=glob_con,
        bounds=[(0, 1) for _ in range(len(mean_ret))],
    )

    # get the pivot table for the test set
    # test set might have some crypto that is not in the train set
    df_test_q = df_test_q[
        df_test_q["name"].isin(df_crypto_processed_q_pivot.columns)
    ].copy()
    df_test_q_pivot = _panel_to_pivot(df_test_q)

    # return the return and weight
    return (
        df_test_q_pivot @ res.x,
        pd.DataFrame(
            {
                "quarter": [test_start_date for _ in range(len(df_crypto_processed_q_pivot.columns))],
                "name": df_crypto_processed_q_pivot.columns,
                "weight": res.x,
            }
        ),
    )


def mean_var_opt(
    df_train_q: pd.DataFrame,
    df_test_q: pd.DataFrame,
    test_start_date: pd.Timestamp,
    obj_fuc: Callable,
) -> tuple[pd.DataFrame, pd.DataFrame]:
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
        constraints=glob_con,
        bounds=[(0, 1) for _ in range(len(mean_ret))],
    )

    # get the pivot table for the test set
    # test set might have some crypto that is not in the train set
    df_test_q = df_test_q[
        df_test_q["name"].isin(df_crypto_processed_q_pivot.columns)
    ].copy()
    df_test_q_pivot = _panel_to_pivot(df_test_q)

    # return the return and weight
    return df_test_q_pivot @ res.x, pd.DataFrame(
        {
            "quarter": [test_start_date for _ in range(len(df_crypto_processed_q_pivot.columns))],
            "name": df_crypto_processed_q_pivot.columns,
            "weight": res.x,
        }
    )
