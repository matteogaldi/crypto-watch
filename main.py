import signal
from sys import exit

import gas_price_watcher


def handler(signal_received, frame):
    print("Exiting...")
    exit(0)


if __name__ == '__main__':
    signal.signal(signal.SIGINT, handler)
    gas_price_watcher.start(gas_limit=21000)
    while True:
        print("Type get to get current gas price \n")
        a = input()
        if a == "get":
            print(round(gas_price_watcher.usd_transaction_price, 3))
        elif a == "quit":
            exit(0)
