"""
Script to calculate boom and bust periods of a given price.
"""

import logging
from typing import Union

import numpy as np
import pandas as pd

logging.basicConfig(level=logging.INFO)


def boom_bust_one_period(
    time_price: pd.DataFrame, boom_change: float = 0.3, bust_change: float = 0.3
) -> dict:
    """
    Return the boom and bust periods of the given price.

    Args:
        time_price (pd.DataFrame): A DataFrame containing price and time columns.
        boom_change (float): The percentage change required for a price boom.
        bust_change (float): The percentage change required for a price bust.

    Returns:
        dict: A dictionary containing the main trend, start time, and end time of the period.
    """
    if len(time_price) == 0:
        raise ValueError("Input DataFrame is empty.")

    if "price" not in time_price.columns or "time" not in time_price.columns:
        raise ValueError("Input DataFrame missing required columns.")

    boom_threshold = time_price["price"][0] * (1 + boom_change)
    bust_threshold = time_price["price"][0] * (1 - bust_change)

    boom = np.where(time_price["price"] > boom_threshold)[0]
    bust = np.where(time_price["price"] < bust_threshold)[0]

    cycle = {
        "main_trend": "none",
        "start": time_price["time"].iloc[0],
        "end": time_price["time"].iloc[-1],
    }

    if len(boom) == len(bust) == 0:
        return cycle

    if len(boom) == 0 or (len(bust) > 0 and bust[0] < boom[0]):
        cycle["main_trend"] = "bust"
        cycle_end = bust[0] - 1
        while (
            cycle_end + 1 < len(time_price["price"])
            and time_price["price"][cycle_end + 1] < time_price["price"][cycle_end]
        ):
            cycle_end += 1
    else:
        cycle["main_trend"] = "boom"
        cycle_end = boom[0] - 1
        while (
            cycle_end + 1 < len(time_price["price"])
            and time_price["price"][cycle_end + 1] > time_price["price"][cycle_end]
        ):
            cycle_end += 1

    cycle["end"] = time_price["time"][cycle_end]

    price_array = time_price["price"].iloc[: cycle_end + 1]

    cycle["pre_trend_end"] = time_price["time"][
        price_array.idxmin() if cycle["main_trend"] == "boom" else price_array.idxmax()
    ]

    return cycle


def boom_bust_periods(
    time_price: pd.DataFrame, boom_change: float = 0.3, bust_change: float = 0.3
) -> list:
    """
    Function to calculate the boom and bust periods of a given price.
    """
    boom_bust_list = []
    # Sort the time_price dataframe by time
    time_price = time_price.sort_values(by="time").reset_index(drop=True)
    end = time_price["time"][0]
    previous_trend = "none"
    while end < time_price["time"].iloc[-1]:
        time_price = time_price[time_price["time"] >= end].reset_index(drop=True)
        cycle_dict = boom_bust_one_period(time_price, boom_change, bust_change)
        if cycle_dict["main_trend"] != "none" and previous_trend != "none":
            if cycle_dict["main_trend"] == previous_trend:
                boom_bust_list[-1]["end"] = cycle_dict["end"]
            else:
                if "pre_trend_end" in cycle_dict:
                    boom_bust_list[-1]["end"] = cycle_dict["pre_trend_end"]
                    boom_bust_list.append(
                        {
                            "main_trend": cycle_dict["main_trend"],
                            "start": cycle_dict["pre_trend_end"],
                            "end": cycle_dict["end"],
                        }
                    )
                else:
                    boom_bust_list.append(
                        {
                            "main_trend": cycle_dict["main_trend"],
                            "start": end,
                            "end": cycle_dict["end"],
                        }
                    )
        else:
            boom_bust_list.append(
                {
                    "main_trend": cycle_dict["main_trend"],
                    "start": end,
                    "end": cycle_dict["end"],
                }
            )
        end = cycle_dict["end"]
        previous_trend = cycle_dict["main_trend"]
    return boom_bust_list


# allow time to be both integer and pandas._libs.tslibs.timestamps.Timestamp
def is_boom(boom_bust_list: list, time: Union[int, pd.Timestamp]) -> bool:
    """
    determine if the given time is in a boom period
    """
    for i in boom_bust_list:
        if i["main_trend"] == "boom" and i["start"] <= time <= i["end"]:
            return True
    return False


if __name__ == "__main__":
    price = pd.DataFrame(
        {
            "time": [
                200,
                300,
                400,
                500,
                600,
                700,
                800,
                900,
                1000,
                1100,
                1200,
            ],
            "price": [
                9,
                10,
                29,
                2,
                69,
                10,
                2,
                69,
                120,
                6,
                7,
            ],
        }
    )

    periods = boom_bust_periods(price)

    # plot the price with the boom bust periods
    import matplotlib.pyplot as plt

    # sort the price by time
    price = price.sort_values(by="time").reset_index(drop=True)

    plt.plot(price["time"], price["price"])

    # plot boom as green and bust as red
    for i in periods:
        if i["main_trend"] == "boom":
            plt.axvspan(i["start"], i["end"], color="green", alpha=0.5)
        elif i["main_trend"] == "bust":
            plt.axvspan(i["start"], i["end"], color="red", alpha=0.5)
