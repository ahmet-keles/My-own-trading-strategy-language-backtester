import os
import yfinance as yf

target_folder = 'data'
file_name = f"SPY_10y.csv"
full_path = os.path.join(target_folder, file_name)

os.makedirs(f'{target_folder}', exist_ok=True)

ticker_data = yf.download('SPY', period='10y', auto_adjust=True, rounding=False, multi_level_index=False)

if not ticker_data.empty:
    ticker_data.to_csv(full_path)
    print(f"Success! Data saved to: {full_path}")
else:
    print("No data found for the specified parameters.")
