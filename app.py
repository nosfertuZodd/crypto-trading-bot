import os
import logging
from flask import Flask, jsonify, request
from binance.client import Client
from binance.exceptions import BinanceAPIException
from flask_cors import CORS
from flasgger import Swagger
import requests
import pandas as pd
import datetime
import time
import numpy as np


# Initialize Flask app and CORS
app = Flask(__name__)
CORS(app)
swagger = Swagger(app, template_file='swagger.yaml')

# Load API keys from environment variables for security
API_KEY = 'R1abV976W7rcTLAAQJpD0NVT9UyWoe6LBCAJj93750Y26Kso1j3lEB6n2rVDuxyo'
API_SECRET = 'FU00rdJZd0wpxLWbca4AFAVlYmMbkon9Nzddpy2DNe2kkimSazAXvArUnqYyHOuI'
TAAPI_API_KEY = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJjbHVlIjoiNjc1MDZkYzI4YTIzODE2NDA3NTVhYjA5IiwiaWF0IjoxNzMzMzI0NDEzLCJleHAiOjMzMjM3Nzg4NDEzfQ.6ZiwhhdexNyeCRvFur0xT1RM1fxPNtQj-46KuiiAtug'

# Set up logging for better visibility
logging.basicConfig(level=logging.INFO)

# Initialize Binance client
client = Client(API_KEY, API_SECRET)

# Define the available indicators (as per your earlier code)
indicators = [
    [
        {'indicator': 'rsi', 'period': 14},
        {'indicator': 'stoch', 'k_period': 14, 'd_period': 3, 'smooth_k': 3},
        {'indicator': 'cci', 'period': 20},
        {'indicator': 'ao'},
        {'indicator': 'adx', 'period': 14},
        {'indicator': 'mom', 'period': 10},
        {'indicator': 'macd', 'fast_period': 12, 'slow_period': 26, 'signal_period': 9},
        {'indicator': 'stochrsi', 'rsi_period': 14, 'stoch_k_period': 3, 'stoch_d_period': 3, 'stoch_d_smooth': 3},
        {'indicator': 'willr', 'period': 14},
        {'indicator': 'ultosc', 'short_period': 7, 'medium_period': 14, 'long_period': 20}
    ],
    [
        {'indicator': 'sma', 'period': 10},
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
        {'indicator': 'ichimoku', 'period': 26},
        {'indicator': 'vwma', 'period': 20},
        {'indicator': 'hma', 'period': 9}
    ]
]

