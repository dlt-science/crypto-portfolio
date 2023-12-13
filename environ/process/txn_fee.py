"""
Functions to calculate transaction fee and adjust the return
"""

from typing import Literal

import pandas as pd

from environ.constants import INITIAL_WEALTH, TRANSACTION_COST

def wealth_daily(strategy_info: dict[str, pd.DataFrame]) -> pd.DataFrame:
    """
    Function to calculate the daily wealth
    """

    df_wealth = strategy_info["wealth"].copy()
    df_ret = strategy_info["ret"].copy()
    df_wealth_daily = pd.DataFrame()

    for idx, date in enumerate(df_wealth["date"].unique()):
        wealth = df_wealth.loc[df_wealth["date"] == date, 'wealth'].values[0]
        if idx != len(df_wealth) - 1:
            df_ret_period = df_ret.loc[(df_ret.index >= date) & (df_ret.index < df_wealth["date"].unique()[idx + 1])].copy()
        else:
            df_ret_period = df_ret.loc[(df_ret.index >= date)].copy()

        df_ret_period["ret"] = df_ret_period["ret"].shift(1).fillna(0)

        df_ret_period["wealth_daily"] = (df_ret_period["ret"] + 1).cumprod() * wealth
        
        df_wealth_daily = pd.concat([df_wealth_daily, 
                                     df_ret_period[["wealth_daily"]]])

    return df_wealth_daily

def wealth(
    ret_df: pd.DataFrame,
    wgt_df: pd.DataFrame,
    freq: Literal["weekly", "monthly", "quarterly"] = "quarterly",
    initial_wealth: float = INITIAL_WEALTH,
    transaction_cost_rate: float = TRANSACTION_COST,
) -> dict[str, list[str | float]]:
    """
    Function to calculate the wealth dynamics
    """

    ret_df.index = pd.to_datetime(ret_df.index)
    wgt_df["quarter"] = pd.to_datetime(wgt_df["quarter"])

    date_list = sorted(wgt_df["quarter"].unique().tolist())

    wgt_df_without_cash = wgt_df[wgt_df["name"] != "Cash"].copy()
    wgt_df_without_cash.sort_values(["quarter", "name"], inplace=True)

    wealth_dict = {
        "date": [],
        "wealth": [],
    }

    for idx, date in enumerate(date_list):
        wealth_dict["date"].append(date)

        wgt_vec_without_cash = wgt_df_without_cash.loc[
            wgt_df_without_cash["quarter"] == date, "weight"
        ]

        if idx == 0:
            # open position
            wealth_dict["wealth"].append(
                initial_wealth
                - initial_wealth
                * wgt_vec_without_cash.sum()  # type: ignore
                * transaction_cost_rate
            )
        else:
            investment_value_before_ret = wealth_dict["wealth"][-1]

            if idx == len(date_list) - 1:
                # close position
                cum_ret = (
                    ret_df.loc[
                        (ret_df.index >= date),
                        "ret",
                    ]
                    + 1
                ).prod() - 1  # type: ignore
                investment_value_after_ret_before_fee = investment_value_before_ret * (
                    cum_ret + 1
                )
                wealth_dict["wealth"].append(
                    investment_value_after_ret_before_fee
                    - investment_value_after_ret_before_fee
                    * wgt_vec_without_cash.sum()  # type: ignore
                    * transaction_cost_rate
                )

            else:
                # rebalance
                match freq:
                    case "quarterly":
                        cum_ret = (
                            ret_df.loc[
                                (ret_df.index >= date - pd.DateOffset(months=3))
                                & (ret_df.index < date),
                                "ret",
                            ]
                            + 1
                        ).prod() - 1  # type: ignore
                    case "monthly":
                        cum_ret = (
                            ret_df.loc[
                                (ret_df.index >= date - pd.DateOffset(months=1))
                                & (ret_df.index < date),
                                "ret",
                            ]
                            + 1
                        ).prod() - 1  # type: ignore
                    case _:
                        cum_ret = (
                            ret_df.loc[
                                (ret_df.index >= date - pd.DateOffset(days=7))
                                & (ret_df.index < date),
                                "ret",
                            ]
                            + 1
                        ).prod() - 1  # type: ignore


                investment_value_after_ret_before_fee = investment_value_before_ret * (
                    cum_ret + 1
                )
                wgt_vec_without_cash_next = wgt_df_without_cash.loc[
                    wgt_df_without_cash["quarter"] == date_list[idx + 1], "weight"
                ]
                investment_value_after_fee = (
                    investment_value_after_ret_before_fee
                    - investment_value_after_ret_before_fee
                    * (
                        abs(
                            wgt_vec_without_cash_next.values  # type: ignore
                            - wgt_vec_without_cash.values  # type: ignore
                        ).sum()
                        * transaction_cost_rate
                    )
                )
                wealth_dict["wealth"].append(investment_value_after_fee)

    return wealth_dict


if __name__ == "__main__":
    RET_TEST = pd.DataFrame(
        {"ret": [1, 1, 1]},
        index=["2000-01-01", "2000-04-01", "2000-07-01"],
    ).rename_axis("date")

    WGT_TEST = pd.DataFrame(
        {
            "quarter": [
                "2000-01-01",
                "2000-04-01",
                "2000-07-01",
                "2000-01-01",
                "2000-04-01",
                "2000-07-01",
            ],
            "name": ["Cash", "Cash", "Cash", "BTC", "BTC", "BTC"],
            "weight": [0.5, 0.6, 0.7, 0.5, 0.4, 0.3],
        }
    )

    print(wealth(RET_TEST, WGT_TEST))
