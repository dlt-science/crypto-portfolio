"""
Script to preprocess the crypto data
"""
import pandas as pd

from scripts.process.clean_crypto_panel import df_crypto_without_missing_date

# add cash to the panel
df_crypto_without_missing_date = pd.concat(
    [
        df_crypto_without_missing_date,
        pd.DataFrame(
            {
                "date": pd.date_range(
                    df_crypto_without_missing_date["date"].min(),
                    df_crypto_without_missing_date["date"].max(),
                    freq="D",
                ),
                "name": "Cash",
                "symbol": "Cash",
                "price": 1,
            }
        ),
    ]
)

# calculate the daily return
df_crypto_without_missing_date = df_crypto_without_missing_date.sort_values(
    ["name", "date"]
)
df_crypto_without_missing_date["ret"] = df_crypto_without_missing_date.groupby("name")[
    "price"
].pct_change()
df_crypto_without_missing_date.dropna(inplace=True)

# get the min date of the panel
min_date = df_crypto_without_missing_date["date"].min()
max_date = df_crypto_without_missing_date["date"].max()
date_list = pd.date_range(min_date, max_date, freq="Q").tolist()
df_crypto_without_missing_date["quarter"] = df_crypto_without_missing_date["date"].isin(
    date_list
)

# finish data preprocessing
df_crypto_processed = df_crypto_without_missing_date.copy()