# Helper function to call the TAAPI API
def get_indicator_data(symbol, interval, indicator):
    url = 'https://api.taapi.io/rsi?secret=API_KEY&exchange=binance&symbol=BTC/USDT&interval=1h'
    payload = {
        'secret': 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJjbHVlIjoiNjc1MDZkYzI4YTIzODE2NDA3NTVhYjA5IiwiaWF0IjoxNzMzMzI0NDEzLCJleHAiOjMzMjM3Nzg4NDEzfQ.6ZiwhhdexNyeCRvFur0xT1RM1fxPNtQj',
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
        response.raise_for_status()
        return response.json()['data']
    except requests.exceptions.RequestException as e:
        logging.error(f"Error fetching indicators: {e}")
        return None

def make_prediction(indicators):
    buy_count = 0
    sell_count = 0
    strong_buy_count = 0
    strong_sell_count = 0

    # Example: If RSI < 30, it's a strong buy signal
    if 'rsi' in indicators and indicators['rsi'] < 30:
        strong_buy_count += 1

    # Example: If RSI > 70, it's a strong sell signal
    if 'rsi' in indicators and indicators['rsi'] > 70:
        strong_sell_count += 1

    # Example: MACD crossover
    if 'macd' in indicators:
        if indicators['macd']['histogram'] > 0:
            buy_count += 1
        else:
            sell_count += 1

    # Decision rules:
    if strong_buy_count >= 2:
        return 'Strong Buy'
    elif strong_sell_count >= 2:
        return 'Strong Sell'
    elif buy_count >= 4:
        return 'Buy'
    elif sell_count >= 3:
        return 'Sell'
    else:
        return 'Hold'  # No clear decision



# Helper function to make a buy order
def place_order(symbol, quantity, side):
    try:
        order = client.create_order(
            symbol=symbol,
            side=side,
            type=Client.ORDER_TYPE_MARKET,
            quantity=quantity
        )
        return order
    except BinanceAPIException as e:
        logging.error(f"Error placing order: {str(e)}")
        return None

# Endpoint to fetch available symbols
@app.route('/symbols', methods=['GET'])
def get_symbols():
    try:
        exchange_info = client.get_exchange_info()
        symbols = [s['symbol'] for s in exchange_info['symbols']]
        return jsonify({'symbols': symbols})
    except Exception as e:
        logging.error(f"Error fetching symbols: {str(e)}")
        return jsonify({'error': 'Failed to fetch symbols'}), 500


@app.route('/indicators/custom', methods=['POST'])
def get_custom_indicators():
    # Get the selected indicators from the user's request
    user_indicators = request.json.get('indicators', [])
    symbol = request.json.get('symbol', 'BTC/USDT')
    interval = request.json.get('interval', '1m')
    
    if not user_indicators:
        return jsonify({'error': 'Please provide at least one indicator.'}), 400

    # Prepare the payload for the TAAPI.io API request
    payload = {
        'secret': 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJjbHVlIjoiNjc1MDZkYzI4YTIzODE2NDA3NTVhYjA5IiwiaWF0IjoxNzMzMzI0NDEzLCJleHAiOjMzMjM3Nzg4NDEzfQ.6ZiwhhdexNyeCRvFur0xT1RM1fxPNtQj-46KuiiAtug',
        'construct': [
            {
                'exchange': 'binance',
                'symbol': symbol,
                'interval': interval,
                'indicators': user_indicators
            }
        ]
    }

    try:
        response = requests.post('https://api.taapi.io/bulk', json=payload)
        if response.status_code == 200:
            # Parse the response and extract the indicator values
            indicators = response.json().get('data', {})
            
            # Call the decision-making function
            prediction = make_prediction(indicators)
            
            return jsonify({
                'indicators': indicators,
                'prediction': prediction
            })
        else:
            return jsonify({'error': 'Error from TAAPI.io', 'status_code': response.status_code}), 500
    except Exception as e:
        return jsonify({'error': str(e)}), 500



# Endpoint to fetch candlestick data from Binance
@app.route('/candlestick_data_since2023', methods=['GET'])
def get_candlestick_data():
    symbol = request.args.get('symbol', default='BTCUSDT', type=str)
    interval = request.args.get('interval', default=Client.KLINE_INTERVAL_5MINUTE, type=str)
    since_date = datetime.datetime(2023, 1, 1)
    until_date = datetime.datetime(2023, 2, 1)

    all_data = []
    try:
        while since_date < until_date:
            candlesticks = client.get_historical_klines(
                symbol=symbol,
                interval=interval,
                start_str=str(since_date),
                end_str=str(until_date),
                limit=5000
            )
            all_data.extend(candlesticks)
            last_candle_time = candlesticks[-1][0]
            since_date = datetime.datetime.fromtimestamp(last_candle_time / 1000)
        
        df = pd.DataFrame(all_data, columns=[
            'dateTime', 'open', 'high', 'low', 'close', 'volume', 'closeTime',
            'quoteAssetVolume', 'numberOfTrades', 'takerBuyBaseVol', 'takerBuyQuoteVol', 'ignore'
        ])
        df['dateTime'] = pd.to_datetime(df['dateTime'], unit='ms').dt.strftime('%Y-%m-%d %H:%M:%S')
        df.set_index('dateTime', inplace=True)
        df.drop(['closeTime', 'quoteAssetVolume', 'numberOfTrades', 'takerBuyBaseVol', 'takerBuyQuoteVol', 'ignore'], axis=1, inplace=True)
        df.to_csv('candlestick_data.csv')
        return jsonify({'message': 'Candlestick data saved successfully'}), 200
    except Exception as e:
        logging.error(f"Error fetching candlestick data: {str(e)}")
        return jsonify({'error': 'Failed to fetch candlestick data'}), 500

# Endpoint to fetch indicator data
@app.route('/indicators', methods=['POST'])
def get_indicators():
    symbol = request.json.get('symbol', 'BTCUSDT')
    interval = request.json.get('interval', '1h')
    responses = []

    for indicator_group in indicators:
        for indicator in indicator_group:
            indicator_data = get_indicator_data(symbol, interval, indicator)
            if indicator_data:
                responses.append({'indicator': indicator, 'data': indicator_data})
    
    if not responses:
        return jsonify({'error': 'Failed to fetch indicator data'}), 500

    return jsonify({'data': responses})

# Endpoint to place a buy order
@app.route('/buy', methods=['POST'])
def buy_order():
    try:
        symbol = request.json.get('symbol', 'BTCUSDT')
        quantity = request.json.get('quantity', 0.001)
        order = place_order(symbol, quantity, Client.SIDE_BUY)
        if order:
            return jsonify(order), 200
        return jsonify({'error': 'Failed to place buy order'}), 500
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Endpoint to place a sell order
@app.route('/sell', methods=['POST'])
def sell_order():
    symbol = request.json.get('symbol', 'BTCUSDT')
    quantity = request.json.get('quantity', 0.001)

    order = place_order(symbol, quantity, Client.SIDE_SELL)
    if order:
        return jsonify(order)
    return jsonify({'error': 'Failed to place sell order'}), 500


# Endpoint to compare predictions and actual data
@app.route('/compare_predictions', methods=['POST'])
def compare_predictions():
    symbol = request.json.get('symbol', 'BTCUSDT')
    interval = request.json.get('interval', '15m')
    limit = request.json.get('limit', 15)

    # Fetch actual data
    actual_data = client.get_klines(symbol=symbol, interval=interval, limit=limit)
    actual_close_prices = [float(candle[4]) for candle in actual_data]

    # You can implement prediction logic here. For now, we simulate predicted data:
    predicted_close_prices = [price * 1.01 for price in actual_close_prices]  # Dummy prediction (1% increase)

    # Calculate error metrics 12345
    mae = np.mean(np.abs(np.array(actual_close_prices) - np.array(predicted_close_prices)))
    mse = np.mean((np.array(actual_close_prices) - np.array(predicted_close_prices)) ** 2)
    
    return jsonify({
        'mae': mae,
        'mse': mse,
        'actual': actual_close_prices,
        'predicted': predicted_close_prices
    })

if __name__ == '__main__':
    app.run(debug=True)
