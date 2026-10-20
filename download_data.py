import os
import yfinance as yf

target_folder = 'data'
ticker = 'SPY'
file_name = ticker + "_10y.csv"
full_path = os.path.join(target_folder, file_name)

if os.path.exists(full_path):
    print(f"File already exists at {full_path}. To get fresh data, delete {full_path} and run again.")
else:
    os.makedirs(target_folder, exist_ok=True)

    ticker_data = yf.download(ticker, period='10y', auto_adjust=True, rounding=False, multi_level_index=False)

    if not ticker_data.empty:
        ticker_data.to_csv(full_path)
        print(f"Success! Data saved to: {full_path}")
    else:
        print("No data found for the specified parameters.")

