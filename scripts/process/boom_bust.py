"""
plot market with boom bust cycles
"""

from environ.process.boom_calculator import boom_bust_periods
from scripts.process.preprocess_crypto_panel import min_date
from scripts.process.sp import sp_df

sp_df["time"] = sp_df["Date"]
sp_df = sp_df.loc[sp_df["Date"] >= min_date]

# replace s&p colume with price
sp_df = sp_df.rename(columns={"S&P": "price"})

BOOM_BUST = boom_bust_periods(sp_df)
