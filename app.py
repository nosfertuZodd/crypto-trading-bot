from flask import Flask, jsonify, request
from binance import Client
from requests.exceptions import Timeout
from flask_cors import CORS
from binance.exceptions import BinanceAPIException
import requests
import pandas as pd
import datetime, time
import json

# Initiaizaing a Flask app
app = Flask(__name__)
CORS(app)

api_key = 'R1abV976W7rcTLAAQJpD0NVT9UyWoe6LBCAJj93750Y26Kso1j3lEB6n2rVDuxyo'
api_secret = 'FU00rdJZd0wpxLWbca4AFAVlYmMbkon9Nzddpy2DNe2kkimSazAXvArUnqYyHOuI'
taapi_api = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJjbHVlIjoiNjA4NzExNGM0MjI0NmNlM2IwY2U1ZWUzIiwiaWF0IjoxNzIxNDE2ODU3LCJleHAiOjMzMjI1ODgwODU3fQ.i3Mon47Geg_zIZV2sMl8JlFvFJSQruMua6oyLAp7Ebk'
client = Client(api_key, api_secret, testnet=True)

@app.route('/symbols', methods=['GET'])
def get_symbols():
    try:
        exchange_info = client.get_exchange_info()
        symbols = [s['symbol'] for s in exchange_info['symbols']]
        return jsonify({'symbols': symbols})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/candlestick_data_since2023', methods=['GET'])
