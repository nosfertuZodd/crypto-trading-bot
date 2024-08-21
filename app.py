from flask import Flask, jsonify, request
from binance import Client
from requests.exceptions import Timeout
from flask_cors import CORS
from binance.exceptions import BinanceAPIException
import requests
import json

# Initiaizaing a Flask app
app = Flask(__name__)
CORS(app)

api_key = 'R1abV976W7rcTLAAQJpD0NVT9UyWoe6LBCAJj93750Y26Kso1j3lEB6n2rVDuxyo'
api_secret = 'FU00rdJZd0wpxLWbca4AFAVlYmMbkon9Nzddpy2DNe2kkimSazAXvArUnqYyHOuI'
taapi_api = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJjbHVlIjoiNjA4NzExNGM0MjI0NmNlM2IwY2U1ZWUzIiwiaWF0IjoxNzIxNDE2ODU3LCJleHAiOjMzMjI1ODgwODU3fQ.i3Mon47Geg_zIZV2sMl8JlFvFJSQruMua6oyLAp7Ebk'
client = Client(api_key, api_secret)

@app.route('/symbols', methods=['GET'])
def get_symbols():
    try:
        exchange_info = client.get_exchange_info()
        symbols = [s['symbol'] for s in exchange_info['symbols']]
        return jsonify({'symbols': symbols})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/candlestick_data', methods=['GET'])
def get_candlestick_data():
    symbol = request.args.get('symbol', default='BTCUSDT', type=str)
    interval = request.args.get('interval', default=Client.KLINE_INTERVAL_1DAY, type=str)
    limit = request.args.get('limit', default=500, type=int)
    try:
        candlesticks = client.get_klines(symbol=symbol, interval=interval, limit=limit)
        data = [{
            "time": c[0],
            "open": c[1],
            "high": c[2],
            "low": c[3],
            "close": c[4],
            "volume": c[5]
        } for c in candlesticks]
        return jsonify(data)
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
        
if __name__ == '__main__':
    app.run(debug=True)