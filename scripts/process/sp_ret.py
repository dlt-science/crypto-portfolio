"""
Script to process the sp
"""
import pandas as pd

from scripts.process.sp import sp_df

# calculate the percentage return
sp_df["ret"] = sp_df["S&P"].pct_change()
sp_df["cum_ret"] = (1 + sp_df["ret"]).cumprod()

# drop the first row
sp_df = sp_df.dropna().reset_index(drop=True)

# convert the date in DD/MM/YYYY to datetime
sp_df["date"] = pd.to_datetime(sp_df["Date"], format="%d/%m/%Y")
sp_df.set_index("Date", inplace=True)
