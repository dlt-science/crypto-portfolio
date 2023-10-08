"""
Script to evaluate the performance
"""

from environ.process.pfm_evl import cal_sharpe
from scripts.process.max_var_adj_sharpe import df_ret

# calculate the sharpe ratio
print(f"Sharpe ratio for the optimized portfolio: {cal_sharpe(df_ret):.4f}")
