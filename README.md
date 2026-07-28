# Earnings Call Sentiment vs. Stock Returns — Retail/Consumer Sector

## Question
Does management tone on earnings calls predict forward stock returns for retail/consumer companies?

## Companies covered
Target (TGT), Walmart (WMT), Costco (COST), Home Depot (HD), Lowe's (LOW),
TJX Companies (TJX), Ross Stores (ROST), Nike (NKE), Starbucks (SBUX), Chipotle (CMG)

## Method
1. Collect earnings call transcripts (`data/transcripts/`)
2. Score sentiment two ways:
   - Loughran-McDonald finance-specific lexicon (`src/sentiment_lexicon.py`)
   - LLM-based tone scoring via Claude API (`src/sentiment_llm.py`)
3. Pull forward stock returns (1-day, 5-day, 30-day) via `src/fetch_prices.py`
4. Analyze relationship in `notebooks/analysis.ipynb`

## Setup
```bash
pip install -r requirements.txt
```

You'll also need:
- A Loughran-McDonald dictionary CSV (free download, see `src/sentiment_lexicon.py` for expected format)
- An Anthropic API key set as an environment variable if using LLM scoring:
  `export ANTHROPIC_API_KEY=your_key_here`

## Repo structure
```
data/
  transcripts/       # raw transcript text files, one per company-quarter
  processed/         # cleaned data + computed scores (CSV)
notebooks/
  analysis.ipynb      # main analysis + charts
src/
  fetch_prices.py     # pulls price data via yfinance, computes forward returns
  sentiment_lexicon.py # Loughran-McDonald based scoring
  sentiment_llm.py     # Claude API based scoring
  companies.py         # ticker list + metadata
requirements.txt
README.md
```

## Status
- [x] Transcripts collected
- [x] Lexicon scoring run
- [ ] LLM scoring run
- [x] Price data pulled
- [x] Analysis + charts complete
- [x] Writeup finished

## Findings
Across 31 earnings calls from 10 retail/consumer companies, lexicon-based sentiment showed only a weak correlation with 1-day forward returns (r = 0.157), and virtually no correlation at 5-day (r = 0.048) or 30-day (r = 0.047) horizons. Excluding three high-volatility outlier tickers (Ross Stores, Nike, Chipotle) reduced the 1-day correlation to near zero (r = 0.002), suggesting the modest overall relationship was largely driven by a small number of dramatic single-quarter reactions rather than a consistent pattern. This is broadly consistent with efficient-market behavior for large, heavily-covered companies — by the time these calls happen, much of the "surprise" has likely already been priced in through pre-call guidance and analyst previews.

