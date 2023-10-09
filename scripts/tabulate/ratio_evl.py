"""
Script to tabulate the ratio
"""

from environ.process.pfm_evl import cal_sharpe, cal_sortino
from environ.constants import TABLE_PATH
from scripts.process.result_agg import dict_result


# save the latex table
with open(
    TABLE_PATH / "ratio_evl.tex",
    "w",
    encoding="utf-8",
) as f:
    f.write("\\begin{tabular}{l" + "c" * len(dict_result.keys()) + "}\n")
    f.write("\\toprule\n")
    f.write("Ratio & " + " & ".join(dict_result.keys()) + "\\\\\n")
    f.write("\\midrule\n")
    f.write(
        "Sharpe Ratio & "
        + " & ".join(
            [f"{cal_sharpe(value['ret']):.4f}" for _, value in dict_result.items()]
        )
        + "\\\\\n"
    )
    f.write(
        "Sortino Ratio & "
        + " & ".join(
            [f"{cal_sortino(value['ret']):.4f}" for _, value in dict_result.items()]
        )
        + "\\\\\n"
    )
    f.write("\\bottomrule\n")
    f.write("\\end{tabular}\n")
