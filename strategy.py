import numpy as np
import pandas as pd

df = pd.read_csv('data/SPY_10y.csv', index_col='Date', parse_dates=['Date'])

df['sma_20'] = df['Close'].rolling(window=20).mean()
df['sma_50'] = df['Close'].rolling(window=50).mean()

df = df.dropna(subset=['sma_20', 'sma_50'])

df['signal'] = np.where(df['sma_20'] > df['sma_50'], 1, 0)
df['crossover'] = df['signal'].diff()

df.at[df.index[0], 'crossover'] = 0

print(df['crossover'].value_counts())
# print(df.head())
print(df.tail(100))


