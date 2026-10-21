# My-own-trading-strategy-language-backtester
I'm going to attempt to build a language to test out simple trading strategies. The reason I'm attempting this is to combine my knowledge of Python, C++, and my recent exposure from my Programming Paradigms class.

Used conventionalcommits.org and Angular convention to name my commits.

## Strategies
- Buy when the 20MA crosses above 50MA. Sell when the 20MA crosses below 50MA.
- Wait for the first crossover. Don't buy on the first day.

## Assumptions
- Trades execute at the next day's open after a crossover.
- Prices are adjusted for dividends.

## Known Limitations
- If the data contains no crossover, the backtest incorrectly holds from the second day.

## Disclaimer
- This is just an educational simulation, not financial advice.

## Conclusions
- Using the crossover strategy with 20MA and 50MA on SPY resulted in a 117.53% return from 2017-05-04 to 2026-03-03 downloaded on 2026-10-19, while simply buying and holding resulted in 225.07% return over the same period. This is normal with such a strongly rising index, so it's a good start.