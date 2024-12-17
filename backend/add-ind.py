import os
import pandas as pd
import ta
import ta.momentum
import ta.trend
import ta.volatility
import ta.volume


filenames = [filename for filename in os.listdir("C:/Users/ahmed/VSCode/flask_server/") if filename.endswith('indicators')]
print(filename.split('-', 1)[0] for filename in filenames)
# print(len(filenames))

new_path = ""

for file in filenames:
    with open(file=file, mode='r') as infile:
        new_path = f"C:/Users/ahmed/VSCode/flask_server/{file.split('-', 1)[0]}" + "-indicators"
        if not os.path.exists(new_path):
            os.makedirs(new_path)
        
        df = pd.read_csv(infile)
        df['rsi'] = ta.momentum.RSIIndicator(close=df.Close, window=14).rsi()
        df['stoch_k'] = ta.momentum.StochasticOscillator(high=df['High'], low=df['Low'], close=df['Close'], window=14, smooth_window=3).stoch()
        df['stoch_d'] = ta.momentum.StochasticOscillator(high=df['High'], low=df['Low'], close=df['Close'], window=14, smooth_window=3).stoch_signal()
        df['cci'] = ta.trend.CCIIndicator(high=df['High'], low=df['Low'], close=df['Close'], window=20).cci()
        df['adi'] = ta.volume.AccDistIndexIndicator(high=df['High'], low=df['Low'], close=df['Close'], volume=df['Volume']).acc_dist_index()
        df['ao'] = ta.momentum.AwesomeOscillatorIndicator(high=df['High'], low=df['Low'], window1=5, window2=34).awesome_oscillator()
        df['short_term_mom'] = df['Close'] - df['Close'].shift(10)
        df['middle_term_mom'] = df['Close'] - df['Close'].shift(20)
        df['long_term_mom'] = df['Close'] - df['Close'].shift(50)
        macd = ta.trend.MACD(close=df['Close'], window_slow=26, window_fast=12, window_sign=9)
        df['macd'] = macd.macd()
        df['macd_signal'] = macd.macd_signal()
        df['macd_diff'] = macd.macd_diff()
        df['stoch_rsi_k'] = ta.momentum.StochRSIIndicator(close=df['Close'], window=14, smooth1=3, smooth2=3).stochrsi_k()
        df['stoch_rsi_d'] = ta.momentum.StochRSIIndicator(close=df['Close'], window=14, smooth1=3, smooth2=3).stochrsi_d()
        df['wpr'] = ta.momentum.WilliamsRIndicator(high=df['High'], low=df['Low'], close=df['Close'], lbp=14).williams_r()
        df['ema_13'] = ta.trend.EMAIndicator(close=df['Close'], window=13).ema_indicator()
        df['bull_power'] = df['High'] - df['ema_13']
        df['bear_power'] = df['Low'] - df['ema_13']
        df['uo'] = ta.momentum.UltimateOscillator(high=df['High'], low=df['Low'], close=df['Close'], window1=7, window2=14, window3=28).ultimate_oscillator()
        df['roc'] = ta.momentum.ROCIndicator(close=df['Close'], window=12).roc()
        df['high_bbands'] = ta.volatility.BollingerBands(close=df['Close'], window=20, window_dev=2).bollinger_hband_indicator()
        df['low_bbands'] = ta.volatility.BollingerBands(close=df['Close'], window=20, window_dev=2).bollinger_lband_indicator()
        df['sma'] = ta.trend.SMAIndicator(close=df['Close'], window=12).sma_indicator()
        df['psar'] = ta.trend.PSARIndicator(high=df['High'], low=df['Low'], close=df['Close']).psar()
        df['atr'] = ta.volatility.AverageTrueRange(high=df['High'], close=df['Close'], low=df['Low'], window=14).average_true_range()
        df['obv'] = ta.volume.OnBalanceVolumeIndicator(close=df['Close'], volume=df['Volume']).on_balance_volume()
        df['donc_chan_high'] = ta.volatility.DonchianChannel(high=df['High'], low=df['Low'], close=df['Close']).donchian_channel_hband()
        df['donc_chan_low'] = ta.volatility.DonchianChannel(high=df['High'], low=df['Low'], close=df['Close']).donchian_channel_lband()
        df['kel'] = ta.volatility.KeltnerChannel(high=df['High'], low=df['Low'], close=df['Close']).keltner_channel_hband_indicator()
        df['kel'] = ta.volatility.KeltnerChannel(high=df['High'], low=df['Low'], close=df['Close']).keltner_channel_lband_indicator()

        try:
            df.to_csv(f"{new_path}/{file.split('-', 1)[0]}" + f"-{file.split('-', 5)[4]}-indicators.csv")
        except Exception:
            print(f'Error: {Exception}')
            break


            







