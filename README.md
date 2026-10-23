# My-own-trading-strategy-language-backtester
I'm going to attempt to build a language to test out simple trading strategies. The reason I'm attempting this is to combine my knowledge of Python, C++, and my recent exposure from my Programming Paradigms class.

Used conventionalcommits.org and Angular convention to name my commits.

## Status
Step 2 of 7 complete. Next: C++ lexer.

- [x] 1. Python prototype: load SPY data, compute moving averages, backtest a crossover strategy
- [x] 2. Language design: define what a strategy can express and write its grammar, see [docs/language.md](docs/language.md)
- [ ] 3. C++ lexer: turn strategy text into tokens
- [ ] 4. C++ parser: build a syntax tree from the tokens
- [ ] 5. C++ interpreter: run the syntax tree over price data to produce trades
- [ ] 6. C++/Python bridge: Python loads data, calls the engine, and plots results
- [ ] 7. Stats, storage and benchmarks: Sharpe, drawdown, SQLite, C++ vs. Python speed

## Strategies
Step 1 prototype (hard-coded in Python):
- Buy when the 20MA crosses above 50MA. Sell when the 20MA crosses below 50MA.
- Wait for the first crossover. Don't buy on the first day.

The same idea in my strategy language, plus a 5% stop-loss (see [docs/language.md](docs/language.md)):
`````
buy(sma(20) crosses_above sma(50))
sell(close <= 0.95 * entry_price or sma(20) crosses_below sma(50))
`````

## Assumptions
- Trades execute at the next day's open after a crossover.
- Prices are adjusted for dividends and stock splits.
- The last trade is still open when the data ends, so it has no exit.
- The equity curve values it at the last Close in the data.

## Known Limitations
- If the data contains no crossover, the backtest incorrectly holds from the second day.
- exit_price and sell-only strategies are deliberately out of version 1.

## Disclaimer
- This is just an educational simulation, not financial advice.

## Conclusions
- Using the crossover strategy with 20MA and 50MA on SPY resulted in a 117.53% return from 2017-05-04 to 2026-03-03 downloaded on 2026-10-19, while simply buying and holding resulted in 225.07% return over the same period. This is normal with such a strongly rising index, so it's a good start.
- The 117.53% figure only counts the 19 completed trades, so it stops at the last exit on 2026-03-03.