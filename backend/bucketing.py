import os
import ta
import pandas as pd

symbol_weights = {
    '1INCHUSDT': {
        'rsi': 0.11, 'stoch_k': 0.04, 'stoch_d': 0.04, 'macd': 0.12, 'ao': 0.05,
        'cci': 0.04, 'ema_13': 0.05, 'sma': 0.05, 'psar': 0.05, 'roc': 0.04,
        'obv': 0.09, 'adi': 0.06, 'atr': 0.07, 'high_bbands': 0.03, 'low_bbands': 0.03,
        'donc_chan_high': 0.025, 'donc_chan_low': 0.025, 'kelterChannelhband': 0.03, 'kelterchannellband': 0.03,
        'wpr': 0.05, 'uo': 0.05
    },
    'AAVEBTC': {
        'rsi': 0.10, 'stoch_k': 0.03, 'stoch_d': 0.03, 'macd': 0.13, 'ao': 0.06,
        'cci': 0.05, 'ema_13': 0.06, 'sma': 0.06, 'psar': 0.05, 'roc': 0.04,
        'obv': 0.10, 'adi': 0.07, 'atr': 0.06, 'high_bbands': 0.03, 'low_bbands': 0.03,
        'donc_chan_high': 0.03, 'donc_chan_low': 0.03, 'kelterChannelhband': 0.03, 'kelterchannellband': 0.03,
        'wpr': 0.04, 'uo': 0.06
    },
    'AAVEUSDT': {
        'rsi': 0.12, 'stoch_k': 0.03, 'stoch_d': 0.03, 'macd': 0.12, 'ao': 0.05,
        'cci': 0.05, 'ema_13': 0.06, 'sma': 0.06, 'psar': 0.05, 'roc': 0.05,
        'obv': 0.09, 'adi': 0.06, 'atr': 0.07, 'high_bbands': 0.03, 'low_bbands': 0.03,
        'donc_chan_high': 0.03, 'donc_chan_low': 0.03, 'kelterChannelhband': 0.03, 'kelterchannellband': 0.03,
        'wpr': 0.05, 'uo': 0.05
    },
    'ADABTC': {
        'rsi': 0.11, 'stoch_k': 0.04, 'stoch_d': 0.04, 'macd': 0.12, 'ao': 0.05,
        'cci': 0.04, 'ema_13': 0.05, 'sma': 0.05, 'psar': 0.05, 'roc': 0.04,
        'obv': 0.08, 'adi': 0.06, 'atr': 0.06, 'high_bbands': 0.03, 'low_bbands': 0.03,
        'donc_chan_high': 0.03, 'donc_chan_low': 0.03, 'kelterChannelhband': 0.03, 'kelterchannellband': 0.03,
        'wpr': 0.05, 'uo': 0.05
    },
    'ADAUSDT': { 
        'rsi': 0.12, 'stoch_k': 0.04, 'stoch_d': 0.04, 'macd': 0.13, 'ao': 0.06,
        'cci': 0.05, 'ema_13': 0.06, 'sma': 0.06, 'psar': 0.06, 'roc': 0.05,
        'obv': 0.08, 'adi': 0.06, 'atr': 0.07, 'high_bbands': 0.03, 'low_bbands': 0.03,
        'donc_chan_high': 0.03, 'donc_chan_low': 0.03, 'kelterChannelhband': 0.03, 'kelterchannellband': 0.03,
        'wpr': 0.05, 'uo': 0.06
    },
    'AKROUSDT': {
        'rsi': 0.12, 'stoch_k': 0.05, 'stoch_d': 0.05, 'macd': 0.12, 'ao': 0.06,
        'cci': 0.05, 'ema_13': 0.05, 'sma': 0.05, 'psar': 0.05, 'roc': 0.04,
        'obv': 0.09, 'adi': 0.06, 'atr': 0.07, 'high_bbands': 0.03, 'low_bbands': 0.03,
        'donc_chan_high': 0.03, 'donc_chan_low': 0.03, 'kelterChannelhband': 0.03, 'kelterchannellband': 0.03,
        'wpr': 0.05, 'uo': 0.05
    },
    'ALGOETH': {
        'rsi': 0.10, 'stoch_k': 0.03, 'stoch_d': 0.03, 'macd': 0.12, 'ao': 0.05,
        'cci': 0.05, 'ema_13': 0.05, 'sma': 0.05, 'psar': 0.05, 'roc': 0.05,
        'obv': 0.08, 'adi': 0.07, 'atr': 0.06, 'high_bbands': 0.03, 'low_bbands': 0.03,
        'donc_chan_high': 0.03, 'donc_chan_low': 0.03, 'kelterChannelhband': 0.03, 'kelterchannellband': 0.03,
        'wpr': 0.05, 'uo': 0.05
    },
    'ALGOUSDT': {
        'rsi': 0.12, 'stoch_k': 0.04, 'stoch_d': 0.04, 'macd': 0.12, 'ao': 0.06,
        'cci': 0.05, 'ema_13': 0.05, 'sma': 0.06, 'psar': 0.05, 'roc': 0.05,
        'obv': 0.08, 'adi': 0.06, 'atr': 0.07, 'high_bbands': 0.03, 'low_bbands': 0.03,
        'donc_chan_high': 0.03, 'donc_chan_low': 0.03, 'kelterChannelhband': 0.03, 'kelterchannellband': 0.03,
        'wpr': 0.05, 'uo': 0.05
    },
    'ANKRUSDT': {
        'rsi': 0.12, 'stoch_k': 0.04, 'stoch_d': 0.04, 'macd': 0.12, 'ao': 0.06,
        'cci': 0.05, 'ema_13': 0.05, 'sma': 0.06, 'psar': 0.05, 'roc': 0.04,
        'obv': 0.09, 'adi': 0.07, 'atr': 0.07, 'high_bbands': 0.03, 'low_bbands': 0.03,
        'donc_chan_high': 0.03, 'donc_chan_low': 0.03, 'kelterChannelhband': 0.03, 'kelterchannellband': 0.03,
        'wpr': 0.05, 'uo': 0.05
    },
    'ARUSDT': {
        'rsi': 0.12, 'stoch_k': 0.05, 'stoch_d': 0.05, 'macd': 0.12, 'ao': 0.06,
        'cci': 0.05, 'ema_13': 0.05, 'sma': 0.05, 'psar': 0.05, 'roc': 0.04,
        'obv': 0.09, 'adi': 0.07, 'atr': 0.07, 'high_bbands': 0.03, 'low_bbands': 0.03,
        'donc_chan_high': 0.03, 'donc_chan_low': 0.03, 'kelterChannelhband': 0.03, 'kelterchannellband': 0.03,
        'wpr': 0.05, 'uo': 0.05
    },
    'ATOMUSDT': {
        'rsi': 0.11, 'stoch_k': 0.04, 'stoch_d': 0.04, 'macd': 0.13, 'ao': 0.06,
        'cci': 0.05, 'ema_13': 0.06, 'sma': 0.06, 'psar': 0.06, 'roc': 0.05,
        'obv': 0.08, 'adi': 0.06, 'atr': 0.06, 'high_bbands': 0.03, 'low_bbands': 0.03,
        'donc_chan_high': 0.03, 'donc_chan_low': 0.03, 'kelterChannelhband': 0.03, 'kelterchannellband': 0.03,
        'wpr': 0.05, 'uo': 0.05
    },
    'AVAXETH': {
        'rsi': 0.12, 'stoch_k': 0.04, 'stoch_d': 0.04, 'macd': 0.13, 'ao': 0.05,
        'cci': 0.05, 'ema_13': 0.06, 'sma': 0.06, 'psar': 0.06, 'roc': 0.05,
        'obv': 0.08, 'adi': 0.06, 'atr': 0.07, 'high_bbands': 0.03, 'low_bbands': 0.03,
        'donc_chan_high': 0.03, 'donc_chan_low': 0.03, 'kelterChannelhband': 0.03, 'kelterchannellband': 0.03,
        'wpr': 0.05, 'uo': 0.05
    },
    'AVAXUSDT': {
        'rsi': 0.13, 'stoch_k': 0.04, 'stoch_d': 0.04, 'macd': 0.14, 'ao': 0.06,
        'cci': 0.05, 'ema_13': 0.06, 'sma': 0.06, 'psar': 0.06, 'roc': 0.05,
        'obv': 0.09, 'adi': 0.05, 'atr': 0.08, 'high_bbands': 0.04, 'low_bbands': 0.04,
        'donc_chan_high': 0.03, 'donc_chan_low': 0.03, 'kelterChannelhband': 0.03, 'kelterchannellband': 0.03,
        'wpr': 0.05, 'uo': 0.05
    },
    'BALUSDT': {
        'rsi': 0.12, 'stoch_k': 0.04, 'stoch_d': 0.04, 'macd': 0.13, 'ao': 0.06,
        'cci': 0.05, 'ema_13': 0.06, 'sma': 0.06, 'psar': 0.05, 'roc': 0.05,
        'obv': 0.09, 'adi': 0.06, 'atr': 0.07, 'high_bbands': 0.03, 'low_bbands': 0.03,
        'donc_chan_high': 0.03, 'donc_chan_low': 0.03, 'kelterChannelhband': 0.03, 'kelterchannellband': 0.03,
        'wpr': 0.05, 'uo': 0.05
    },
    'BATETH': {
        'rsi': 0.11, 'stoch_k': 0.04, 'stoch_d': 0.04, 'macd': 0.12, 'ao': 0.05,
        'cci': 0.05, 'ema_13': 0.05, 'sma': 0.05, 'psar': 0.05, 'roc': 0.04,
        'obv': 0.08, 'adi': 0.07, 'atr': 0.06, 'high_bbands': 0.03, 'low_bbands': 0.03,
        'donc_chan_high': 0.03, 'donc_chan_low': 0.03, 'kelterChannelhband': 0.03, 'kelterchannellband': 0.03,
        'wpr': 0.05, 'uo': 0.05
    },
    'BATUSDT': {
        'rsi': 0.12, 'stoch_k': 0.04, 'stoch_d': 0.04, 'macd': 0.13, 'ao': 0.05,
        'cci': 0.05, 'ema_13': 0.06, 'sma': 0.06, 'psar': 0.05, 'roc': 0.05,
        'obv': 0.09, 'adi': 0.06, 'atr': 0.07, 'high_bbands': 0.03, 'low_bbands': 0.03,
        'donc_chan_high': 0.03, 'donc_chan_low': 0.03, 'kelterChannelhband': 0.03, 'kelterchannellband': 0.03,
        'wpr': 0.05, 'uo': 0.05
    },
    'BCHBTC': {
        'rsi': 0.10, 'stoch_k': 0.03, 'stoch_d': 0.03, 'macd': 0.12, 'ao': 0.05,
        'cci': 0.05, 'ema_13': 0.05, 'sma': 0.05, 'psar': 0.05, 'roc': 0.04,
        'obv': 0.08, 'adi': 0.07, 'atr': 0.06, 'high_bbands': 0.03, 'low_bbands': 0.03,
        'donc_chan_high': 0.03, 'donc_chan_low': 0.03, 'kelterChannelhband': 0.03, 'kelterchannellband': 0.03,
        'wpr': 0.05, 'uo': 0.05
    },
    'BCHUSDT': {
        'rsi': 0.11, 'stoch_k': 0.04, 'stoch_d': 0.04, 'macd': 0.13, 'ao': 0.06,
        'cci': 0.05, 'ema_13': 0.06, 'sma': 0.06, 'psar': 0.06, 'roc': 0.05,
        'obv': 0.09, 'adi': 0.06, 'atr': 0.07, 'high_bbands': 0.03, 'low_bbands': 0.03,
        'donc_chan_high': 0.03, 'donc_chan_low': 0.03, 'kelterChannelhband': 0.03, 'kelterchannellband': 0.03,
        'wpr': 0.05, 'uo': 0.05
    },
    'BELUSDT': {
        'rsi': 0.12, 'stoch_k': 0.05, 'stoch_d': 0.05, 'macd': 0.12, 'ao': 0.06,
        'cci': 0.05, 'ema_13': 0.05, 'sma': 0.05, 'psar': 0.05, 'roc': 0.04,
        'obv': 0.09, 'adi': 0.06, 'atr': 0.07, 'high_bbands': 0.03, 'low_bbands': 0.03,
        'donc_chan_high': 0.03, 'donc_chan_low': 0.03, 'kelterChannelhband': 0.03, 'kelterchannellband': 0.03,
        'wpr': 0.05, 'uo': 0.05
    },
    'BNBBTC': {
        'rsi': 0.10, 'stoch_k': 0.03, 'stoch_d': 0.03, 'macd': 0.12, 'ao': 0.05,
        'cci': 0.05, 'ema_13': 0.06, 'sma': 0.06, 'psar': 0.05, 'roc': 0.05,
        'obv': 0.09, 'adi': 0.07, 'atr': 0.07, 'high_bbands': 0.03, 'low_bbands': 0.03,
        'donc_chan_high': 0.03, 'donc_chan_low': 0.03, 'kelterChannelhband': 0.03, 'kelterchannellband': 0.03,
        'wpr': 0.05, 'uo': 0.05
    },
    'BNBUSDT': {
        'rsi': 0.12, 'stoch_k': 0.04, 'stoch_d': 0.04, 'macd': 0.13, 'ao': 0.05,
        'cci': 0.05, 'ema_13': 0.06, 'sma': 0.06, 'psar': 0.05, 'roc': 0.05,
        'obv': 0.09, 'adi': 0.06, 'atr': 0.07, 'high_bbands': 0.03, 'low_bbands': 0.03,
        'donc_chan_high': 0.03, 'donc_chan_low': 0.03, 'kelterChannelhband': 0.03, 'kelterchannellband': 0.03,
        'wpr': 0.05, 'uo': 0.05
    },
    'BNTUSDT': {
        'rsi': 0.11, 'stoch_k': 0.04, 'stoch_d': 0.04, 'macd': 0.12, 'ao': 0.05,
        'cci': 0.05, 'ema_13': 0.06, 'sma': 0.05, 'psar': 0.05, 'roc': 0.05,
        'obv': 0.09, 'adi': 0.06, 'atr': 0.06, 'high_bbands': 0.03, 'low_bbands': 0.03,
        'donc_chan_high': 0.03, 'donc_chan_low': 0.03, 'kelterChannelhband': 0.03, 'kelterchannellband': 0.03,
        'wpr': 0.05, 'uo': 0.05
    },
    'BTC-indicators': {
        'rsi': 0.12, 'stoch_k': 0.04, 'stoch_d': 0.04, 'macd': 0.13, 'ao': 0.06,
        'cci': 0.05, 'ema_13': 0.06, 'sma': 0.06, 'psar': 0.06, 'roc': 0.05,
        'obv': 0.09, 'adi': 0.07, 'atr': 0.07, 'high_bbands': 0.03, 'low_bbands': 0.03,
        'donc_chan_high': 0.03, 'donc_chan_low': 0.03, 'kelterChannelhband': 0.03, 'kelterchannellband': 0.03,
        'wpr': 0.05, 'uo': 0.05
    },
    'CAKEUSDT-indicators': {
        'rsi': 0.13, 'stoch_k': 0.05, 'stoch_d': 0.05, 'macd': 0.12, 'ao': 0.06,
        'cci': 0.05, 'ema_13': 0.05, 'sma': 0.05, 'psar': 0.05, 'roc': 0.04,
        'obv': 0.09, 'adi': 0.06, 'atr': 0.07, 'high_bbands': 0.03, 'low_bbands': 0.03,
        'donc_chan_high': 0.03, 'donc_chan_low': 0.03, 'kelterChannelhband': 0.03, 'kelterchannellband': 0.03,
        'wpr': 0.05, 'uo': 0.05
    },
    'CELRUSDT-indicators': {
        'rsi': 0.12, 'stoch_k': 0.04, 'stoch_d': 0.04, 'macd': 0.13, 'ao': 0.06,
        'cci': 0.05, 'ema_13': 0.06, 'sma': 0.06, 'psar': 0.06, 'roc': 0.05,
        'obv': 0.09, 'adi': 0.06, 'atr': 0.07, 'high_bbands': 0.03, 'low_bbands': 0.03,
        'donc_chan_high': 0.03, 'donc_chan_low': 0.03, 'kelterChannelhband': 0.03, 'kelterchannellband': 0.03,
        'wpr': 0.05, 'uo': 0.05
    },
    'CHZUSDT-indicators': {
        'rsi': 0.11, 'stoch_k': 0.04, 'stoch_d': 0.04, 'macd': 0.12, 'ao': 0.05,
        'cci': 0.05, 'ema_13': 0.06, 'sma': 0.06, 'psar': 0.05, 'roc': 0.05,
        'obv': 0.09, 'adi': 0.06, 'atr': 0.06, 'high_bbands': 0.03, 'low_bbands': 0.03,
        'donc_chan_high': 0.03, 'donc_chan_low': 0.03, 'kelterChannelhband': 0.03, 'kelterchannellband': 0.03,
        'wpr': 0.05, 'uo': 0.05
    },
    'COMPUSDT-indicators': {
        'rsi': 0.13, 'stoch_k': 0.04, 'stoch_d': 0.04, 'macd': 0.13, 'ao': 0.06,
        'cci': 0.05, 'ema_13': 0.06, 'sma': 0.06, 'psar': 0.06, 'roc': 0.05,
        'obv': 0.09, 'adi': 0.06, 'atr': 0.07, 'high_bbands': 0.03, 'low_bbands': 0.03,
        'donc_chan_high': 0.03, 'donc_chan_low': 0.03, 'kelterChannelhband': 0.03, 'kelterchannellband': 0.03,
        'wpr': 0.05, 'uo': 0.05
    },
    'CRVETH-indicators': {
        'rsi': 0.11, 'stoch_k': 0.04, 'stoch_d': 0.04, 'macd': 0.12, 'ao': 0.05,
        'cci': 0.05, 'ema_13': 0.06, 'sma': 0.06, 'psar': 0.05, 'roc': 0.05,
        'obv': 0.09, 'adi': 0.06, 'atr': 0.07, 'high_bbands': 0.03, 'low_bbands': 0.03,
        'donc_chan_high': 0.03, 'donc_chan_low': 0.03, 'kelterChannelhband': 0.03, 'kelterchannellband': 0.03,
        'wpr': 0.05, 'uo': 0.05
    },
    'CRVUSDT-indicators': {
        'rsi': 0.12, 'stoch_k': 0.04, 'stoch_d': 0.04, 'macd': 0.13, 'ao': 0.06,
        'cci': 0.05, 'ema_13': 0.06, 'sma': 0.06, 'psar': 0.05, 'roc': 0.05,
        'obv': 0.09, 'adi': 0.06, 'atr': 0.07, 'high_bbands': 0.03, 'low_bbands': 0.03,
        'donc_chan_high': 0.03, 'donc_chan_low': 0.03, 'kelterChannelhband': 0.03, 'kelterchannellband': 0.03,
        'wpr': 0.05, 'uo': 0.05
    },
    'CTSIUSDT-indicators': {
        'rsi': 0.11, 'stoch_k': 0.04, 'stoch_d': 0.04, 'macd': 0.12, 'ao': 0.05,
        'cci': 0.05, 'ema_13': 0.05, 'sma': 0.05, 'psar': 0.05, 'roc': 0.04,
        'obv': 0.09, 'adi': 0.07, 'atr': 0.06, 'high_bbands': 0.03, 'low_bbands': 0.03,
        'donc_chan_high': 0.03, 'donc_chan_low': 0.03, 'kelterChannelhband': 0.03, 'kelterchannellband': 0.03,
        'wpr': 0.05, 'uo': 0.05
    },
    'CVCUSDT-indicators': {
        'rsi': 0.12, 'stoch_k': 0.05, 'stoch_d': 0.05, 'macd': 0.13, 'ao': 0.06,
        'cci': 0.05, 'ema_13': 0.05, 'sma': 0.05, 'psar': 0.05, 'roc': 0.04,
        'obv': 0.09, 'adi': 0.06, 'atr': 0.07, 'high_bbands': 0.03, 'low_bbands': 0.03,
        'donc_chan_high': 0.03, 'donc_chan_low': 0.03, 'kelterChannelhband': 0.03, 'kelterchannellband': 0.03,
        'wpr': 0.05, 'uo': 0.05
    },
    'DASHETH-indicators': {
        'rsi': 0.11, 'stoch_k': 0.04, 'stoch_d': 0.04, 'macd': 0.12, 'ao': 0.05,
        'cci': 0.05, 'ema_13': 0.06, 'sma': 0.06, 'psar': 0.05, 'roc': 0.05,
        'obv': 0.09, 'adi': 0.07, 'atr': 0.06, 'high_bbands': 0.03, 'low_bbands': 0.03,
        'donc_chan_high': 0.03, 'donc_chan_low': 0.03, 'kelterChannelhband': 0.03, 'kelterchannellband': 0.03,
        'wpr': 0.05, 'uo': 0.05
    },
    'DASHUSDT-indicators': {
        'rsi': 0.12, 'stoch_k': 0.04, 'stoch_d': 0.04, 'macd': 0.13, 'ao': 0.06,
        'cci': 0.05, 'ema_13': 0.06, 'sma': 0.06, 'psar': 0.06, 'roc': 0.05,
        'obv': 0.09, 'adi': 0.06, 'atr': 0.07, 'high_bbands': 0.03, 'low_bbands': 0.03,
        'donc_chan_high': 0.03, 'donc_chan_low': 0.03, 'kelterChannelhband': 0.03, 'kelterchannellband': 0.03,
        'wpr': 0.05, 'uo': 0.05
    },
    'DENTETH-indicators': {
        'rsi': 0.12, 'stoch_k': 0.05, 'stoch_d': 0.05, 'macd': 0.12, 'ao': 0.06,
        'cci': 0.05, 'ema_13': 0.05, 'sma': 0.05, 'psar': 0.05, 'roc': 0.04,
        'obv': 0.09, 'adi': 0.06, 'atr': 0.07, 'high_bbands': 0.03, 'low_bbands': 0.03,
        'donc_chan_high': 0.03, 'donc_chan_low': 0.03, 'kelterChannelhband': 0.03, 'kelterchannellband': 0.03,
        'wpr': 0.05, 'uo': 0.05
    },
    'DENTUSDT-indicators': {
        'rsi': 0.11, 'stoch_k': 0.04, 'stoch_d': 0.04, 'macd': 0.13, 'ao': 0.06,
        'cci': 0.05, 'ema_13': 0.05, 'sma': 0.05, 'psar': 0.05, 'roc': 0.05,
        'obv': 0.09, 'adi': 0.06, 'atr': 0.07, 'high_bbands': 0.03, 'low_bbands': 0.03,
        'donc_chan_high': 0.03, 'donc_chan_low': 0.03, 'kelterChannelhband': 0.03, 'kelterchannellband': 0.03,
        'wpr': 0.05, 'uo': 0.05
    },
    'DOGEBTC-indicators': {
        'rsi': 0.14, 'stoch_k': 0.05, 'stoch_d': 0.05, 'macd': 0.14, 'ao': 0.06,
        'cci': 0.05, 'ema_13': 0.06, 'sma': 0.06, 'psar': 0.05, 'roc': 0.05,
        'obv': 0.10, 'adi': 0.06, 'atr': 0.09, 'high_bbands': 0.04, 'low_bbands': 0.04,
        'donc_chan_high': 0.04, 'donc_chan_low': 0.04, 'kelterChannelhband': 0.03, 'kelterchannellband': 0.03,
        'wpr': 0.05, 'uo': 0.05
    },
    'DOGEUSDT-indicators': {
        'rsi': 0.14, 'stoch_k': 0.05, 'stoch_d': 0.05, 'macd': 0.14, 'ao': 0.06,
        'cci': 0.05, 'ema_13': 0.06, 'sma': 0.06, 'psar': 0.05, 'roc': 0.05,
        'obv': 0.10, 'adi': 0.06, 'atr': 0.09, 'high_bbands': 0.04, 'low_bbands': 0.04,
        'donc_chan_high': 0.04, 'donc_chan_low': 0.04, 'kelterChannelhband': 0.03, 'kelterchannellband': 0.03,
        'wpr': 0.05, 'uo': 0.05
    },
    'DOTBTC-indicators': {
        'rsi': 0.11, 'stoch_k': 0.04, 'stoch_d': 0.04, 'macd': 0.12, 'ao': 0.05,
        'cci': 0.05, 'ema_13': 0.06, 'sma': 0.06, 'psar': 0.05, 'roc': 0.05,
        'obv': 0.09, 'adi': 0.06, 'atr': 0.07, 'high_bbands': 0.03, 'low_bbands': 0.03,
        'donc_chan_high': 0.03, 'donc_chan_low': 0.03, 'kelterChannelhband': 0.03, 'kelterchannellband': 0.03,
        'wpr': 0.05, 'uo': 0.05
    },
    'DOTUSDT-indicators': {
        'rsi': 0.12, 'stoch_k': 0.04, 'stoch_d': 0.04, 'macd': 0.13, 'ao': 0.06,
        'cci': 0.05, 'ema_13': 0.06, 'sma': 0.06, 'psar': 0.06, 'roc': 0.05,
        'obv': 0.09, 'adi': 0.06, 'atr': 0.07, 'high_bbands': 0.03, 'low_bbands': 0.03,
        'donc_chan_high': 0.03, 'donc_chan_low': 0.03, 'kelterChannelhband': 0.03, 'kelterchannellband': 0.03,
        'wpr': 0.05, 'uo': 0.05
    },
    'EGLDETH-indicators': {
        'rsi': 0.11, 'stoch_k': 0.04, 'stoch_d': 0.04, 'macd': 0.12, 'ao': 0.05,
        'cci': 0.05, 'ema_13': 0.06, 'sma': 0.06, 'psar': 0.05, 'roc': 0.05,
        'obv': 0.09, 'adi': 0.07, 'atr': 0.06, 'high_bbands': 0.03, 'low_bbands': 0.03,
        'donc_chan_high': 0.03, 'donc_chan_low': 0.03, 'kelterChannelhband': 0.03, 'kelterchannellband': 0.03,
        'wpr': 0.05, 'uo': 0.05
    },
    'EGLDUSDT-indicators': {
        'rsi': 0.12, 'stoch_k': 0.04, 'stoch_d': 0.04, 'macd': 0.13, 'ao': 0.06,
        'cci': 0.05, 'ema_13': 0.06, 'sma': 0.06, 'psar': 0.06, 'roc': 0.05,
        'obv': 0.09, 'adi': 0.06, 'atr': 0.07, 'high_bbands': 0.03, 'low_bbands': 0.03,
        'donc_chan_high': 0.03, 'donc_chan_low': 0.03, 'kelterChannelhband': 0.03, 'kelterchannellband': 0.03,
        'wpr': 0.05, 'uo': 0.05
    },
    'ENJUSDT-indicators': {
        'rsi': 0.12, 'stoch_k': 0.04, 'stoch_d': 0.04, 'macd': 0.13, 'ao': 0.06,
        'cci': 0.05, 'ema_13': 0.05, 'sma': 0.05, 'psar': 0.05, 'roc': 0.05,
        'obv': 0.09, 'adi': 0.06, 'atr': 0.07, 'high_bbands': 0.03, 'low_bbands': 0.03,
        'donc_chan_high': 0.03, 'donc_chan_low': 0.03, 'kelterChannelhband': 0.03, 'kelterchannellband': 0.03,
        'wpr': 0.05, 'uo': 0.05
    },
    'EOSUSDT-indicators': {
        'rsi': 0.11, 'stoch_k': 0.04, 'stoch_d': 0.04, 'macd': 0.12, 'ao': 0.05,
        'cci': 0.05, 'ema_13': 0.06, 'sma': 0.06, 'psar': 0.05, 'roc': 0.05,
        'obv': 0.09, 'adi': 0.07, 'atr': 0.06, 'high_bbands': 0.03, 'low_bbands': 0.03,
        'donc_chan_high': 0.03, 'donc_chan_low': 0.03, 'kelterChannelhband': 0.03, 'kelterchannellband': 0.03,
        'wpr': 0.05, 'uo': 0.05
    },
    'ETHBTC-indicators': {
        'rsi': 0.12, 'stoch_k': 0.04, 'stoch_d': 0.04, 'macd': 0.13, 'ao': 0.06,
        'cci': 0.05, 'ema_13': 0.06, 'sma': 0.06, 'psar': 0.06, 'roc': 0.05,
        'obv': 0.09, 'adi': 0.07, 'atr': 0.07, 'high_bbands': 0.03, 'low_bbands': 0.03,
        'donc_chan_high': 0.03, 'donc_chan_low': 0.03, 'kelterChannelhband': 0.03, 'kelterchannellband': 0.03,
        'wpr': 0.05, 'uo': 0.05
    },
    'ETHUSDT-indicators': {
        'rsi': 0.12, 'stoch_k': 0.04, 'stoch_d': 0.04, 'macd': 0.13, 'ao': 0.06,
        'cci': 0.05, 'ema_13': 0.06, 'sma': 0.06, 'psar': 0.06, 'roc': 0.05,
        'obv': 0.09, 'adi': 0.07, 'atr': 0.07, 'high_bbands': 0.03, 'low_bbands': 0.03,
        'donc_chan_high': 0.03, 'donc_chan_low': 0.03, 'kelterChannelhband': 0.03, 'kelterchannellband': 0.03,
        'wpr': 0.05, 'uo': 0.05
    },
    'FILUSDT-indicators': {
        'rsi': 0.12, 'stoch_k': 0.04, 'stoch_d': 0.04, 'macd': 0.13, 'ao': 0.06,
        'cci': 0.05, 'ema_13': 0.06, 'sma': 0.06, 'psar': 0.06, 'roc': 0.05,
        'obv': 0.09, 'adi': 0.07, 'atr': 0.07, 'high_bbands': 0.03, 'low_bbands': 0.03,
        'donc_chan_high': 0.03, 'donc_chan_low': 0.03, 'kelterChannelhband': 0.03, 'kelterchannellband': 0.03,
        'wpr': 0.05, 'uo': 0.05
    },
    'FTMETH-indicators': {
        'rsi': 0.11, 'stoch_k': 0.04, 'stoch_d': 0.04, 'macd': 0.12, 'ao': 0.05,
        'cci': 0.05, 'ema_13': 0.05, 'sma': 0.05, 'psar': 0.05, 'roc': 0.05,
        'obv': 0.09, 'adi': 0.07, 'atr': 0.07, 'high_bbands': 0.03, 'low_bbands': 0.03,
        'donc_chan_high': 0.03, 'donc_chan_low': 0.03, 'kelterChannelhband': 0.03, 'kelterchannellband': 0.03,
        'wpr': 0.05, 'uo': 0.05
    },
    'FTMUSDT-indicators': {
        'rsi': 0.12, 'stoch_k': 0.04, 'stoch_d': 0.04, 'macd': 0.13, 'ao': 0.06,
        'cci': 0.05, 'ema_13': 0.06, 'sma': 0.06, 'psar': 0.06, 'roc': 0.05,
        'obv': 0.09, 'adi': 0.06, 'atr': 0.07, 'high_bbands': 0.03, 'low_bbands': 0.03,
        'donc_chan_high': 0.03, 'donc_chan_low': 0.03, 'kelterChannelhband': 0.03, 'kelterchannellband': 0.03,
        'wpr': 0.05, 'uo': 0.05
    },
    'FTTUSDT-indicators': {
        'rsi': 0.12, 'stoch_k': 0.04, 'stoch_d': 0.04, 'macd': 0.13, 'ao': 0.06,
        'cci': 0.05, 'ema_13': 0.06, 'sma': 0.06, 'psar': 0.06, 'roc': 0.05,
        'obv': 0.09, 'adi': 0.06, 'atr': 0.07, 'high_bbands': 0.03, 'low_bbands': 0.03,
        'donc_chan_high': 0.03, 'donc_chan_low': 0.03, 'kelterChannelhband': 0.03, 'kelterchannellband': 0.03,
        'wpr': 0.05, 'uo': 0.05
    },
    'GRTUSDT-indicators': {
        'rsi': 0.11, 'stoch_k': 0.04, 'stoch_d': 0.04, 'macd': 0.12, 'ao': 0.05,
        'cci': 0.05, 'ema_13': 0.06, 'sma': 0.06, 'psar': 0.05, 'roc': 0.05,
        'obv': 0.09, 'adi': 0.07, 'atr': 0.06, 'high_bbands': 0.03, 'low_bbands': 0.03,
        'donc_chan_high': 0.03, 'donc_chan_low': 0.03, 'kelterChannelhband': 0.03, 'kelterchannellband': 0.03,
        'wpr': 0.05, 'uo': 0.05
    },
    'HBARUSDT-indicators': {
        'rsi': 0.12, 'stoch_k': 0.04, 'stoch_d': 0.04, 'macd': 0.13, 'ao': 0.06,
        'cci': 0.05, 'ema_13': 0.06, 'sma': 0.06, 'psar': 0.06, 'roc': 0.05,
        'obv': 0.09, 'adi': 0.07, 'atr': 0.07, 'high_bbands': 0.03, 'low_bbands': 0.03,
        'donc_chan_high': 0.03, 'donc_chan_low': 0.03, 'kelterChannelhband': 0.03, 'kelterchannellband': 0.03,
        'wpr': 0.05, 'uo': 0.05
    },
    'ICPUSDT-indicators': {
        'rsi': 0.12, 'stoch_k': 0.04, 'stoch_d': 0.04, 'macd': 0.13, 'ao': 0.06,
        'cci': 0.05, 'ema_13': 0.06, 'sma': 0.06, 'psar': 0.06, 'roc': 0.05,
        'obv': 0.09, 'adi': 0.07, 'atr': 0.07, 'high_bbands': 0.03, 'low_bbands': 0.03,
        'donc_chan_high': 0.03, 'donc_chan_low': 0.03, 'kelterChannelhband': 0.03, 'kelterchannellband': 0.03,
        'wpr': 0.05, 'uo': 0.05
    },
    'ICXUSDT-indicators': {
        'rsi': 0.11, 'stoch_k': 0.04, 'stoch_d': 0.04, 'macd': 0.12, 'ao': 0.05,
        'cci': 0.05, 'ema_13': 0.06, 'sma': 0.06, 'psar': 0.05, 'roc': 0.05,
        'obv': 0.09, 'adi': 0.07, 'atr': 0.06, 'high_bbands': 0.03, 'low_bbands': 0.03,
        'donc_chan_high': 0.03, 'donc_chan_low': 0.03, 'kelterChannelhband': 0.03, 'kelterchannellband': 0.03,
        'wpr': 0.05, 'uo': 0.05
    },
     'MANAETH-indicators': {
        'rsi': 0.11, 'stoch_k': 0.04, 'stoch_d': 0.04, 'macd': 0.12, 'ao': 0.05,
        'cci': 0.05, 'ema_13': 0.05, 'sma': 0.05, 'psar': 0.05, 'roc': 0.05,
        'obv': 0.09, 'adi': 0.06, 'atr': 0.06, 'high_bbands': 0.03, 'low_bbands': 0.03,
        'donc_chan_high': 0.03, 'donc_chan_low': 0.03, 'kelterChannelhband': 0.03, 'kelterchannellband': 0.03,
        'wpr': 0.05, 'uo': 0.05
    },
    'MANAUSDT-indicators': {
        'rsi': 0.12, 'stoch_k': 0.04, 'stoch_d': 0.04, 'macd': 0.13, 'ao': 0.06,
        'cci': 0.05, 'ema_13': 0.06, 'sma': 0.06, 'psar': 0.06, 'roc': 0.05,
        'obv': 0.09, 'adi': 0.06, 'atr': 0.07, 'high_bbands': 0.03, 'low_bbands': 0.03,
        'donc_chan_high': 0.03, 'donc_chan_low': 0.03, 'kelterChannelhband': 0.03, 'kelterchannellband': 0.03,
        'wpr': 0.05, 'uo': 0.05
    },
    'MATICBTC-indicators': {
        'rsi': 0.12, 'stoch_k': 0.04, 'stoch_d': 0.04, 'macd': 0.13, 'ao': 0.06,
        'cci': 0.05, 'ema_13': 0.06, 'sma': 0.06, 'psar': 0.06, 'roc': 0.05,
        'obv': 0.09, 'adi': 0.06, 'atr': 0.07, 'high_bbands': 0.03, 'low_bbands': 0.03,
        'donc_chan_high': 0.03, 'donc_chan_low': 0.03, 'kelterChannelhband': 0.03, 'kelterchannellband': 0.03,
        'wpr': 0.05, 'uo': 0.05
    },
    'MATICETH-indicators': {
        'rsi': 0.12, 'stoch_k': 0.04, 'stoch_d': 0.04, 'macd': 0.13, 'ao': 0.06,
        'cci': 0.05, 'ema_13': 0.06, 'sma': 0.06, 'psar': 0.06, 'roc': 0.05,
        'obv': 0.09, 'adi': 0.06, 'atr': 0.07, 'high_bbands': 0.03, 'low_bbands': 0.03,
        'donc_chan_high': 0.03, 'donc_chan_low': 0.03, 'kelterChannelhband': 0.03, 'kelterchannellband': 0.03,
        'wpr': 0.05, 'uo': 0.05
    },
    'MATICUSDT-indicators': {
        'rsi': 0.13, 'stoch_k': 0.04, 'stoch_d': 0.04, 'macd': 0.13, 'ao': 0.06,
        'cci': 0.05, 'ema_13': 0.06, 'sma': 0.06, 'psar': 0.06, 'roc': 0.05,
        'obv': 0.09, 'adi': 0.06, 'atr': 0.07, 'high_bbands': 0.03, 'low_bbands': 0.03,
        'donc_chan_high': 0.03, 'donc_chan_low': 0.03, 'kelterChannelhband': 0.03, 'kelterchannellband': 0.03,
        'wpr': 0.05, 'uo': 0.05
    },
    'MKRUSDT-indicators': {
        'rsi': 0.12, 'stoch_k': 0.04, 'stoch_d': 0.04, 'macd': 0.13, 'ao': 0.06,
        'cci': 0.05, 'ema_13': 0.06, 'sma': 0.06, 'psar': 0.06, 'roc': 0.05,
        'obv': 0.09, 'adi': 0.06, 'atr': 0.07, 'high_bbands': 0.03, 'low_bbands': 0.03,
        'donc_chan_high': 0.03, 'donc_chan_low': 0.03, 'kelterChannelhband': 0.03, 'kelterchannellband': 0.03,
        'wpr': 0.05, 'uo': 0.05
    },
    'NEARETH-indicators': {
        'rsi': 0.12, 'stoch_k': 0.04, 'stoch_d': 0.04, 'macd': 0.13, 'ao': 0.06,
        'cci': 0.05, 'ema_13': 0.06, 'sma': 0.06, 'psar': 0.06, 'roc': 0.05,
        'obv': 0.09, 'adi': 0.06, 'atr': 0.07, 'high_bbands': 0.03, 'low_bbands': 0.03,
        'donc_chan_high': 0.03, 'donc_chan_low': 0.03, 'kelterChannelhband': 0.03, 'kelterchannellband': 0.03,
        'wpr': 0.05, 'uo': 0.05
    },
    'NEARUSDT-indicators': {
        'rsi': 0.13, 'stoch_k': 0.04, 'stoch_d': 0.04, 'macd': 0.13, 'ao': 0.06,
        'cci': 0.05, 'ema_13': 0.06, 'sma': 0.06, 'psar': 0.06, 'roc': 0.05,
        'obv': 0.09, 'adi': 0.06, 'atr': 0.07, 'high_bbands': 0.03, 'low_bbands': 0.03,
        'donc_chan_high': 0.03, 'donc_chan_low': 0.03, 'kelterChannelhband': 0.03, 'kelterchannellband': 0.03,
        'wpr': 0.05, 'uo': 0.05
    },
    'NEOUSDT-indicators': {
        'rsi': 0.11, 'stoch_k': 0.04, 'stoch_d': 0.04, 'macd': 0.12, 'ao': 0.05,
        'cci': 0.05, 'ema_13': 0.06, 'sma': 0.06, 'psar': 0.05, 'roc': 0.05,
        'obv': 0.09, 'adi': 0.07, 'atr': 0.06, 'high_bbands': 0.03, 'low_bbands': 0.03,
        'donc_chan_high': 0.03, 'donc_chan_low': 0.03, 'kelterChannelhband': 0.03, 'kelterchannellband': 0.03,
        'wpr': 0.05, 'uo': 0.05
    },
    'OCEANUSDT-indicators': {
        'rsi': 0.12, 'stoch_k': 0.04, 'stoch_d': 0.04, 'macd': 0.13, 'ao': 0.06,
        'cci': 0.05, 'ema_13': 0.06, 'sma': 0.06, 'psar': 0.06, 'roc': 0.05,
        'obv': 0.09, 'adi': 0.06, 'atr': 0.07, 'high_bbands': 0.03, 'low_bbands': 0.03,
        'donc_chan_high': 0.03, 'donc_chan_low': 0.03, 'kelterChannelhband': 0.03, 'kelterchannellband': 0.03,
        'wpr': 0.05, 'uo': 0.05
    },
    'OMGUSDT-indicators': {
        'rsi': 0.11, 'stoch_k': 0.04, 'stoch_d': 0.04, 'macd': 0.12, 'ao': 0.05,
        'cci': 0.05, 'ema_13': 0.05, 'sma': 0.05, 'psar': 0.05, 'roc': 0.05,
        'obv': 0.09, 'adi': 0.06, 'atr': 0.07, 'high_bbands': 0.03, 'low_bbands': 0.03,
        'donc_chan_high': 0.03, 'donc_chan_low': 0.03, 'kelterChannelhband': 0.03, 'kelterchannellband': 0.03,
        'wpr': 0.05, 'uo': 0.05
    },
    'ONTUSDT-indicators': {
        'rsi': 0.12, 'stoch_k': 0.04, 'stoch_d': 0.04, 'macd': 0.13, 'ao': 0.06,
        'cci': 0.05, 'ema_13': 0.06, 'sma': 0.06, 'psar': 0.06, 'roc': 0.05,
        'obv': 0.09, 'adi': 0.06, 'atr': 0.07, 'high_bbands': 0.03, 'low_bbands': 0.03,
        'donc_chan_high': 0.03, 'donc_chan_low': 0.03, 'kelterChannelhband': 0.03, 'kelterchannellband': 0.03,
        'wpr': 0.05, 'uo': 0.05
    },
    'PHAUSDT-indicators': {
        'rsi': 0.11, 'stoch_k': 0.04, 'stoch_d': 0.04, 'macd': 0.12, 'ao': 0.05,
        'cci': 0.05, 'ema_13': 0.06, 'sma': 0.06, 'psar': 0.05, 'roc': 0.05,
        'obv': 0.09, 'adi': 0.07, 'atr': 0.06, 'high_bbands': 0.03, 'low_bbands': 0.03,
        'donc_chan_high': 0.03, 'donc_chan_low': 0.03, 'kelterChannelhband': 0.03, 'kelterchannellband': 0.03,
        'wpr': 0.05, 'uo': 0.05
    },
    'QTUMETH-indicators': {
        'rsi': 0.12, 'stoch_k': 0.04, 'stoch_d': 0.04, 'macd': 0.13, 'ao': 0.06,
        'cci': 0.05, 'ema_13': 0.06, 'sma': 0.06, 'psar': 0.06, 'roc': 0.05,
        'obv': 0.09, 'adi': 0.06, 'atr': 0.07, 'high_bbands': 0.03, 'low_bbands': 0.03,
        'donc_chan_high': 0.03, 'donc_chan_low': 0.03, 'kelterChannelhband': 0.03, 'kelterchannellband': 0.03,
        'wpr': 0.05, 'uo': 0.05
    },
    'QTUMUSDT-indicators': {
        'rsi': 0.13, 'stoch_k': 0.04, 'stoch_d': 0.04, 'macd': 0.13, 'ao': 0.06,
        'cci': 0.05, 'ema_13': 0.06, 'sma': 0.06, 'psar': 0.06, 'roc': 0.05,
        'obv': 0.09, 'adi': 0.06, 'atr': 0.07, 'high_bbands': 0.03, 'low_bbands': 0.03,
        'donc_chan_high': 0.03, 'donc_chan_low': 0.03, 'kelterChannelhband': 0.03, 'kelterchannellband': 0.03,
        'wpr': 0.05, 'uo': 0.05
    },
    'RENBTC-indicators': {
        'rsi': 0.11, 'stoch_k': 0.04, 'stoch_d': 0.04, 'macd': 0.12, 'ao': 0.05,
        'cci': 0.05, 'ema_13': 0.06, 'sma': 0.06, 'psar': 0.05, 'roc': 0.05,
        'obv': 0.09, 'adi': 0.07, 'atr': 0.06, 'high_bbands': 0.03, 'low_bbands': 0.03,
        'donc_chan_high': 0.03, 'donc_chan_low': 0.03, 'kelterChannelhband': 0.03, 'kelterchannellband': 0.03,
        'wpr': 0.05, 'uo': 0.05
    },
    'NEOETH-indicators': {
        'rsi': 0.11, 'stoch_k': 0.04, 'stoch_d': 0.04, 'macd': 0.12, 'ao': 0.05,
        'cci': 0.05, 'ema_13': 0.06, 'sma': 0.06, 'psar': 0.05, 'roc': 0.05,
        'obv': 0.09, 'adi': 0.07, 'atr': 0.06, 'high_bbands': 0.03, 'low_bbands': 0.03,
        'donc_chan_high': 0.03, 'donc_chan_low': 0.03, 'kelterChannelhband': 0.03, 'kelterchannellband': 0.03,
        'wpr': 0.05, 'uo': 0.05
    },
    'RENUSDT-indicators': {
        'rsi': 0.12, 'stoch_k': 0.04, 'stoch_d': 0.04, 'macd': 0.13, 'ao': 0.06,
        'cci': 0.05, 'ema_13': 0.06, 'sma': 0.06, 'psar': 0.06, 'roc': 0.05,
        'obv': 0.09, 'adi': 0.06, 'atr': 0.07, 'high_bbands': 0.03, 'low_bbands': 0.03,
        'donc_chan_high': 0.03, 'donc_chan_low': 0.03, 'kelterChannelhband': 0.03, 'kelterchannellband': 0.03,
        'wpr': 0.05, 'uo': 0.05
    },
    'RLCUSDT-indicators': {
        'rsi': 0.12, 'stoch_k': 0.04, 'stoch_d': 0.04, 'macd': 0.13, 'ao': 0.06,
        'cci': 0.05, 'ema_13': 0.06, 'sma': 0.06, 'psar': 0.06, 'roc': 0.05,
        'obv': 0.09, 'adi': 0.06, 'atr': 0.07, 'high_bbands': 0.03, 'low_bbands': 0.03,
        'donc_chan_high': 0.03, 'donc_chan_low': 0.03, 'kelterChannelhband': 0.03, 'kelterchannellband': 0.03,
        'wpr': 0.05, 'uo': 0.05
    },
    'RSRUSDT-indicators': {
        'rsi': 0.11, 'stoch_k': 0.04, 'stoch_d': 0.04, 'macd': 0.12, 'ao': 0.05,
        'cci': 0.05, 'ema_13': 0.05, 'sma': 0.05, 'psar': 0.05, 'roc': 0.04,
        'obv': 0.09, 'adi': 0.07, 'atr': 0.06, 'high_bbands': 0.03, 'low_bbands': 0.03,
        'donc_chan_high': 0.03, 'donc_chan_low': 0.03, 'kelterChannelhband': 0.03, 'kelterchannellband': 0.03,
        'wpr': 0.05, 'uo': 0.05
    },
    'RUNEETH-indicators': {
        'rsi': 0.12, 'stoch_k': 0.04, 'stoch_d': 0.04, 'macd': 0.13, 'ao': 0.06,
        'cci': 0.05, 'ema_13': 0.06, 'sma': 0.06, 'psar': 0.06, 'roc': 0.05,
        'obv': 0.09, 'adi': 0.06, 'atr': 0.07, 'high_bbands': 0.03, 'low_bbands': 0.03,
        'donc_chan_high': 0.03, 'donc_chan_low': 0.03, 'kelterChannelhband': 0.03, 'kelterchannellband': 0.03,
        'wpr': 0.05, 'uo': 0.05
    },
    'RUNEUSDT-indicators': {
        'rsi': 0.13, 'stoch_k': 0.04, 'stoch_d': 0.04, 'macd': 0.13, 'ao': 0.06,
        'cci': 0.05, 'ema_13': 0.06, 'sma': 0.06, 'psar': 0.06, 'roc': 0.05,
        'obv': 0.09, 'adi': 0.06, 'atr': 0.07, 'high_bbands': 0.03, 'low_bbands': 0.03,
        'donc_chan_high': 0.03, 'donc_chan_low': 0.03, 'kelterChannelhband': 0.03, 'kelterchannellband': 0.03,
        'wpr': 0.05, 'uo': 0.05
    },
    'SANDETH-indicators': {
        'rsi': 0.12, 'stoch_k': 0.04, 'stoch_d': 0.04, 'macd': 0.13, 'ao': 0.06,
        'cci': 0.05, 'ema_13': 0.06, 'sma': 0.06, 'psar': 0.06, 'roc': 0.05,
        'obv': 0.09, 'adi': 0.06, 'atr': 0.07, 'high_bbands': 0.03, 'low_bbands': 0.03,
        'donc_chan_high': 0.03, 'donc_chan_low': 0.03, 'kelterChannelhband': 0.03, 'kelterchannellband': 0.03,
        'wpr': 0.05, 'uo': 0.05
    },
    'SANDUSDT-indicators': {
        'rsi': 0.12, 'stoch_k': 0.04, 'stoch_d': 0.04, 'macd': 0.13, 'ao': 0.06,
        'cci': 0.05, 'ema_13': 0.06, 'sma': 0.06, 'psar': 0.06, 'roc': 0.05,
        'obv': 0.09, 'adi': 0.06, 'atr': 0.07, 'high_bbands': 0.03, 'low_bbands': 0.03,
        'donc_chan_high': 0.03, 'donc_chan_low': 0.03, 'kelterChannelhband': 0.03, 'kelterchannellband': 0.03,
        'wpr': 0.05, 'uo': 0.05
    },
    'SHIBUSDT-indicators': {
        'rsi': 0.13, 'stoch_k': 0.05, 'stoch_d': 0.05, 'macd': 0.14, 'ao': 0.06,
        'cci': 0.05, 'ema_13': 0.06, 'sma': 0.06, 'psar': 0.06, 'roc': 0.05,
        'obv': 0.10, 'adi': 0.06, 'atr': 0.08, 'high_bbands': 0.04, 'low_bbands': 0.04,
        'donc_chan_high': 0.04, 'donc_chan_low': 0.04, 'kelterChannelhband': 0.04, 'kelterchannellband': 0.04,
        'wpr': 0.05, 'uo': 0.05
    },
    'SOLBTC-indicators': {
        'rsi': 0.12, 'stoch_k': 0.04, 'stoch_d': 0.04, 'macd': 0.13, 'ao': 0.06,
        'cci': 0.05, 'ema_13': 0.06, 'sma': 0.06, 'psar': 0.06, 'roc': 0.05,
        'obv': 0.09, 'adi': 0.06, 'atr': 0.07, 'high_bbands': 0.03, 'low_bbands': 0.03,
        'donc_chan_high': 0.03, 'donc_chan_low': 0.03, 'kelterChannelhband': 0.03, 'kelterchannellband': 0.03,
        'wpr': 0.05, 'uo': 0.05
    },
    'SOLUSDT-indicators': {
        'rsi': 0.13, 'stoch_k': 0.05, 'stoch_d': 0.05, 'macd': 0.14, 'ao': 0.06,
        'cci': 0.05, 'ema_13': 0.06, 'sma': 0.06, 'psar': 0.06, 'roc': 0.05,
        'obv': 0.10, 'adi': 0.06, 'atr': 0.08, 'high_bbands': 0.04, 'low_bbands': 0.04,
        'donc_chan_high': 0.04, 'donc_chan_low': 0.04, 'kelterChannelhband': 0.04, 'kelterchannellband': 0.04,
        'wpr': 0.05, 'uo': 0.05
    },
    'STMXUSDT-indicators': {
        'rsi': 0.11, 'stoch_k': 0.04, 'stoch_d': 0.04, 'macd': 0.12, 'ao': 0.05,
        'cci': 0.05, 'ema_13': 0.05, 'sma': 0.05, 'psar': 0.05, 'roc': 0.05,
        'obv': 0.09, 'adi': 0.07, 'atr': 0.06, 'high_bbands': 0.03, 'low_bbands': 0.03,
        'donc_chan_high': 0.03, 'donc_chan_low': 0.03, 'kelterChannelhband': 0.03, 'kelterchannellband': 0.03,
        'wpr': 0.05, 'uo': 0.05
    },
    'STORJUSDT-indicators': {
        'rsi': 0.12, 'stoch_k': 0.04, 'stoch_d': 0.04, 'macd': 0.13, 'ao': 0.06,
        'cci': 0.05, 'ema_13': 0.06, 'sma': 0.06, 'psar': 0.06, 'roc': 0.05,
        'obv': 0.09, 'adi': 0.06, 'atr': 0.07, 'high_bbands': 0.03, 'low_bbands': 0.03,
        'donc_chan_high': 0.03, 'donc_chan_low': 0.03, 'kelterChannelhband': 0.03, 'kelterchannellband': 0.03,
        'wpr': 0.05, 'uo': 0.05
    },
    'SHIBBTC-indicators': {
        'rsi': 0.13, 'stoch_k': 0.05, 'stoch_d': 0.05, 'macd': 0.14, 'ao': 0.06,
        'cci': 0.05, 'ema_13': 0.06, 'sma': 0.06, 'psar': 0.06, 'roc': 0.05,
        'obv': 0.10, 'adi': 0.06, 'atr': 0.08, 'high_bbands': 0.04, 'low_bbands': 0.04,
        'donc_chan_high': 0.04, 'donc_chan_low': 0.04, 'kelterChannelhband': 0.04, 'kelterchannellband': 0.04,
        'wpr': 0.05, 'uo': 0.05
    },
    'SUSHIBTC-indicators': {
        'rsi': 0.12, 'stoch_k': 0.04, 'stoch_d': 0.04, 'macd': 0.13, 'ao': 0.06,
        'cci': 0.05, 'ema_13': 0.06, 'sma': 0.06, 'psar': 0.06, 'roc': 0.05,
        'obv': 0.09, 'adi': 0.06, 'atr': 0.07, 'high_bbands': 0.03, 'low_bbands': 0.03,
        'donc_chan_high': 0.03, 'donc_chan_low': 0.03, 'kelterChannelhband': 0.03, 'kelterchannellband': 0.03,
        'wpr': 0.05, 'uo': 0.05
    },
    'SUSHIUSDT-indicators': {
        'rsi': 0.12, 'stoch_k': 0.04, 'stoch_d': 0.04, 'macd': 0.13, 'ao': 0.06,
        'cci': 0.05, 'ema_13': 0.06, 'sma': 0.06, 'psar': 0.06, 'roc': 0.05,
        'obv': 0.09, 'adi': 0.06, 'atr': 0.07, 'high_bbands': 0.03, 'low_bbands': 0.03,
        'donc_chan_high': 0.03, 'donc_chan_low': 0.03, 'kelterChannelhband': 0.03, 'kelterchannellband': 0.03,
        'wpr': 0.05, 'uo': 0.05
    },
    'THETABTC-indicators': {
        'rsi': 0.11, 'stoch_k': 0.04, 'stoch_d': 0.04, 'macd': 0.12, 'ao': 0.05,
        'cci': 0.05, 'ema_13': 0.05, 'sma': 0.05, 'psar': 0.05, 'roc': 0.05,
        'obv': 0.09, 'adi': 0.07, 'atr': 0.06, 'high_bbands': 0.03, 'low_bbands': 0.03,
        'donc_chan_high': 0.03, 'donc_chan_low': 0.03, 'kelterChannelhband': 0.03, 'kelterchannellband': 0.03,
        'wpr': 0.05, 'uo': 0.05
    },
    'THETAUSDT-indicators': {
        'rsi': 0.12, 'stoch_k': 0.04, 'stoch_d': 0.04, 'macd': 0.13, 'ao': 0.06,
        'cci': 0.05, 'ema_13': 0.06, 'sma': 0.06, 'psar': 0.06, 'roc': 0.05,
        'obv': 0.09, 'adi': 0.06, 'atr': 0.07, 'high_bbands': 0.03, 'low_bbands': 0.03,
        'donc_chan_high': 0.03, 'donc_chan_low': 0.03, 'kelterChannelhband': 0.03, 'kelterchannellband': 0.03,
        'wpr': 0.05, 'uo': 0.05
    },
    'UMAUSDT-indicators': {
        'rsi': 0.12, 'stoch_k': 0.04, 'stoch_d': 0.04, 'macd': 0.13, 'ao': 0.06,
        'cci': 0.05, 'ema_13': 0.06, 'sma': 0.06, 'psar': 0.06, 'roc': 0.05,
        'obv': 0.09, 'adi': 0.06, 'atr': 0.07, 'high_bbands': 0.03, 'low_bbands': 0.03,
        'donc_chan_high': 0.03, 'donc_chan_low': 0.03, 'kelterChannelhband': 0.03, 'kelterchannellband': 0.03,
        'wpr': 0.05, 'uo': 0.05
    },
    'UNIBTC-indicators': {
        'rsi': 0.12, 'stoch_k': 0.04, 'stoch_d': 0.04, 'macd': 0.13, 'ao': 0.06,
        'cci': 0.05, 'ema_13': 0.06, 'sma': 0.06, 'psar': 0.06, 'roc': 0.05,
        'obv': 0.09, 'adi': 0.06, 'atr': 0.07, 'high_bbands': 0.03, 'low_bbands': 0.03,
        'donc_chan_high': 0.03, 'donc_chan_low': 0.03, 'kelterChannelhband': 0.03, 'kelterchannellband': 0.03,
        'wpr': 0.05, 'uo': 0.05
    },
    'UNIETH-indicators': {
        'rsi': 0.12, 'stoch_k': 0.04, 'stoch_d': 0.04, 'macd': 0.13, 'ao': 0.06,
        'cci': 0.05, 'ema_13': 0.06, 'sma': 0.06, 'psar': 0.06, 'roc': 0.05,
        'obv': 0.09, 'adi': 0.06, 'atr': 0.07, 'high_bbands': 0.03, 'low_bbands': 0.03,
        'donc_chan_high': 0.03, 'donc_chan_low': 0.03, 'kelterChannelhband': 0.03, 'kelterchannellband': 0.03,
        'wpr': 0.05, 'uo': 0.05
    },
    'UNIUSDT-indicators': {
        'rsi': 0.13, 'stoch_k': 0.04, 'stoch_d': 0.04, 'macd': 0.13, 'ao': 0.06,
        'cci': 0.05, 'ema_13': 0.06, 'sma': 0.06, 'psar': 0.06, 'roc': 0.05,
        'obv': 0.09, 'adi': 0.06, 'atr': 0.07, 'high_bbands': 0.03, 'low_bbands': 0.03,
        'donc_chan_high': 0.03, 'donc_chan_low': 0.03, 'kelterChannelhband': 0.03, 'kelterchannellband': 0.03,
        'wpr': 0.05, 'uo': 0.05
    },
    'SOLETH-indicators': {
        'rsi': 0.12, 'stoch_k': 0.04, 'stoch_d': 0.04, 'macd': 0.13, 'ao': 0.06,
        'cci': 0.05, 'ema_13': 0.06, 'sma': 0.06, 'psar': 0.06, 'roc': 0.05,
        'obv': 0.09, 'adi': 0.06, 'atr': 0.07, 'high_bbands': 0.03, 'low_bbands': 0.03,
        'donc_chan_high': 0.03, 'donc_chan_low': 0.03, 'kelterChannelhband': 0.03, 'kelterchannellband': 0.03,
        'wpr': 0.05, 'uo': 0.05
    },
    'TRBUSDT-indicators': {
        'rsi': 0.12, 'stoch_k': 0.04, 'stoch_d': 0.04, 'macd': 0.13, 'ao': 0.06,
        'cci': 0.05, 'ema_13': 0.06, 'sma': 0.06, 'psar': 0.06, 'roc': 0.05,
        'obv': 0.09, 'adi': 0.06, 'atr': 0.07, 'high_bbands': 0.03, 'low_bbands': 0.03,
        'donc_chan_high': 0.03, 'donc_chan_low': 0.03, 'kelterChannelhband': 0.03, 'kelterchannellband': 0.03,
        'wpr': 0.05, 'uo': 0.05
    },
    'VETUSDT-indicators': {
        'rsi': 0.13, 'stoch_k': 0.05, 'stoch_d': 0.05, 'macd': 0.14, 'ao': 0.06,
        'cci': 0.05, 'ema_13': 0.06, 'sma': 0.06, 'psar': 0.06, 'roc': 0.05,
        'obv': 0.10, 'adi': 0.06, 'atr': 0.08, 'high_bbands': 0.04, 'low_bbands': 0.04,
        'donc_chan_high': 0.04, 'donc_chan_low': 0.04, 'kelterChannelhband': 0.04, 'kelterchannellband': 0.04,
        'wpr': 0.05, 'uo': 0.05
    },
    'VTHOUSDT-indicators': {
        'rsi': 0.12, 'stoch_k': 0.04, 'stoch_d': 0.04, 'macd': 0.13, 'ao': 0.06,
        'cci': 0.05, 'ema_13': 0.06, 'sma': 0.06, 'psar': 0.06, 'roc': 0.05,
        'obv': 0.09, 'adi': 0.06, 'atr': 0.07, 'high_bbands': 0.03, 'low_bbands': 0.03,
        'donc_chan_high': 0.03, 'donc_chan_low': 0.03, 'kelterChannelhband': 0.03, 'kelterchannellband': 0.03,
        'wpr': 0.05, 'uo': 0.05
    },
    'XLMBTC-indicators': {
        'rsi': 0.12, 'stoch_k': 0.04, 'stoch_d': 0.04, 'macd': 0.13, 'ao': 0.06,
        'cci': 0.05, 'ema_13': 0.06, 'sma': 0.06, 'psar': 0.06, 'roc': 0.05,
        'obv': 0.09, 'adi': 0.06, 'atr': 0.07, 'high_bbands': 0.03, 'low_bbands': 0.03,
        'donc_chan_high': 0.03, 'donc_chan_low': 0.03, 'kelterChannelhband': 0.03, 'kelterchannellband': 0.03,
        'wpr': 0.05, 'uo': 0.05
    },
    'XLMUSDT-indicators': {
        'rsi': 0.13, 'stoch_k': 0.05, 'stoch_d': 0.05, 'macd': 0.14, 'ao': 0.06,
        'cci': 0.05, 'ema_13': 0.06, 'sma': 0.06, 'psar': 0.06, 'roc': 0.05,
        'obv': 0.10, 'adi': 0.06, 'atr': 0.08, 'high_bbands': 0.04, 'low_bbands': 0.04,
        'donc_chan_high': 0.04, 'donc_chan_low': 0.04, 'kelterChannelhband': 0.04, 'kelterchannellband': 0.04,
        'wpr': 0.05, 'uo': 0.05
    },
    'XMRETH-indicators': {
        'rsi': 0.12, 'stoch_k': 0.04, 'stoch_d': 0.04, 'macd': 0.13, 'ao': 0.06,
        'cci': 0.05, 'ema_13': 0.06, 'sma': 0.06, 'psar': 0.06, 'roc': 0.05,
        'obv': 0.09, 'adi': 0.06, 'atr': 0.07, 'high_bbands': 0.03, 'low_bbands': 0.03,
        'donc_chan_high': 0.03, 'donc_chan_low': 0.03, 'kelterChannelhband': 0.03, 'kelterchannellband': 0.03,
        'wpr': 0.05, 'uo': 0.05
    },
    'XMRUSDT-indicators': {
        'rsi': 0.12, 'stoch_k': 0.04, 'stoch_d': 0.04, 'macd': 0.13, 'ao': 0.06,
        'cci': 0.05, 'ema_13': 0.06, 'sma': 0.06, 'psar': 0.06, 'roc': 0.05,
        'obv': 0.09, 'adi': 0.06, 'atr': 0.07, 'high_bbands': 0.03, 'low_bbands': 0.03,
        'donc_chan_high': 0.03, 'donc_chan_low': 0.03, 'kelterChannelhband': 0.03, 'kelterchannellband': 0.03,
        'wpr': 0.05, 'uo': 0.05
    },
    'XRPBTC-indicators': {
        'rsi': 0.12, 'stoch_k': 0.04, 'stoch_d': 0.04, 'macd': 0.13, 'ao': 0.06,
        'cci': 0.05, 'ema_13': 0.06, 'sma': 0.06, 'psar': 0.06, 'roc': 0.05,
        'obv': 0.09, 'adi': 0.06, 'atr': 0.07, 'high_bbands': 0.03, 'low_bbands': 0.03,
        'donc_chan_high': 0.03, 'donc_chan_low': 0.03, 'kelterChannelhband': 0.03, 'kelterchannellband': 0.03,
        'wpr': 0.05, 'uo': 0.05
    },
    'XRPUSDT-indicators': {
        'rsi': 0.13, 'stoch_k': 0.05, 'stoch_d': 0.05, 'macd': 0.14, 'ao': 0.06,
        'cci': 0.05, 'ema_13': 0.06, 'sma': 0.06, 'psar': 0.06, 'roc': 0.05,
        'obv': 0.10, 'adi': 0.06, 'atr': 0.08, 'high_bbands': 0.04, 'low_bbands': 0.04,
        'donc_chan_high': 0.04, 'donc_chan_low': 0.04, 'kelterChannelhband': 0.04, 'kelterchannellband': 0.04,
        'wpr': 0.05, 'uo': 0.05
    },
    'XTZUSDT-indicators': {
        'rsi': 0.12, 'stoch_k': 0.04, 'stoch_d': 0.04, 'macd': 0.13, 'ao': 0.06,
        'cci': 0.05, 'ema_13': 0.06, 'sma': 0.06, 'psar': 0.06, 'roc': 0.05,
        'obv': 0.09, 'adi': 0.06, 'atr': 0.07, 'high_bbands': 0.03, 'low_bbands': 0.03,
        'donc_chan_high': 0.03, 'donc_chan_low': 0.03, 'kelterChannelhband': 0.03, 'kelterchannellband': 0.03,
        'wpr': 0.05, 'uo': 0.05
    },
    'YFIBTC-indicators': {
        'rsi': 0.12, 'stoch_k': 0.04, 'stoch_d': 0.04, 'macd': 0.13, 'ao': 0.06,
        'cci': 0.05, 'ema_13': 0.06, 'sma': 0.06, 'psar': 0.06, 'roc': 0.05,
        'obv': 0.09, 'adi': 0.06, 'atr': 0.07, 'high_bbands': 0.03, 'low_bbands': 0.03,
        'donc_chan_high': 0.03, 'donc_chan_low': 0.03, 'kelterChannelhband': 0.03, 'kelterchannellband': 0.03,
        'wpr': 0.05, 'uo': 0.05
    },
    'YFIUSDT-indicators': {
        'rsi': 0.13, 'stoch_k': 0.05, 'stoch_d': 0.05, 'macd': 0.14, 'ao': 0.06,
        'cci': 0.05, 'ema_13': 0.06, 'sma': 0.06, 'psar': 0.06, 'roc': 0.05,
        'obv': 0.10, 'adi': 0.06, 'atr': 0.08, 'high_bbands': 0.04, 'low_bbands': 0.04,
        'donc_chan_high': 0.04, 'donc_chan_low': 0.04, 'kelterChannelhband': 0.04, 'kelterchannellband': 0.04,
        'wpr': 0.05, 'uo': 0.05
    },
    'ZECETH-indicators': {
        'rsi': 0.12, 'stoch_k': 0.04, 'stoch_d': 0.04, 'macd': 0.13, 'ao': 0.06,
        'cci': 0.05, 'ema_13': 0.06, 'sma': 0.06, 'psar': 0.06, 'roc': 0.05,
        'obv': 0.09, 'adi': 0.06, 'atr': 0.07, 'high_bbands': 0.03, 'low_bbands': 0.03,
        'donc_chan_high': 0.03, 'donc_chan_low': 0.03, 'kelterChannelhband': 0.03, 'kelterchannellband': 0.03,
        'wpr': 0.05, 'uo': 0.05
    },
    'ZECUSDT-indicators': {
        'rsi': 0.13, 'stoch_k': 0.05, 'stoch_d': 0.05, 'macd': 0.14, 'ao': 0.06,
        'cci': 0.05, 'ema_13': 0.06, 'sma': 0.06, 'psar': 0.06, 'roc': 0.05,
        'obv': 0.10, 'adi': 0.06, 'atr': 0.08, 'high_bbands': 0.04, 'low_bbands': 0.04,
        'donc_chan_high': 0.04, 'donc_chan_low': 0.04, 'kelterChannelhband': 0.04, 'kelterchannellband': 0.04,
        'wpr': 0.05, 'uo': 0.05
    },
    'ZILETH-indicators': {
        'rsi': 0.12, 'stoch_k': 0.04, 'stoch_d': 0.04, 'macd': 0.13, 'ao': 0.06,
        'cci': 0.05, 'ema_13': 0.06, 'sma': 0.06, 'psar': 0.06, 'roc': 0.05,
        'obv': 0.09, 'adi': 0.06, 'atr': 0.07, 'high_bbands': 0.03, 'low_bbands': 0.03,
        'donc_chan_high': 0.03, 'donc_chan_low': 0.03, 'kelterChannelhband': 0.03, 'kelterchannellband': 0.03,
        'wpr': 0.05, 'uo': 0.05
    },
    'ZILUSDT-indicators': {
        'rsi': 0.13, 'stoch_k': 0.05, 'stoch_d': 0.05, 'macd': 0.14, 'ao': 0.06,
        'cci': 0.05, 'ema_13': 0.06, 'sma': 0.06, 'psar': 0.06, 'roc': 0.05,
        'obv': 0.10, 'adi': 0.06, 'atr': 0.08, 'high_bbands': 0.04, 'low_bbands': 0.04,
        'donc_chan_high': 0.04, 'donc_chan_low': 0.04, 'kelterChannelhband': 0.04, 'kelterchannellband': 0.04,
        'wpr': 0.05, 'uo': 0.05
    },
    'ZRXETH-indicators': {
        'rsi': 0.12, 'stoch_k': 0.04, 'stoch_d': 0.04, 'macd': 0.13, 'ao': 0.06,
        'cci': 0.05, 'ema_13': 0.06, 'sma': 0.06, 'psar': 0.06, 'roc': 0.05,
        'obv': 0.09, 'adi': 0.06, 'atr': 0.07, 'high_bbands': 0.03, 'low_bbands': 0.03,
        'donc_chan_high': 0.03, 'donc_chan_low': 0.03, 'kelterChannelhband': 0.03, 'kelterchannellband': 0.03,
        'wpr': 0.05, 'uo': 0.05
    },
    'ZRXUSDT-indicators': {
        'rsi': 0.13, 'stoch_k': 0.05, 'stoch_d': 0.05, 'macd': 0.14, 'ao': 0.06,
        'cci': 0.05, 'ema_13': 0.06, 'sma': 0.06, 'psar': 0.06, 'roc': 0.05,
        'obv': 0.10, 'adi': 0.06, 'atr': 0.08, 'high_bbands': 0.04, 'low_bbands': 0.04,
        'donc_chan_high': 0.04, 'donc_chan_low': 0.04, 'kelterChannelhband': 0.04, 'kelterchannellband': 0.04,
        'wpr': 0.05, 'uo': 0.05
    }
    # Continue adding more symbols with updated weights...
}

