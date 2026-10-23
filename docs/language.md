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
- Commas separate call arguments and are looser than every operator: each argument is a full expression (see `arguments` in the grammar).
- `a != b != c` means `a != b and b != c`, not `a != c`.
- `(a crosses_above b) < close` compares true/false to a number: a type error (caught in Semantics, not by the grammar).
- `not` sits above comparisons, so `1 + not x` and `a == not b` are syntax errors. Write `a == (not b)`.

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
- Any word that is not a keyword, number or symbol: indicator names (`sma`) and built-in values (`close`). To the lexer, `close` and `sma` are both just `IDENTIFIER`. Whether a name is a known built-in or indicator is checked later (see Semantics).
- Characters: letters, digits and underscores; can't start with a digit. `ema12` works, `12ema` doesn't.
- Case-sensitive: `Close` is not `close`, so it fails the unknown-name check.
- Keywords are reserved: the lexer checks each word against the keyword list first.

### Special tokens (not typed characters)
- `EOF`

### Ignored
- Whitespace: spaces, tabs and newlines. Newlines carry no meaning, so a strategy can be written on one line or many.
- The lexer still counts lines and columns for error messages.
- Comments: `#` to the end of the line

### Lexer errors
The lexer reports the first error and stops, with line and column. Cases:
- Unrecognized character (for example `@`, `$`)
- Lone `=` ("did you mean `==`?")
- Lone `!` ("use `not`")
- Malformed numbers (`.5`, `5.`, `008`)

Unbalanced parentheses are reported by the parser, not the lexer.

## 3. Grammar
Notation: `{ ... }` means zero or more, `[ ... ]` means optional, `|` means "or", and quoted text is a literal token.

```
strategy   = buy_rule [ sell_rule ] EOF ;

buy_rule   = "buy"  "(" expression ")" ;
sell_rule  = "sell" "(" expression ")" ;

expression = or_expr ;
or_expr    = and_expr { "or" and_expr } ;
and_expr   = not_expr { "and" not_expr } ;
not_expr   = "not" not_expr | comparison ;
comparison = sum { comp_op sum } ;
comp_op    = "<" | "<=" | ">" | ">=" | "==" | "!="
           | "crosses_above" | "crosses_below" ;
sum        = term { ( "+" | "-" ) term } ;
term       = unary { ( "*" | "/" ) unary } ;
unary      = "-" unary | primary ;

primary    = NUMBER
           | IDENTIFIER [ "(" [ arguments ] ")" ]
           | "(" expression ")" ;
arguments  = expression { "," expression } ;
```

Notes:
- One rule per precedence level, loosest at the top. Each rule is written in terms of the next-tighter one.
- `not_expr` and `unary` refer to themselves, so `not not x` and `--a` stack.
- `comparison` is a flat list. The Python-style meaning of chains (`a < b < c` means `a < b and b < c`) is applied when the parser builds the tree.
- Newlines never appear in the grammar. Rules can be on one line or several.
- `arguments` is optional, so `sma()` parses and `sma(20,)` is a syntax error. Argument counts are checked in Semantics.
- A name followed by `(` is a call. A bare name is a value.
- Structure errors the grammar enforces:
    - `buy` is required and comes first ("expected `buy` rule" for an empty file or a sell-only strategy).
    - At most one `sell`, after `buy`.
    - A second `buy` or `sell` is a syntax error ("expected end of strategy").
    - A missing `)` is "expected `)`". An extra `)` is "expected end of strategy".

## 4. Semantics (checked before the backtest, with line and column)
- Strategy structure (exactly one `buy`, at most one `sell`, `buy` first, no sell-only strategies) is enforced by the grammar (`strategy` rule). No `sell` means the position is held.
- Built-in names: `open`, `high`, `low`, `close`, `entry_price`. Any other bare name is an error.
- `entry_price` is allowed only inside `sell`.
- Indicator table (argument count, kinds, defaults):
    - `sma`: optional `series` source (default `close`), then required `integer` period (minimum 1). `sma(20)` means `sma(close, 20)`.
- Argument kinds: `number`, `series`, `integer`.
    - `integer` slots must be a plain integer literal: `20` is valid; `20.0`, `10 + 10` and `-5` are rejected.
    - `series` slots can hold any expression.
- If an indicator has an optional source, it is always the first argument.
- Type errors, such as comparing a true/false value to a number, are rejected.
- A period longer than the data is not an error: the indicator is NaN everywhere.
- Timing: conditions use the day's full bar; trades happen at the next day's Open. A stop-loss can fill below its threshold if the price gaps down overnight.

## 5. Example strategy
Two lines:
```
buy(sma(20) crosses_above sma(50))
sell(close <= 0.95 * entry_price or sma(20) crosses_below sma(50))
```

The same strategy on one line (newlines don't matter):
```
buy(sma(20) crosses_above sma(50)) sell(close <= 0.95 * entry_price or sma(20) crosses_below sma(50))
```

## 6. Open questions and deferred ideas
- Sell-only strategies
- `exit_price` (needs a missing-value rule, for example three-valued logic or `else` fallback)
- More indicators (RSI, EMA)