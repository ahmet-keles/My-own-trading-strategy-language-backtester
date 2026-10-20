import numpy as np
import pandas as pd

df = pd.read_csv('data/SPY_10y.csv', index_col='Date', parse_dates=['Date'])

df['20MA'] = df['Close'].rolling(window=20).mean()
df['50MA'] = df['Close'].rolling(window=50).mean()

df = df.dropna(subset=['20MA', '50MA'])

df['Status'] = np.where(df['20MA'] > df['50MA'], 'Buy', 'Sell')
df['Trigger'] = np.where(df['Status'].ne(df['Status'].shift(1)), 'New state', 'Same state')
df.at[df.index[0], 'Trigger'] = 'Same state'

print(df.head())
print(df.tail())


