from binance.client import Client
import pandas as pd
import datetime
from dotenv import load_dotenv
import os

# Load environment variables from.env file
load_dotenv()

# Binance API credentials
API_KEY = os.getenv('API_KEY')
API_SECRET = os.getenv('API_SECRET')

# Binance API credentials
# api_key = 'R1abV976W7rcTLAAQJpD0NVT9UyWoe6LBCAJj93750Y26Kso1j3lEB6n2rVDuxyo'
# api_secret = 'FU00rdJZd0wpxLWbca4AFAVlYmMbkon9Nzddpy2DNe2kkimSazAXvArUnqYyHOuI'


client = Client(API_KEY, API_SECRET)

# Define the symbol for BTC/USDT pair
symbols = [
 'DASHETH',
 'ZECETH',
 'NEOETH',
 'ICXETH',
 'ONTETH',
 'QTUMETH',
 'STMXETH',
 'RLCETH',
 'DENTETH',
 'BATETH'
 ]


intervals = {
    '1M': Client.KLINE_INTERVAL_1MINUTE,
    '5M': Client.KLINE_INTERVAL_5MINUTE,
    '30M': Client.KLINE_INTERVAL_30MINUTE,
    '1H': Client.KLINE_INTERVAL_1HOUR,
    '2H': Client.KLINE_INTERVAL_2HOUR,
    '6H': Client.KLINE_INTERVAL_6HOUR,
    '12H': Client.KLINE_INTERVAL_12HOUR,
    '1D': Client.KLINE_INTERVAL_1DAY,
    '3D': Client.KLINE_INTERVAL_3DAY,
    '1W': Client.KLINE_INTERVAL_1WEEK
}



# Define custom start and end time
start_time = datetime.datetime(2023, 1, 1, 0, 0, 0)
end_time = datetime.datetime.now()
for symbol in symbols:

    for interval, interval_value in intervals.items():
        klines = client.get_historical_klines(symbol=symbol, interval=interval_value, start_str=str(start_time), end_str=str(end_time))

        # Convert the data into a pandas dataframe for easier manipulation
        df_M = pd.DataFrame(klines, columns=['Open Time', 'Open', 'High', 'Low', 'Close', 'Volume', 'Close Time', 'Quote Asset Volume', 'Number of Trades', 'Taker Buy Base Asset Volume', 'Taker Buy Quote Asset Volume', 'Ignore'])


        columns_to_convert = ['Open', 'High', 'Low', 'Close', 'Volume', 'Quote Asset Volume', 'Number of Trades', 'Taker Buy Base Asset Volume', 'Taker Buy Quote Asset Volume']

        for col in columns_to_convert:
            df_M[col] = df_M[col].astype(float)

        df_M.drop(['Close Time', 'Quote Asset Volume', 'Number of Trades', 'Taker Buy Base Asset Volume', 'Taker Buy Quote Asset Volume', 'Ignore'], axis=1, inplace=True)

        df_M.to_csv(f'{symbol}-Jan2023-October-2024-{interval}.csv')
# print(df_M)