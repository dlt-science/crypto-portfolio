"""
Constratints for the optimization problem
"""

mean_var_con = (
    {
        "type": "eq",
        "fun": lambda weight: weight.sum() - 1,
    },
    {
        "type": "ineq",
        "fun": lambda weight: weight[0] - 2 * weight[2:].sum(),
    },
)
