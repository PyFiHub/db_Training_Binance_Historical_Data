# Libraries

import requests
import pandas as pd
import numpy as np
import logging
from binance.client import Client
import sqlite3
#from api_keys import api_key, api_secret

api_key = "" #not required
api_secret = "" #not required

# Binance Client
client = Client(api_key, api_secret)

# Logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
if not logger.hasHandlers():
    handler = logging.StreamHandler()
    formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
    handler.setFormatter(formatter)
    logger.addHandler(handler)

# Functions
def convert_to_float(data):
    # Convert formats to floats 
    columns = ["open", "high", "low", "close", "volume", "num_trades"]
    for col in columns:
        data[col] = data[col].astype(float)
    return data

def get_trading_pairs():
    # Screen available pairs - Using USDT pairs.
    try:
        info = client.get_exchange_info()
        return [symbol["symbol"] for symbol in info["symbols"] 
        if symbol["status"] == "TRADING" 
        and "USDT" in symbol["symbol"] 
        and "UPUSDT" not in symbol["symbol"] 
        and "DOWNUSDT" not in symbol["symbol"]]
    except Exception as e:
        logger.error(f"Error retrieving trading pairs: {e}")
        return []

def get_historical_data(symbol, latest_timestamp=None, interval="1d", limit=1000):
    klines = client.get_historical_klines(symbol, interval, limit=limit)
    data = pd.DataFrame(klines, columns=["open_time", "open", "high", "low", "close", "volume", "close_time", "quote_volume", "num_trades", "taker_buy_base_volume", "taker_buy_quote_volume", "ignore"])
    data = data.drop(["quote_volume","taker_buy_base_volume", "taker_buy_quote_volume", "ignore"], axis=1)
    data = convert_to_float(data)
    data["open_time"] = pd.to_datetime(data["open_time"], unit='ms')
    data["close_time"] = pd.to_datetime(data["close_time"], unit='ms')

    if latest_timestamp:
        data = data[data["open_time"] > latest_timestamp]

    return data

def create_table(c, pair):
    # Create a table for each pair - Adding prefix to avoid issue with token/coin starting with integers
    table_name = "pair_" + pair
    c.execute(f'''CREATE TABLE IF NOT EXISTS {table_name} (
        open_time TIMESTAMP,
        open REAL,
        high REAL,
        low REAL,
        close REAL,
        volume REAL,
        close_time TIMESTAMP,
        num_trades INTEGER
    )''')

    
trading_pairs = get_trading_pairs()

if trading_pairs:
    with sqlite3.connect('trading_data.db') as conn:
        c = conn.cursor()
        for pair in trading_pairs:
            create_table(c, pair)
            try:
                table_name = "pair_" + pair
                c.execute(f"SELECT MAX(open_time) FROM {table_name}")
                latest_timestamp = c.fetchone()[0]
                if latest_timestamp:
                    latest_timestamp = pd.to_datetime(latest_timestamp)
                
                data = get_historical_data(pair, latest_timestamp)
                if not data.empty:
                    data.to_sql(table_name, conn, if_exists='append', index=False)
                    rows_added = len(data)
                    logger.info(f"Adding trading pair: {pair} - Rows added: {rows_added}")
                else:
                    logger.info(f"Adding trading pair: {pair} - No new rows added")
            except Exception as e:
                logger.error(f"Error retrieving data for {pair}: {e}")