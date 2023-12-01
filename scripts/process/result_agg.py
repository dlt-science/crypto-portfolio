"""
Script to aggregate the result
"""

from environ.process.optimization import freq_iterate
from scripts.process.preprocess_crypto_panel import df_crypto_processed

dict_result = {}

for cash_con in ["0.33", "0.1"]:
    dict_result[cash_con] = {}
    for freq in ["weekly", "montly", "quarterly"]:
        dict_result[cash_con][freq] = freq_iterate(
            df_crypto_processed,
            cash_con="0.33",
            freq=freq,  # type: ignore
        )

# add the benchmark
dict_result_with_benchmark = dict_result.copy()
