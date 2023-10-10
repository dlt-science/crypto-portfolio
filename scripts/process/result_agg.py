"""
Script to aggregate the result
"""

from environ.process.boom_split import boom_split
from environ.process.optimization import freq_iterate
from scripts.process.preprocess_crypto_panel import df_crypto_processed
from scripts.process.sp_ret import sp_df

# a dict to store the result
dict_result = freq_iterate(df_crypto_processed)


# a dict to store the boom and bust periods
dict_boom_result, dict_bust_result = {}, {}

for strategy, strategy_info in dict_result.items():
    df_boom, df_bust = boom_split(strategy_info["ret"])
    dict_boom_result[strategy] = {
        "file_name": "mean_var_obj",
        "ret": df_boom,
    }
    dict_bust_result[strategy] = {
        "file_name": "mean_var_obj",
        "ret": df_bust,
    }

# a dict to store the benchmark
dict_benchmark = {
    "S&P": {
        "file_name": "sp",
        "ret": sp_df,
    }
}
