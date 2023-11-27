"""
Script to aggregate the result
"""

from environ.process.optimization import freq_iterate
from scripts.process.preprocess_crypto_panel import df_crypto_processed

# a dict to store the result
dict_result = freq_iterate(df_crypto_processed, cash_con="0.33")

# add the benchmark
dict_result_with_benchmark = dict_result.copy()
