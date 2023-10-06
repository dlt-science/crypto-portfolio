"""
Functions for matrix operations
"""

import pandas as pd

from environ.constants import ASSET_CLASSES


def _panel_to_pivot(
    df_panel: pd.DataFrame,
    index: str = "date",
    columns: str = "name",
    value: str = "ret",
) -> pd.DataFrame:
    """
    Function to convert the panel data to the pivot table
    """

    df_panel = df_panel.pivot(index=index, columns=columns, values=value).dropna(axis=1)

    return df_panel[
        ASSET_CLASSES[:2] + [_ for _ in df_panel.columns if _ not in ASSET_CLASSES[:2]]
    ]


def _get_cov_mat(df_pivot: pd.DataFrame) -> pd.DataFrame:
    """
    Function to calculate the covariance matrix with Bitcoin and Cash in the 1st and 2nd position
    """

    cov_mat = df_pivot.cov()
    right_order_lst = ASSET_CLASSES[:2] + [
        _ for _ in cov_mat.columns if _ not in ASSET_CLASSES[:2]
    ]

    return cov_mat[right_order_lst].reindex(index=right_order_lst)


def _get_mean_ret(df_pivot: pd.DataFrame) -> pd.Series:
    """
    Function to calculate the mean return with Bitcoin and Cash in the 1st and 2nd position
    """

    mean_ret = df_pivot.mean()
    mean_ret = mean_ret[
        ASSET_CLASSES[:2] + [_ for _ in mean_ret.index if _ not in ASSET_CLASSES[:2]]
    ]

    return mean_ret


def get_pivot_mean_cov_mat(
    df_panel: pd.DataFrame,
) -> tuple[pd.DataFrame, pd.Series, pd.DataFrame]:
    """
    Function to generate the mean return and covariance matrix
    """

    df_pivot = _panel_to_pivot(df_panel)

    return df_pivot, _get_mean_ret(df_pivot), _get_cov_mat(df_pivot)
