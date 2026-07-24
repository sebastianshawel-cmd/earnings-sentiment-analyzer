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
- [ ] Transcripts collected
- [ ] Lexicon scoring run
- [ ] LLM scoring run
- [ ] Price data pulled
- [ ] Analysis + charts complete
- [ ] Writeup finished

## Findings
(fill in once analysis is done — include the honest result, even if it's a null finding)
