"""
Script to aggregate the result
"""

from scripts.process.mean_var_opt import (
    df_ret as df_ret_mean_var,
    df_wgt as df_wgt_mean_var,
)

from scripts.process.max_var_adj_sharpe import (
    df_ret as df_ret_max_var_adj_sharpe,
    df_wgt as df_wgt_max_var_adj_sharpe,
)

from scripts.process.max_es_adj_sharpe import (
    df_ret as df_ret_max_es_adj_sharpe,
    df_wgt as df_wgt_max_es_adj_sharpe,
)

# a dict to store the result
dict_result = {
    "Mean-variance": {
        "ret": df_ret_mean_var,
        "wgt": df_wgt_mean_var,
    },
    "VaR-adj sharpe": {
        "ret": df_ret_max_var_adj_sharpe,
        "wgt": df_wgt_max_var_adj_sharpe,
    },
    "ES-adj sharpe": {
        "ret": df_ret_max_es_adj_sharpe,
        "wgt": df_wgt_max_es_adj_sharpe,
    },
}
