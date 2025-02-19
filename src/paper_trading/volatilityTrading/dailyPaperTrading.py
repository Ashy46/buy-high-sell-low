import requests
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import time
import schedule
import asyncio

def fetch_current_btc_price():
    url = "https://data-api.cryptocompare.com/spot/v1/latest/tick?market=coinbase&instruments=BTC-USD&apply_mapping=true"
    parametrs = {
        "apikey": "e604cdac25f2a3ef56a7c901baf17b76c7e9a67fd6953904211150f99b0ffecf",
        "limit": 1
    }
    response = requests.get(url, params=parametrs)
    data = response.json()
    return data['Data']['BTC-USD']['PRICE']

def past_10_days_bitcoin():
    url = "https://data-api.cryptocompare.com/spot/v1/historical/days?market=coinbase&instrument=BTC-USD&limit=10&aggregate=1&fill=true&apply"
    parametrs = {
        "apikey": "e604cdac25f2a3ef56a7c901baf17b76c7e9a67fd6953904211150f99b0ffecf",
    }
    response = requests.get(url, params=parametrs)
    data = response.json()
    df = pd.DataFrame([{'Open': data['Data'][i]['OPEN']} for i in range(10)])
    df = pd.concat([df, pd.DataFrame([{'Close': data['Data'][i]['CLOSE']} for i in range(10)])], axis=1)
    df = pd.concat([df, pd.DataFrame([{'High': data['Data'][i]['HIGH']} for i in range(10)])], axis=1)
    df = pd.concat([df, pd.DataFrame([{'Low': data['Data'][i]['LOW']} for i in range(10)])], axis=1)
    return df

def calculate_volatility():
    df = past_10_days_bitcoin()
    std = np.std(df['Open'])
    return std

async def daily_paper_trading():
    open_position = {}

    while True:
        current_btc_price = fetch_current_btc_price()
        std = calculate_volatility()
        print(f"Current BTC price: {current_btc_price}")
        print(f"Volatility: {std}")
        upper_band = current_btc_price + 5 * std
        lower_band = current_btc_price - std

        total_positions = 0
        for key, position in open_position.items():
            total_positions += len(position)

        if total_positions <= 10 and lower_band <= current_btc_price <= upper_band:
            print(f"Position Taken: {current_btc_price}")
            key = lower_band, upper_band
            if key not in open_position:
                open_position[key] = []
            open_position[key].append(current_btc_price)
            with open("volatilityTrading/bitcoin_tracking.txt", "a") as file:
                file.write(f"{key}: {current_btc_price} at {datetime.now()}\n")
        
        for key, position in open_position.items():
            lb, ub = key
            if current_btc_price >= ub:
                for i in position:
                    print(f"Position Closed: {i}")
                    print(f"Profit: {i - current_btc_price}")
                    with open("volatilityTrading/bitcoin_tracking.txt", "a") as file:
                        file.write(f"{key}: {i} at {datetime.now()}\n")
                        file.write(f"Profit: {i - current_btc_price}\n")
                open_position[key] = []
            elif current_btc_price <= lb - 8 * std:
                for i in position:
                    print(f"Position Closed: {i}")
                    print(f"Loss: {lb - 8 * std - i}")
                    with open("bitcoin_tracking.txt", "a") as file:
                        file.write(f"{key}: {i} at {datetime.now()}\n")
                        file.write(f"Loss: {lb - 8 * std - i}\n")
                open_position[key] = []
    
        await asyncio.sleep(3600)

daily_paper_trading()

