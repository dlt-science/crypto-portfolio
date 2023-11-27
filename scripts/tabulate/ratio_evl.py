"""
Script to tabulate the ratio
"""

from environ.constants import TABLE_PATH
from environ.tabulate.latex_tab import gen_latex_tab
from scripts.process.process_ratio_evl import ratio_evl_dict

# generate latex table for the whole sample
for period_name, period_info in ratio_evl_dict.items():
    gen_latex_tab(
        period_info,
        TABLE_PATH / f"{period_name}_ratio_evl_0.33.tex",
    )
