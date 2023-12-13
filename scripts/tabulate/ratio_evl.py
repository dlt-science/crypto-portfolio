"""
Script to tabulate the ratio
"""

from environ.constants import TABLE_PATH
from environ.tabulate.latex_tab import gen_latex_tab
from scripts.process.process_ratio_evl import df_ratio_evl_latex

gen_latex_tab(
    df_ratio_evl_latex,
    TABLE_PATH / "ratio_evl.tex",
)
