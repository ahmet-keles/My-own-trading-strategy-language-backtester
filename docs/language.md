# Strategy language design (draft)

## 1. Precedence table
Tightest at the top, loosest at the bottom. Operators that share a level go on the same row.

| Level | Operators | Associativity | Example and how it groups |
|---|---|---|---|
| 0 (tightest) | `( )` grouping, `name( )` call | n/a (bracketing) | `(a + b) * c` → the sum is computed first<br>`sma(20)` → call `sma` with argument `20` |
| 1 | unary `-` | prefix, right to left (can stack) | `--a` → `-(-a)`<br>`-a * b` → `(-a) * b` |
| 2 | `*`, `/` | left | `a / b * c` → `(a / b) * c` |
| 3 | `+`, `-` | left | `a - b - c` → `(a - b) - c`<br>`a + b * c` → `a + (b * c)` |
| 4 | `<`, `<=`, `>`, `>=`, `==`, `!=`, `crosses_above`, `crosses_below` | chain (Python-style: `a < b < c` means `a < b and b < c`) | `a < b < c` → `a < b and b < c`<br>`sma(20) crosses_above sma(50) < close` → `sma(20) crosses_above sma(50) and sma(50) < close` |
| 5 | `not` | prefix, right to left (can stack) | `not not x` → `not (not x)`<br>`not close < 100` → `not (close < 100)` |
| 6 | `and` | left | `a and b and c` → `(a and b) and c`<br>`not a and b` → `(not a) and b` |
| 7 (loosest) | `or` | left | `a or b and c` → `a or (b and c)` |

Notes:
- Commas separating call arguments are looser than every operator.
- `a != b != c` means `a != b and b != c`, not `a != c`.
- `(a crosses_above b) < close` compares true/false to a number: a type error.

## 2. Token list

### Keywords (reserved)
- `buy`, `sell`, `not`, `and`, `or`, `crosses_above`, `crosses_below`

### Operators
- Single-character: `+`, `-`, `*`, `/`, `<`, `>`
- Multi-character: `<=`, `>=`, `==`, `!=`

### Punctuation
- `(`, `)`, `,`

### Literals
- Numbers:
    - Integers and decimals (`20`, `0.95`, `3.5`)
    - A decimal needs digits on both sides of the dot, so `.5` and `5.` are lexer errors
    - No negative literals: `-5` is unary `-` applied to `5`
    - No `5%` form
    - No extra leading zeros: `008` is an error, but `0` and `0.95` are allowed

### Identifiers
- Any word that is not a keyword, number or symbol: indicator names (`sma`) and built-in values (`close`).
- Characters: letters, digits and underscores; can't start with a digit. `ema12` works, `12ema` doesn't.
- Case-sensitive: `Close` is not `close`, so it fails the unknown-name check.
- Keywords are reserved: the lexer checks each word against the keyword list first.

### Special tokens (not typed characters)
- `NEWLINE`: produced only at parenthesis depth 0
- `EOF`

### Ignored
- Whitespace: spaces and tabs
- Newlines: significant at depth 0 (they separate rules), ignored while a `(` is open
- Comments: `#` to the end of the line

### Lexer errors
The lexer reports the first error and stops, with line and column. Cases:
- Unrecognized character (for example `@`, `$`)
- Lone `=` ("did you mean `==`?")
- Lone `!` ("use `not`")
- Malformed numbers (`.5`, `5.`, `008`)
- `)` with no matching `(`
- End of file with a `(` still open

## 3. Grammar
(to do)

## 4. Semantics (checked before the backtest, with line and column)
- Exactly one `buy` rule, at most one `sell` rule. A sell-only strategy is invalid. No `sell` means the position is held.
- Built-in names: `open`, `high`, `low`, `close`, `entry_price`. Any other bare name is an error.
- `entry_price` is allowed only inside `sell`.
- A name followed by `(` is an indicator call. A bare name is a value.
- Indicator table (argument count, kinds, defaults):
    - `sma`: optional `series` source (default `close`), then required `integer` period (minimum 1). `sma(20)` means `sma(close, 20)`.
- Argument kinds: `number`, `series`, `integer`.
    - `integer` slots must be a plain integer literal: `20` is valid; `20.0`, `10 + 10` and `-5` are rejected.
    - `series` slots can hold any expression.
- If an indicator has an optional source, it is always the first argument.
- A period longer than the data is not an error: the indicator is NaN everywhere.
- Timing: conditions use the day's full bar; trades happen at the next day's Open. A stop-loss can fill below its threshold if the price gaps down overnight.

## 5. Example strategy
```
buy(sma(20) crosses_above sma(50))
sell(close <= 0.95 * entry_price or sma(20) crosses_below sma(50))
```

## 6. Open questions and deferred ideas
- Sell-only strategies
- `exit_price` (needs a missing-value rule, for example three-valued logic or `else` fallback)
- More indicators (RSI, EMA)