"""
Functions to split the data into boom sample and bust sample
"""

import pandas as pd
from scripts.process.boom_bust import BOOM_BUST


def boom_split(df_res: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    """
    Function to split the data into boom sample and bust sample
    """

    df_boom = []
    df_bust = []

    for period in BOOM_BUST:
        if period["main_trend"] == "boom":
            df_boom.append(
                df_res[
                    (df_res["date"] >= period["start"])
                    & (df_res["date"] < period["end"])
                ]
            )

        if period["main_trend"] == "bust":
            df_bust.append(
                df_res[
                    (df_res["date"] >= period["start"])
                    & (df_res["date"] < period["end"])
                ]
            )

    return pd.concat(df_boom), pd.concat(df_bust)