filenames = [filename for filename in os.listdir('C:/Users/ahmed/VSCode/flask_server/') if filename.endswith('indicators')]

path = filenames[0]

for file in filenames:
    os.chdir(path=path)
    csv_files = [csv for csv in os.listdir(path=path)]
    with open(csv in csv_files, 'a+') as csv:
        df = pd.read_csv(csv)

        
        # Bucketing Logic

        rsi_score = 0

        if df['rsi'] > 70:
            rsi_score += 2 # Overbought, Strong Buy
        elif df['rsi'] < 30:
            rsi_score -= 2 # Oversold, Strong Sell
        elif 50 < df['rsi'] <= 70:
            rsi_score += 1 # Buy
        elif 30 < df['rsi'] <= 50:
            rsi_score -= 1 # Neutral/Sell
        
        df['rsi_score'] = rsi_score

        stoch_score = 0

        stoch_score = stoch_score + 1 if df['stoch_k'] > df['stoch_d'] else stoch_score = stoch_score - 1
            # Momentum is up, buy signal
         # Momentum is down, sell signal

        macd_score = 0
        macd_score = macd_score + 1 if df['macd'] > df['macd_signal'] else macd_score = macd_score - 1
        cci_score = 0
        cci_score = cci_score + 1 if df['cci'] > 100 else cci_score = cci_score - 1
        ao_score = 0
        ao_score = ao_score + 1 if df['ao'] > 0 else ao_score = ao_score - 1 # Bullish or Bearish Trend
        bull_score = 0
        bull_score = bull_score + 1 if df['bull_power'] > 0 and df['bear_power'] < 0 else bull_score = bull_score - 1 # Bullish or Bearish Trend
        wpr_score = 0
        wpr_score = wpr_score + 1 if df['wpr'] > -20 else wpr_score = wpr_score - 1 # Strong Buy or Strong Sell
        uo_score = 0
        uo_score = uo_score + 1 if df['uo'] > 50 else uo_score = uo_score - 1
        bbands = 0
        if df['high_bbands'] == 1:
            bbands += 1
        elif df['low_bbands'] == 1:
            bbands -= 1
        ema_score = 0
        if df['Close'] > df['ema_13']:
            ema_score += 1
        else: 
            ema_score -= 1
        short_mom_score = 0
        if df['short_term_mom'] > 0:
            short_mom_score += 1
        else:
            short_mom_score -= 1
        middle_term_score = 0
        if df['middle_term_mom'] > 0:
            middle_term_score += 1
        else:
            middle_term_score -= 1
        long_term_score = 0
        if df['long_term_mom'] > 0:
            long_term_score += 1
        else:
            long_term_score -= 1
        roc_score = 0
        if df['roc'] > 0:
            roc_score += 1
        else:
            roc_score -= 1
        psar_score = 0
        if df['Close'] > df['psar']:
            psar_score += 1
        else: 
            psar_score -= 1
        atr_score = 0
        if df['atr'] > df['atr'].mean():
            atr_score += 1
        obv_score = 0
        if df['obv'] > df['obv'].shift(1):
            obv_score += 1
        else:
            obv_score -= 1
        donc_chan_score = 0
        if df['Close'] > df['donc_chan_high']:
            donc_chan_score += 1
        elif df['Close'] < df['donc_chan_low']:
            donc_chan_score -= 1
        kel_score = 0
        if df['Close'] > df['kel_high']:
            kel_score += 1
        elif df['Close'] < df['kel_low']:
            kel_score -= 1
        

        total_score = kel_score + donc_chan_score + obv_score + ao_score + stoch_score + uo_score + atr_score + cci_score + ema_score + roc_score + rsi_score + wpr_score + bull_score + macd_score + psar_score + long_term_score + short_mom_score + middle_term_score

    if total_score > 8:
        print('Strong Buy')
    elif 4 <= total_score < 8:
        print('Buy')
    elif -3 <= total_score < 4:
        print('Neutral')
    elif -7 <= total_score < -3:
        print('Sell')
    else:
        print('Strong Sell')

        








        


