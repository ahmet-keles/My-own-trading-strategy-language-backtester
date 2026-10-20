import numpy as np
import pandas as pd

df = pd.read_csv('data/SPY_10y.csv', index_col='Date', parse_dates=['Date'])

df['sma_20'] = df['Close'].rolling(window=20).mean()
df['sma_50'] = df['Close'].rolling(window=50).mean()

df = df.dropna(subset=['sma_20', 'sma_50'])

df['signal'] = np.where(df['sma_20'] > df['sma_50'], 1, 0)

df['crossover'] = df['signal'].diff()

df.at[df.index[0], 'crossover'] = 0

first_index = (df['crossover'] == 1).idxmax() # Note: if there is no crossover or +1 in the data, idxmax return the first row (see README)

df['position'] = df['signal'].shift(1)

df.loc[:first_index, 'position'] = 0

print(df['crossover'].value_counts())

first_crossover = df.index.get_loc(first_index)

print(df.iloc[first_crossover-3:first_crossover+3])


