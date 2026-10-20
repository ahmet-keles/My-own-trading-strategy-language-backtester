# My-own-trading-strategy-language-backtester
I'm going to attempt to build a language to test out simple trading strategies. The reason I'm attempting this is to combine my knowledge of Python, C++, and my recent exposure from my Programming Paradigms class.

Used conventionalcommits.org and Angular convention to name my commits.

## Strategy
- Buy when the 20MA crosses above 50MA. Sell when the 20MA crosses below 50MA.
- Wait for the first crossover. Don't buy on the first day.

## Assumptions
- Trades execute at the next day's open after a crossover.

## Known Limitations
- If the data contains no crossover, the backtest incorrectly holds from the second day.