"""
Script to visualize the weight
"""

import matplotlib.pyplot as plt

from scripts.process.mean_var_opt import df_wgt

# plot the weight
plt.figure(figsize=(12, 8))

plt.stackplot(
    df_wgt["quarter"].unique(),
    *[
        df_wgt[df_wgt["name"] == name]["weight"]
        for name in ["Bitcoin", "Caash", "Others"]
    ],
    labels=["Bitcoin", "Cash", "Others"],
)

plt.legend()

plt.show()
