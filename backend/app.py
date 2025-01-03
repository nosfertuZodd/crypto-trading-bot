import os
import logging
from flask import Flask, jsonify, request
from binance.client import Client
from binance.exceptions import BinanceAPIException
from flask_cors import CORS
import requests
import pandas as pd
import datetime
import time
import numpy as np
from dotenv import load_dotenv
from config import Config
from config.db import db
from config.db.models import User

# Load environment variables
load_dotenv()

# Initialize Flask app and CORS
app = Flask(__name__)
CORS(app)
app.config.from_object(Config)

db.init_app(app)

@app.route('/users', methods=['GET'])
def get_users():
    users = User.query.all()
    return jsonify([{'id': user.id, 'username': user.username, 'email': user.email} for user in users])


# Load API keys from environment variables for security

API_KEY = os.getenv('API_KEY')
API_SECRET = os.getenv('API_SECRET')
TAAPI_API_KEY = os.getenv('TAAPI_API_KEY')


# Load API keys from environment variables for security
# API_KEY = 'R1abV976W7rcTLAAQJpD0NVT9UyWoe6LBCAJj93750Y26Kso1j3lEB6n2rVDuxyo'
# API_SECRET = 'FU00rdJZd0wpxLWbca4AFAVlYmMbkon9Nzddpy2DNe2kkimSazAXvArUnqYyHOuI'
# TAAPI_API_KEY = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJjbHVlIjoiNjc1MDZkYzI4YTIzODE2NDA3NTVhYjA5IiwiaWF0IjoxNzMzMzI0NDEzLCJleHAiOjMzMjM3Nzg4NDEzfQ.6ZiwhhdexNyeCRvFur0xT1RM1fxPNtQj-46KuiiAtug'

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
        'secret': TAAPI_API_KEY,
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
    elif buy_count >= 3:
        return 'Buy'
    elif sell_count >= 3:
        return 'Sell'
    else:
        return 'Hold'  # No clear decision


def extract_values(indicators):
    rsi = None
    macd = {"valueMACD": None, "valueSignal": None}

    # Iterate over the list of indicators
    for indicator in indicators:
        if indicator.get("indicator") == "rsi":
            rsi = indicator["result"].get("value")
        elif indicator.get("indicator") == "macd":
            macd["valueMACD"] = indicator["result"].get("valueMACD")
            macd["valueSignal"] = indicator["result"].get("valueMACDSignal")
    
    return rsi, macd


def combine_signals(indicators):
    # Use extract_values to get RSI and MACD data
    rsi, macd = extract_values(indicators)
    
    # Ensure the extracted values are valid
    if rsi is None or macd["valueMACD"] is None or macd["valueSignal"] is None:
        raise ValueError("RSI or MACD values are missing in the result data")
    
    # Convert values to integers
    rsi_value = float(rsi)
    macd_value = float(macd["valueMACD"])
    macd_signal = float(macd["valueSignal"])
    
    # Determine signals based on RSI and MACD logic
    if rsi_value < 30 and macd_value > macd_signal:
        return "BUY"
    elif rsi_value > 70 and macd_value < macd_signal:
        return "SELL"
    else:
        return "HOLD"

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
    interval = request.json.get('interval', '1h')
    
    if not user_indicators:
        return jsonify({'error': 'Please provide at least one indicator.'}), 400

    # Prepare the payload for the TAAPI.io API request
    payload = {
        'secret': TAAPI_API_KEY,
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
            prediction = make_prediction(indicators)
            signals = combine_signals(indicators)

            return jsonify({
                'indicators': indicators,
                'prediction': prediction,
                'signals' :signals
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

 
@app.route('/candlestick_data', methods=['GET'])
def get_candlestick_data_chart():
    # Get the symbol and interval from query parameters, with defaults
    symbol = request.args.get('symbol', default='BTCUSDT', type=str)  # Default symbol is BTCUSDT
    interval = request.args.get('interval', default=Client.KLINE_INTERVAL_5MINUTE, type=str)  # Default interval is 5m

    # Get the current time in UTC
    end_date = datetime.datetime.utcnow()  # Current UTC time
    start_date = end_date - datetime.timedelta(hours=10)  # Start date is 10 hours ego from now

    # Format the dates in the required string format for the Binance API
    start_date_str = start_date.strftime('%Y-%m-%d %H:%M:%S')
    end_date_str = end_date.strftime('%Y-%m-%d %H:%M:%S')

    all_data = []

    try:
        # Increase the limit to ensure we get multiple candles for the last 5 minutes
        limit = 100  # Adjust the limit to fetch more candles (try 10 or more)

        # Fetch candlesticks for the last 5 minutes
        candlesticks = client.get_historical_klines(
            symbol=symbol,
            interval=interval,
            start_str=start_date_str,
            end_str=end_date_str,
            limit=limit  # Fetch 10 candles to cover the last 5 minutes
        )

        # Prepare the data in a format that React can consume
        data = [
            {
                'dateTime': pd.to_datetime(candle[0], unit='ms').strftime('%Y-%m-%d %H:%M:%S'),
                'open': float(candle[1]),
                'high': float(candle[2]),
                'low': float(candle[3]),
                'close': float(candle[4]),
                'volume': float(candle[5]),
            }
            for candle in candlesticks
        ]

        return jsonify(data), 200  # Return the candlestick data as JSON

    except Exception as e:
        logging.error(f"Error fetching candlestick data: {str(e)}")
        return jsonify({'error': 'Failed to fetch candlestick data'}), 500

from sqlalchemy import text

@app.route('/check_db_connection', methods=['GET'])
def check_db_connection():
    try:
        # Run a simple query to check the connection
        db.session.execute(text('SELECT 1'))
        return jsonify({'message': 'Database connection successful'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Endpoint to fetch indicator data
@app.route('/indicators', methods=['POST'])
def get_indicators():
    symbol = request.json.get('symbol', 'BTCUSDT')
    interval = request.json.get('interval', '1h')
    responses = []

    # Fetch indicators for the selected symbol and interval
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
    symbol = request.json.get('symbol', 'BTCUSDT')
    quantity = request.json.get('quantity', 0.001)
    
    order = place_order(symbol, quantity, Client.SIDE_BUY)
    if order:
        return jsonify(order)
    return jsonify({'error': 'Failed to place buy order'}), 500

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

    # Calculate error metrics
    mae = np.mean(np.abs(np.array(actual_close_prices) - np.array(predicted_close_prices)))
    mse = np.mean((np.array(actual_close_prices) - np.array(predicted_close_prices)) ** 2)

    return jsonify({
        'mae': mae,
        'mse': mse,
        'actual': actual_close_prices,
        'predicted': predicted_close_prices
    })

if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Ensure the tables are created
    app.run(debug=True)
