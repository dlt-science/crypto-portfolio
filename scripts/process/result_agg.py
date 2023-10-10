"""
Script to aggregate the result
"""

from environ.process.optimization import freq_iterate
from scripts.process.preprocess_crypto_panel import df_crypto_processed
from scripts.process.sp_ret import sp_df

# a dict to store the result
dict_result = freq_iterate(df_crypto_processed)

# add the benchmark
dict_result["S\&P"] = {
    "file_name": "sp500",
    "type": "benchmark",
    "ret": sp_df,
}
dict_result["BTC"] = {
    "file_name": "btc",
    "type": "benchmark",
    "ret": df_crypto_processed[df_crypto_processed["symbol"] == "BTC"].copy(),
}
