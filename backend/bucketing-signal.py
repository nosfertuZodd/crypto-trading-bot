import os
import pandas as pd

# Symbol Weights Dictionary
symbol_weights = {
    'BTCUSDT': {
        'rsi': 0.3, 'stoch': 0.2, 'macd': 0.3, 'cci': 0.2
    },
    # Add other symbols here with respective weights
}

# Function to calculate individual indicator signals
def calculate_rsi_signal(rsi):
    return rsi.apply(lambda x: 1 if x > 70 else -1 if x < 30 else 0)

def calculate_stochastic_signal(df):
    return df.apply(lambda row: 1 if row['stoch_k'] > row['stoch_d'] else -1, axis=1)

def calculate_macd_signal(df):
    return df.apply(lambda row: 1 if row['macd'] > row['macd_signal'] else -1, axis=1)

def calculate_cci_signal(cci):
    return cci.apply(lambda x: 1 if x > 100 else -1 if x < -100 else 0)

# Function to calculate combined signal and action
def calculate_combined_signals(df, weights):
    df['combined_signal'] = (
        weights['rsi'] * df['rsi_signal'] +
        weights['stoch'] * df['stoch_signal'] +
        weights['macd'] * df['macd_signal'] +
        weights['cci'] * df['cci_signal']
    )
    df['combined_action'] = df['combined_signal'].apply(assign_combined_action)

# Function to assign combined action
def assign_combined_action(signal):
    if signal <= -0.5:
        return 'Sell'
    elif signal >= 0.5:
        return 'Buy'
    else:
        return 'Neutral'

# Directory Path
flask_server_directory = 'C:/Users/atifw/Documents/GitHub/crypto-trading-bot/backend/flask_server/'

# Process Subdirectories Ending with '-indicators'
subdirectories = [
    subdir for subdir in os.listdir(flask_server_directory) if subdir.endswith('indicators')
]

# Get the list of symbols from the weights dictionary
available_symbols = set(symbol_weights.keys())
print(f"Available symbols in symbol_weight list: {available_symbols} type: {type(available_symbols)}")

for subdir in subdirectories:
    subdir_path = os.path.join(flask_server_directory, subdir)
    # print(f"Processing directory Name: {subdir}")

    # Process CSV files in the subdirectory
    csv_files = [file for file in os.listdir(subdir_path) if file.endswith('.csv')]
    for csv_file in csv_files:
        csv_file_path = os.path.join(subdir_path, csv_file)
        # print(f"Processing file Name: {csv_file}")

        # Load DataFrame
        df = pd.read_csv(csv_file_path)
        # print(f"First few rows of {csv_file}:/n {df.head()}")

        # Extract symbol and weights from the CSV file
        symbol_from_csv = csv_file.split(' git -')[0] # Extract symbol from the filename
        print(f"Symbol from csv: {symbol_from_csv} type: {type(symbol_from_csv)}")

        # Dictionary to store the weights of the matched symbols
        weights = {}
        # Check if the symbol is available in the symbol_weights dictionary
        if symbol_from_csv in available_symbols:
            weights = symbol_weights[symbol_from_csv]
            print(f"Weights for {symbol_from_csv}: {weights}")
        else:
            print(f"Symbol {symbol_from_csv} not found in symbol_weights dictionary")

        # Now, `weights` will contain the weights dictionary for the matched symbol
        print("Stored weights:", weights)

        # Calculate individual indicator signals
        df['rsi_signal'] = calculate_rsi_signal(df['rsi'])
        df['stoch_signal'] = calculate_stochastic_signal(df)
        df['macd_signal'] = calculate_macd_signal(df)
        df['cci_signal'] = calculate_cci_signal(df['cci'])

        # Calculate combined signals and actions
        calculate_combined_signals(df, weights)

        # Save to CSV
        output_file = os.path.join(subdir_path, f"{symbol_from_csv}_combined_signals.csv")
        df.to_csv(output_file, index=False)

        print(f"Processed signals for {symbol_from_csv} and saved to {output_file}")
