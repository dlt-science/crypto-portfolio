"""
Script to aggregate the result
"""

import pandas as pd

from environ.process.optimization import freq_iterate
from scripts.process.preprocess_crypto_panel import date_list, df_crypto_processed
from scripts.process.sp_ret import sp_df

# a dict to store the result
dict_result = freq_iterate(df_crypto_processed)

# add the benchmark
dict_result_with_benchmark = dict_result.copy()

sp_q_df = {
    "date": [],
    "ret": [],
}
df_btc_q = {
    "date": [],
    "ret": [],
}

df_btc = df_crypto_processed[df_crypto_processed["symbol"] == "BTC"].copy()

# convert the sp_df to quarterly return
for idx in range(len(date_list) - 1):
    date = date_list[idx]
    date_next = date_list[idx + 1]
    sp_ret = sp_df.loc[(sp_df["date"] >= date) & (sp_df["date"] < date_next), "ret"]
    btc_ret = df_btc.loc[(df_btc["date"] >= date) & (df_btc["date"] < date_next), "ret"]

    if len(sp_ret) != 0:
        sp_q_df["date"].append(date)
        sp_q_df["ret"].append((sp_ret + 1).cumprod().iloc[-1] - 1)

    if len(btc_ret) != 0:
        df_btc_q["date"].append(date)
        df_btc_q["ret"].append((btc_ret + 1).cumprod().iloc[-1] - 1)

sp_q_df = pd.DataFrame(sp_q_df)
df_btc_q = pd.DataFrame(df_btc_q)

df_btc["cum_ret"] = (df_btc["ret"] + 1).cumprod()
df_btc_q["cum_ret"] = (df_btc_q["ret"] + 1).cumprod()
sp_q_df["cum_ret"] = (sp_q_df["ret"] + 1).cumprod()

dict_result_with_benchmark["S&P"] = {
    "file_name": "sp500",
    "type": "benchmark",
    "ret": sp_df,
    "q_ret": sp_q_df,
}

# isolate the BTC
dict_result_with_benchmark["BTC"] = {
    "file_name": "btc",
    "type": "benchmark",
    "ret": df_btc,
    "q_ret": df_btc_q,
}
