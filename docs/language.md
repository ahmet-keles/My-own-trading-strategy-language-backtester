# Strategy language: precedence and tokens (draft)

## 1. Precedence table
Tightest at the top, loosest at the bottom. Operators that share a level go on the same row.
Add or remove rows as needed.

| Level | Operators | Associativity (left / right / chain) | Example and how it groups |
|---|---|---|---|
| 1 (tightest) | | | |
| 2 | | | |
| 3 | | | |
| 4 | | | |
| 5 | | | |
| 6 | | | |
| 7 | | | |
| 8 (loosest) | | | |

Check: does every operator from my decisions appear exactly once?

## 2. Token list

### Keywords (reserved words)
-

### Built-in names
-

### Operators
- Single-character:
- Multi-character:
- Multi-word:

### Punctuation
-

### Literals
- Numbers: (integers? decimals? both? is `.5` allowed? is `5%` allowed?)

### Identifiers
- What counts as a name (for example, an indicator like `sma`)?
- Allowed characters:
- Can it clash with a keyword?

### Ignored
- Whitespace:
- Newlines:
- Comments? (yes or no, and what syntax)

## 3. Open questions I found while writing this
-