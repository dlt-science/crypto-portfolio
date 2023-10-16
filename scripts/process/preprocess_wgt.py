"""
Script to preprocess the weights in results
"""

import pandas as pd

from environ.process.boom_split import boom_check
from scripts.process.result_agg import dict_result

PLOT_DICT = {
    "whole": {},
    "boom": {},
    "bust": {},
}

for strategy, strategy_info in dict_result.items():
    for period in ["whole", "boom", "bust"]:
        PLOT_DICT[period][strategy] = pd.DataFrame()

    PLOT_DICT["whole"][strategy] = dict_result[strategy]["wgt"]

    for idx, row in strategy_info["wgt"].iterrows():
        if boom_check(row["quarter"]) == "boom":
            PLOT_DICT["boom"][strategy] = pd.concat(
                [PLOT_DICT["boom"][strategy], row.to_frame().T]
            )

        if boom_check(row["quarter"]) == "bust":
            PLOT_DICT["bust"][strategy] = pd.concat(
                [PLOT_DICT["bust"][strategy], row.to_frame().T]
            )

    for period in ["whole", "boom", "bust"]:
        # convert the date to datetime
        PLOT_DICT[period][strategy]["quarter"] = pd.to_datetime(
            PLOT_DICT[period][strategy]["quarter"]
        ).dt.to_period("Q")
