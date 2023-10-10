"""
Functions to generate LaTeX tables
"""

from pathlib import Path
from typing import Union

import pandas as pd


def gen_latex_tab(df_res: pd.DataFrame, save_path: Union[str, Path]) -> None:
    """
    Function to generate LaTeX table using the key as key,
    first column as index, and the rest as columns
    """

    with open(
        save_path,
        "w",
        encoding="utf-8",
    ) as f:
        f.write("\\begin{tabular}{l" + "c" * len(df_res.keys()) + "}\n")
        f.write("\\toprule\n")
        f.write("Ratio & " + " & ".join(df_res.keys()) + "\\\\\n")
        f.write("\\midrule\n")
        for idx, row in df_res.iterrows():
            f.write(
                f"{idx} & " + " & ".join([f"{value:.4f}" for value in row]) + "\\\\\n"
            )
        f.write("\\bottomrule\n")
        f.write("\\end{tabular}\n")
