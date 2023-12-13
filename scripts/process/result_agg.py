"""
Script to aggregate the result
"""

from environ.process.ema_filter import ema_filter
from environ.process.optimization import freq_iterate
from environ.process.txn_fee import wealth_daily
from scripts.process.preprocess_crypto_panel import df_crypto_processed

dict_result = {}

for cash_con in ["0.33", "0.1"]:
    dict_result[cash_con] = {}
    for freq in ["weekly", "monthly", "quarterly"]:
        dict_result[cash_con][freq] = freq_iterate(
            df_crypto_processed,
            cash_con=cash_con,
            freq=freq,  # type: ignore
        )
        for strategy, strategy_info in dict_result[cash_con][freq].items():
            # use the ema filter for wealth
            dict_result[cash_con][freq][strategy]["wealth"]["wealth_ema"] = ema_filter(
                dict_result[cash_con][freq][strategy]["wealth"]
                .set_index("date")["wealth"]
                .tolist()
            )

            # calculate the daily wealth
            dict_result[cash_con][freq][strategy]["wealth_daily"] = wealth_daily(
                strategy_info
            )
            dict_result[cash_con][freq][strategy]["wealth_daily"][
                "wealth_ema"
            ] = ema_filter(
                dict_result[cash_con][freq][strategy]["wealth_daily"][
                    "wealth_daily"
                ].tolist()
            )

            # calculate the return for the wealth
            dict_result[cash_con][freq][strategy]["wealth_daily"]["wealth_ret"] = (
                dict_result[cash_con][freq][strategy]["wealth_daily"]["wealth_daily"]
                .pct_change()
                .dropna()
            )


# add the benchmark
dict_result_with_benchmark = dict_result.copy()
