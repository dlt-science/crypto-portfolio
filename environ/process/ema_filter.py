"""
Function to calculate the exponential moving average of a signal
"""


def ema_filter(signal: list[float]) -> list[float]:
    """
    Function to calculate the exponential moving average of a signal
    """

    # iterate through the signal
    ema = []

    # initialize the first value
    ema.append(signal[0])

    # iterate through the signal
    for idx, val in enumerate(signal[1:]):
        k = 2 / (idx + 3)
        ema.append(k * val + (1 - k) * ema[idx])

    return ema


if __name__ == "__main__":
    print(ema_filter([1, 2, 3, 4]))
