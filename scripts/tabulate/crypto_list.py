"""
Script to tabulate the crypto list
"""

from environ.constants import TABLE_PATH
from scripts.process.clean_crypto_panel import df_crypto_without_missing_date

df_crypto_without_missing_date.sort_values("date", ascending=True)
crypto_list = (
    df_crypto_without_missing_date.groupby(["name", "symbol"])["date"]
    .min()
    .reset_index()
)
crypto_list["date"] = crypto_list["date"].dt.strftime("%Y-%m-%d")

save_path = TABLE_PATH / "crypto_list.tex"


with open(
    save_path,
    "w",
    encoding="utf-8",
) as f:
    f.write("\\begin{tabular}{" + "c" * 6 + "}\n")
    f.write("\\toprule\n")
    f.write("Crypto & Symbol & Date & Crypto & Symbol & Date" + "\\\\\n")
    f.write("\\midrule\n")

    for idx in range(len(crypto_list) // 2 + 1):
        row = crypto_list.iloc[2 * idx - 1]
        if idx == len(crypto_list) // 2:
            f.write(f"{row['name']} & {row['symbol']} & {row['date']} & & &" + "\\\\\n")
            break
        row2 = crypto_list.iloc[2 * idx]
        f.write(
            f"{row['name']} & {row['symbol']} & {row['date']} & {row2['name']} & {row2['symbol']} & {row2['date']}"
            + "\\\\\n"
        )
    f.write("\\bottomrule\n")
    f.write("\\end{tabular}\n")
