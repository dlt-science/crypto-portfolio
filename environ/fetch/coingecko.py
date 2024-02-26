"""
Script to fetch data from CoinGecko API
"""

import time
from multiprocessing import Pool

import requests
from retry import retry
from tqdm import tqdm

from environ.constants import COINGECKO_API_KEY


class CoinGecko:
    """
    Class to fetch data from CoinGecko API
    """

    def __init__(self) -> None:
        pass

    def coins_list(self) -> list[dict[str, str]]:
        """
        Method to fetch the list of coins from CoinGecko API
        """
        url = "https://api.coingecko.com/api/v3/coins/list"
        response = requests.get(url, timeout=60)
        return response.json()

    @retry(delay=1, backoff=2, tries=3)
    def market_data(self, api_key: str, coin_id: str) -> dict:
        """
        Method to fetch the market data of a coin from CoinGecko API
        """
        url = (
            f"https://api.coingecko.com/api/v3/coins/{coin_id}"
            + "/market_chart?vs_currency=usd&days=max"
            + f"&x_cg_demo_api_key={api_key}"
        )
        response = requests.get(url, timeout=60)
        time.sleep(1)
        return response.json()


if __name__ == "__main__":
    cg = CoinGecko()
    coin_list = cg.coins_list()
    n_coin = 11

    start = time.time()
    for coin in coin_list[0:n_coin]:
        cg.market_data(COINGECKO_API_KEY[0], coin["id"])

    print(f"Time taken: {time.time() - start}")

    start = time.time()
    # distribute the api key to each process
    api_key_multi_list = []

    for idx, coin_id in enumerate(coin_list[0:n_coin]):
        api_key_multi_list.append(
            (coin_id, COINGECKO_API_KEY[idx % len(COINGECKO_API_KEY)])
        )

    with Pool(processes=15) as p:
        list(
            tqdm(p.starmap(cg.market_data, api_key_multi_list), desc="Processing data")
        )

    print(f"Time taken: {time.time() - start}")
