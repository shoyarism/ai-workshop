# Strategy Extraction Reference

Templates for pulling strategy components from YouTube transcripts.

## Template 1: Trend-Following
```
Entry:
- Trigger: [EMA cross / breakout / RSI cross]
- Direction: [long/short/both]
- Timeframe: [5m / 15m / 1h / daily]
- Confirmation: [volume / higher-TF trend]

Exit:
- SL: [ATR x, fixed %, trailing]
- TP: [R multiple / target %]
- Exit on: [reverse signal / time]

Filters:
- Session: [ASIA/US/London]
- News filter: [yes/no]
- Position size: [fixed % / Kelly]
```

## Template 2: Mean Reversion
```
Entry:
- Indicator: [RSI < 30 / Bollinger lower]
- Reversal signal: [candle pattern]
- Timeframe: [1h+ preferred]

Exit:
- SL: [recent swing high/low]
- TP: [middle band / 50 MA]
- Time stop: [N bars]
```

## Template 3: Grid / Scalping
```
Grid:
- Levels: [10-20 grids]
- Distance: [ATR % or fixed]
- Order size per level: [fixed / declining]

Limits:
- Max orders open
- Stop if equity -X%
```

## Common YouTube-Strategy Red Flags

1. **"100% win rate"** — survivorship bias
2. **"No stop loss"** — eventual blow-up
3. **"Trade any market"** — vague filter
4. **Screenshot-only** — no methodology
5. **"Follow me on VIP"** — no public test

## Metrics to Compute

```python
# After backtest
import pandas as pd
df = trades  # dataframe with columns: pnl, ret, duration, exit_reason

print(f"Trades: {len(df)}")
print(f"Win rate: {(df.pnl > 0).mean():.1%}")
print(f"Profit factor: {df.pnl[df.pnl>0].sum() / abs(df.pnl[df.pnl<0].sum()):.2f}")
print(f"Max drawdown: {((df.pnl.cumsum() - df.pnl.cumsum().cummax()) / df.pnl.cumsum().cummax()).min():.1%}")
print(f"Sharpe (annualized): {df.pnl.mean() / df.pnl.std() * (252**0.5):.2f}")
```

## User's Baseline (ADA)

Compare against best existing:
- **ADA 15m EMA300 SL=1% TP=6% RR=1:6** → +206%, PF 1.175
- **Ada 2h ATR** → PF 2.21, +404%
