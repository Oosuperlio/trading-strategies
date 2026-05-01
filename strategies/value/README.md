# Value Investing Screener

## Overview
Value investing strategy based on classic metrics: P/E, P/B, dividend yield, and financial health.

## Metrics
- **P/E Ratio**: < 15 (value threshold)
- **P/B Ratio**: < 1.5 (asset valuation)
- **Dividend Yield**: > 3% (income generation)
- **Debt/Equity**: < 50% (financial health)
- **ROE**: > 10% (profitability)

## Target Markets
- HK: 0700 (Tencent), 3968 (CMBC), 0005 (HSBC)
- US: JPM, PG, PEP, KO

## Usage
```python
python -m strategies.value.screener --market=hk --min_pe=5 --max_pe=20
```