def get_candlestick_data():
    untilThisDate = datetime.datetime(2023, 2, 1)
    
    # Start from January 1st, 2023
    sinceThisDate = datetime.datetime(2023, 1, 1)
    
    # Query parameters (symbol, interval)
    symbol = request.args.get('symbol', default='BTCUSDT', type=str)
    interval = request.args.get('interval', default=Client.KLINE_INTERVAL_5MINUTE, type=str)
    
    all_data = []  # List to hold all the fetched data
    
    try:
        print(sinceThisDate)
        # Loop through and fetch all data in batches of 1000 (Binance API limit)
        while sinceThisDate < untilThisDate:
            print(f"Fetching data starting from: {sinceThisDate}")  # Log the starting point
            
            # Fetch historical candlestick data
            candlesticks = client.get_historical_klines(symbol=symbol, 
                                                        interval=interval, 
                                                        start_str=str(sinceThisDate), 
                                                        end_str=str(untilThisDate), 
                                                        limit=5000)
            
            if not candlesticks:
                print("No more data available")
                break  # Stop the loop if no more data is returned
            
            # Append the fetched data to the all_data list
            all_data.extend(candlesticks)
            print(f"Fetched {len(candlesticks)} records")  # Log number of records fetched
            
            # Update the sinceThisDate to the time of the last returned candlestick
            last_candle_time = candlesticks[-1][0]  # Get the time of the last returned candlestick
            sinceThisDate = datetime.datetime.fromtimestamp(last_candle_time / 1000)  # Convert to datetime
            print(f"New sinceThisDate: {sinceThisDate}")
        
        # Convert the data into a DataFrame
        df = pd.DataFrame(all_data, columns=['dateTime', 'open', 'high', 'low', 'close', 'volume', 'closeTime', 'quoteAssetVolume', 'numberOfTrades', 'takerBuyBaseVol', 'takerBuyQuoteVol', 'ignore'])
        
        # Convert timestamp to readable datetime format
        df['dateTime'] = pd.to_datetime(df['dateTime'], unit='ms').dt.strftime('%Y-%m-%d %H:%M:%S')
        
        # Set dateTime as index
        df.set_index('dateTime', inplace=True)

        # Drop unnecessary columns
        df.drop(['closeTime', 'quoteAssetVolume', 'numberOfTrades', 'takerBuyBaseVol', 'takerBuyQuoteVol', 'ignore'], axis=1, inplace=True)
        
        # Save the DataFrame as CSV
        df.to_csv('BTC-USDT-Jan2023-Onwards.csv')
        
        return jsonify({'message': 'Candlestick data has been saved successfully!'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

    
indicators = [
                       [ {'indicator': 'rsi', 'period': 14},
                        {'indicator': 'stoch', 'k_period': 14, 'd_period': 3, 'smooth_k': 3},
                        {'indicator': 'cci', 'period': 20},
                        {'indicator': 'ao'},
                        {'indicator': 'adx', 'period': 14},
                        {'indicator': 'mom', 'period': 10},
                        {'indicator': 'macd', 'fast_period': 12, 'slow_period': 26, 'signal_period': 9},
                        {'indicator': 'stochrsi', 'rsi_period': 14, 'stoch_k_period': 3, 'stoch_d_period': 3, 'stoch_d_smooth': 3},
                        {'indicator': 'willr', 'period': 14},
                        {'indicator': 'ultosc', 'short_period': 7, 'medium_period': 14, 'long_period': 20} ],                       # {'indicator': 'ema', 'period': 10},
                       [{'indicator': 'sma', 'period': 10},
                        {'indicator': 'ema', 'period': 20},
                        {'indicator': 'sma', 'period': 20},
                        {'indicator': 'ema', 'period': 30},
                        {'indicator': 'sma', 'period': 30},
                        {'indicator': 'ema', 'period': 50},
                        {'indicator': 'sma', 'period': 50},
                        {'indicator': 'ema', 'period': 100},
                        {'indicator': 'sma', 'period': 100},
                        {'indicator': 'ema', 'period': 200},
                        {'indicator': 'sma', 'period': 200},
                        {'indicator': 'ichimoku', 'period': 26},  # Ichimoku Base Line period
                        {'indicator': 'vwma', 'period': 20},  # Volume Weighted Moving Average period
                        {'indicator': 'hma', 'period': 9}
                    ]
                    ]

@app.route('/indicators', methods=['POST'])
def get_indicators():
    responses = []
    symbol = request.json.get('symbol', 'BTC/USDT')
    interval = request.json.get('interval', '1d')
    url = 'https://api.taapi.io/bulk'
    for indicator in indicators:
        payload = {
            'secret': taapi_api,
            'construct': [
                {
                    'exchange': 'binance',
                    'symbol': symbol,
                    'interval': interval,
                    'indicators': indicator
                }
            ]
        }
        try:
            response = requests.post(url, json=payload)
            if response.status_code == 200:
                responses.extend(response.json()['data'])
            else:
                return jsonify({'error': 'Error from taapi.io', 'status_code': response.status_code}), 500    
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    return jsonify({'data': responses})
 

@app.route('/buy', methods=['POST'])
def buy_order():
    symbol = request.json.get('symbol', 'BTCUSDT')
    quantity = request.json.get('quantity', 0.001)

    try:
        order = client.create_order(
            symbol=symbol,
            side=Client.SIDE_BUY,
            type=Client.ORDER_TYPE_MARKET,
            quantity=quantity
        )
        return jsonify(order)
    except BinanceAPIException as e:
        return jsonify({'error': str(e)}), 500
    
@app.route('/sell', methods=['POST'])
def sell_order():
    symbol = request.json.get('symbol', 'BTCUSDT')
    quantity = request.json.get('quantity', 0.001)

    try:
        order = client.create_order(
            symbol=symbol,
            side=Client.SIDE_SELL,
            type = Client.ORDER_TYPE_MARKET,
            quantity=quantity
        )
        return jsonify(order)
    except BinanceAPIException as e:
        return jsonify({'error': str(e)}), 500

@app.route('/compare_predictions', methods=['GET'])
def compare_predictions():
    symbol = 'BTCUSDT'
    interval = Client.KLINE_INTERVAL_15MINUTE
    limit = 15  # Fetch the last 15 minutes of candlestick data
    
    try:
        # Fetch actual close prices from Binance
        candlesticks = client.get_klines(symbol=symbol, interval=interval, limit=limit)
        actual_close_prices = [float(c[4]) for c in candlesticks]
        
        # Get predicted close prices
        predicted_close_prices = get_prediction(symbol, interval)
        
        # Calculate error metrics
        mae = np.mean(np.abs(np.array(actual_close_prices) - np.array(predicted_close_prices)))
        mse = np.mean((np.array(actual_close_prices) - np.array(predicted_close_prices)) ** 2)
        rmse = np.sqrt(mse)
        mape = np.mean(np.abs((np.array(actual_close_prices) - np.array(predicted_close_prices)) / np.array(actual_close_prices))) * 100
        
        # Return comparison results
        comparison = {
            'actual_close_prices': actual_close_prices,
            'predicted_close_prices': predicted_close_prices,
            'mae': mae,
            'mse': mse,
            'rmse': rmse,
            'mape': mape
        }
        return jsonify(comparison)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

import numpy as np
import pandas as pd
from binance.client import Client
from datetime import datetime, timedelta

# Define the function to get predictions

def compare_predictions():
    symbol = 'BTCUSDT'
    interval = Client.KLINE_INTERVAL_15MINUTE
    limit = 15  # Fetch the last 15 minutes of candlestick data
    
    try:
        # Fetch actual close prices from Binance
        candlesticks = client.get_klines(symbol=symbol, interval=interval, limit=limit)
        actual_close_prices = [float(c[4]) for c in candlesticks]
        
        # Get predicted close prices
        predicted_close_prices = get_prediction(symbol, interval)
        
        # Calculate error metrics
        mae = np.mean(np.abs(np.array(actual_close_prices) - np.array(predicted_close_prices)))
        mse = np.mean((np.array(actual_close_prices) - np.array(predicted_close_prices)) ** 2)
        rmse = np.sqrt(mse)
        mape = np.mean(np.abs((np.array(actual_close_prices) - np.array(predicted_close_prices)) / np.array(actual_close_prices))) * 100
        
        # Return comparison results
        comparison = {
            'actual_close_prices': actual_close_prices,
            'predicted_close_prices': predicted_close_prices,
            'mae': mae,
            'mse': mse,
            'rmse': rmse,
            'mape': mape
        }
        return jsonify(comparison)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)