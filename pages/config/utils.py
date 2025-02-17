import datetime

import pandas as pd
import streamlit as st

from backend.services.backend_api_client import BackendAPIClient
from CONFIG import BACKEND_API_HOST, BACKEND_API_PORT


def get_max_records(days_to_download: int, interval: str) -> int:
    conversion = {"s": 1 / 60, "m": 1, "h": 60, "d": 1440}
    unit = interval[-1]
    quantity = int(interval[:-1])
    return int(days_to_download * 24 * 60 / (quantity * conversion[unit]))


@st.cache_data
def get_candles(connector_name="binance", trading_pair="BTC-USDT", interval="1m", days=7):
    backend_client = BackendAPIClient(BACKEND_API_HOST, BACKEND_API_PORT)
    end_time = datetime.datetime.now() - datetime.timedelta(minutes=15)
    start_time = end_time - datetime.timedelta(days=days)

    df = pd.DataFrame(backend_client.get_historical_candles(connector_name, trading_pair, interval,
                                                            start_time=int(start_time.timestamp()),
                                                            end_time=int(end_time.timestamp())))
    df.index = pd.to_datetime(df.timestamp, unit='s')
    return df

@staticmethod
def ai_signals() -> int:
    external_sig = external_signal().strip().lower()
    print(f"External signal is {external_sig}")
    if external_sig == "buy":
        return 1
    if external_sig == "sell":
        return -1

    return 0

@staticmethod
def combine_signals(original: int) -> int:
    external_sig = external_signal().strip().lower()
    print(f"External signal is {external_sig} and original is {original}")
    if external_sig == "buy" and original == 1:
        return 1
    if external_sig == "sell" and original == -1:
        return -1

    return 0

@staticmethod
def external_signal():
    import time
    signal = 0
    with open("/home/hummingbot/data/signals.txt", "r") as f:
        try:
            signal = f.read()
        finally:
            time.sleep(1)
        return signal
