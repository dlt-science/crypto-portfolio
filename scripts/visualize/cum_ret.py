"""
Script to visualize the cumulative return
"""

import matplotlib.pyplot as plt
from scripts.process.pfm_evl import df_ret

# plot the cumulative return
plt.figure(figsize=(12, 8))

df_ret["cum_ret"].plot()

plt.show()
