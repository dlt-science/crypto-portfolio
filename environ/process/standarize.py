"""
Script to standardize the process
"""

import pandas as pd


def min_max_scaler(df: pd.DataFrame) -> pd.DataFrame:
    """
    Function to standardize the dataframe using min max scaler
    """
    for col in df.columns:
        df[col] = (df[col] - df[col].min()) / (df[col].max() - df[col].min())

    return df
