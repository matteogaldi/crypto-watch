from datetime import datetime
import os
import threading
import time

import requests
from pycoingecko import CoinGeckoAPI
from dotenv import load_dotenv

import database_connection

load_dotenv()
cg = CoinGeckoAPI()

usd_unit_gas_price = 0
usd_transaction_price = 0


def watch_gas_price():
    global usd_unit_gas_price
    while True:
        api_endpoint = os.environ.get("GAS_NOW_API_ENDPOINT")
        response = requests.request("GET", api_endpoint).json()['data']['slow']
        usd_unit_gas_price = response / (10 ** 18)
        time.sleep(0.5)


def watch_transaction_price(gas_limit):
    global usd_transaction_price
    while True:
        eth_usd_price = cg.get_price(ids=['ethereum'], vs_currencies='usd')
        usd_price = eth_usd_price["ethereum"]["usd"] * usd_unit_gas_price * gas_limit
        if usd_price != usd_transaction_price:
            usd_transaction_price = usd_price
            database_connection.save_data(collection="gasPrice",
                                          data={"date": datetime.now().isoformat(),
                                                "price": round(usd_transaction_price, 8)})
        time.sleep(0.5)


def start(gas_limit):
    t1 = threading.Thread(target=watch_gas_price, daemon=True)
    t2 = threading.Thread(target=watch_transaction_price, args=(gas_limit,), daemon=True)
    t1.start()
    t2.start()
