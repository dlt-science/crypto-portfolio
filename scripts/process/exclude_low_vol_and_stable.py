"""
Scripts to remove low volume crypto and stablecoin from the list
"""

import json
import os

from environ.constants import (
    LOW_VOL_LIST,
    PROCESSED_DATA_PATH,
    DATA_PATH,
    STABLE_COIN_LIST,
)

# a dict to store the results
res_dict = {}

# load the json file
with open(DATA_PATH / "swiss_quote" / "crypto_lst.json", "r", encoding="utf-8") as f:
    data = json.load(f)

# iterate over the data
for crypto, crypto_info in data.items():
    # if the crypto is not in the low vol list and not in the stable coin list
    if crypto not in LOW_VOL_LIST and crypto not in STABLE_COIN_LIST:
        # add the crypto to the res_dict
        res_dict[crypto] = crypto_info

# check whether the processed data path exists
if not (PROCESSED_DATA_PATH / "swiss_quote").exists():
    # if not, create the path
    os.makedirs(PROCESSED_DATA_PATH / "swiss_quote")

# save the res_dict to a json file
with open(
    PROCESSED_DATA_PATH / "swiss_quote" / "crypto_lst_exclude_low_vol_and_stable.json",
    "w",
    encoding="utf-8",
) as f:
    json.dump(res_dict, f, indent=4)
