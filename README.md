# My-own-trading-strategy-language-backtester
I'm going to attempt to build a language to test out simple trading strategies. The reason I'm attempting this is to combine my knowledge of Python, C++, and my recent exposure from my Programming Paradigms class.

Used conventionalcommits.org and Angular convention to name my commits.

## Status
Step 1 of 7 complete. Next: designing the language.

- [x] 1. Python prototype: load SPY data, compute moving averages, backtest a crossover strategy
- [ ] 2. Language design: define what a strategy can express and write its grammar
- [ ] 3. C++ lexer: turn strategy text into tokens
- [ ] 4. C++ parser: build a syntax tree from the tokens
- [ ] 5. C++ interpreter: run the syntax tree over price data to produce trades
- [ ] 6. C++/Python bridge: Python loads data, calls the engine, and plots results
- [ ] 7. Stats, storage and benchmarks: Sharpe, drawdown, SQLite, C++ vs. Python speed

## Strategies
- Buy when the 20MA crosses above 50MA. Sell when the 20MA crosses below 50MA.
- Wait for the first crossover. Don't buy on the first day.

## Assumptions
- Trades execute at the next day's open after a crossover.
- Prices are adjusted for dividends and stock splits.
- The last trade is still open when the data ends, so it has no exit.
- The equity curve values it at the last Close in the data.

## Known Limitations
- If the data contains no crossover, the backtest incorrectly holds from the second day.

## Disclaimer
- This is just an educational simulation, not financial advice.

## Conclusions
- Using the crossover strategy with 20MA and 50MA on SPY resulted in a 117.53% return from 2017-05-04 to 2026-03-03 downloaded on 2026-10-19, while simply buying and holding resulted in 225.07% return over the same period. This is normal with such a strongly rising index, so it's a good start.
- The 117.53% figure only counts the 19 completed trades, so it stops at the last exit on 2026-03-03.