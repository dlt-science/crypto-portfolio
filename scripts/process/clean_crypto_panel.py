"""
Script to clean the crypto data
"""

import pandas as pd

from scripts.process.merge_crypto_panel import df_crypto


# convert the timestamp to datetime
df_crypto.sort_values(["name", "timestamp"], ascending=True, inplace=True)
df_crypto["date"] = pd.to_datetime(df_crypto["timestamp"], unit="ms")
df_crypto["date"] = df_crypto["date"].dt.strftime("%Y-%m-%d")
df_crypto.drop_duplicates(subset=["name", "date"], inplace=True, keep="first")
df_crypto.drop(columns=["timestamp"], inplace=True)
df_crypto["date"] = pd.to_datetime(df_crypto["date"])

# ffill the missing date
df_crypto_without_missing_date = []
for crypto_name in df_crypto["name"].unique():
    df_certain_crypto = df_crypto[df_crypto["name"] == crypto_name].copy()
    df_certain_crypto_timestamp_range = pd.date_range(
        df_certain_crypto["date"].min(),
        df_certain_crypto["date"].max(),
        freq="D",
    )
    df_certain_crypto = df_certain_crypto.set_index("date").reindex(
        df_certain_crypto_timestamp_range
    )

    df_certain_crypto = df_certain_crypto.ffill().reset_index()
    df_crypto_without_missing_date.append(df_certain_crypto)
df_crypto_without_missing_date = pd.concat(df_crypto_without_missing_date)
df_crypto_without_missing_date = df_crypto_without_missing_date.rename(
    columns={"index": "date"}
)
