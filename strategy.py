import numpy as np
import pandas as pd

df = pd.read_csv('data/SPY_10y.csv', index_col='Date', parse_dates=['Date'])

df['sma_20'] = df['Close'].rolling(window=20).mean()
df['sma_50'] = df['Close'].rolling(window=50).mean()
df = df.dropna(subset=['sma_20', 'sma_50'])

df['signal'] = np.where(df['sma_20'] > df['sma_50'], 1, 0)
df['crossover'] = df['signal'].diff()
df.at[df.index[0], 'crossover'] = 0
first_index = (df['crossover'] == 1).idxmax() # Note: if there is no crossover or +1 in the data, idxmax returns the first row (see README)
df['position'] = df['signal'].shift(1)
df.loc[:first_index, 'position'] = 0

df['trade'] = df['position'].diff()

entry_trades = df[df['trade'] == 1].index
exit_trades = df[df['trade'] == -1].index

trade_returns = [0] * len(exit_trades)

for i in range(len(exit_trades)):
    trade_returns[i]= df.loc[exit_trades[i], 'Open'] / df.loc[entry_trades[i], 'Open'] - 1

res = 1
for i in range(len(trade_returns)):
    res *= 1 + trade_returns[i]
res -= 1

print("return: " + str(res * 100) + "%")

buy_and_hold = 1 + df.loc[exit_trades[-1], 'Open'] / df.loc[entry_trades[0], 'Open'] - 1
buy_and_hold -= 1

print("benchmark: " + str(buy_and_hold * 100) + "%")

print(str(entry_trades[0]) + " to " + str(exit_trades[-1]))
print(str(df.index[-1]))

#print(len(entry_trades))
#print(len(exit_trades))
#print(df['crossover'].value_counts())
#first_crossover = df.index.get_loc(first_index)
#print(df.iloc[first_crossover-3:first_crossover+3])


