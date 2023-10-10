"""
Script to aggregate the result
"""

from environ.process.boom_split import boom_split
from scripts.process.max_es_adj_sharpe import df_ret as df_ret_max_es_adj_sharpe
from scripts.process.max_es_adj_sharpe import df_wgt as df_wgt_max_es_adj_sharpe
from scripts.process.max_var_adj_sharpe import df_ret as df_ret_max_var_adj_sharpe
from scripts.process.max_var_adj_sharpe import df_wgt as df_wgt_max_var_adj_sharpe
from scripts.process.mean_var_opt import df_ret as df_ret_mean_var
from scripts.process.mean_var_opt import df_wgt as df_wgt_mean_var
from scripts.process.sp_ret import sp_df

# a dict to store the result
dict_result = {
    "Mean-variance": {
        "file_name": "mean_var",
        "ret": df_ret_mean_var,
        "wgt": df_wgt_mean_var,
    },
    "VaR-adj sharpe": {
        "file_name": "max_var_adj_sharpe",
        "ret": df_ret_max_var_adj_sharpe,
        "wgt": df_wgt_max_var_adj_sharpe,
    },
    "ES-adj sharpe": {
        "file_name": "max_es_adj_sharpe",
        "ret": df_ret_max_es_adj_sharpe,
        "wgt": df_wgt_max_es_adj_sharpe,
    },
}


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
