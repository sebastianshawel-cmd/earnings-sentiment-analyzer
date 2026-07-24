"""
Loughran-McDonald lexicon-based sentiment scoring for financial text.

Download the dictionary CSV from the Loughran-McDonald master dictionary
(search "Loughran McDonald Master Dictionary" — Notre Dame hosts the free
academic version). Expected columns: Word, Positive, Negative, Uncertainty
(nonzero values indicate the word belongs to that category).

Usage:
    from sentiment_lexicon import LexiconScorer
    scorer = LexiconScorer("data/loughran_mcdonald_dict.csv")
    score = scorer.score(transcript_text)
"""

import re
import pandas as pd


class LexiconScorer:
    def __init__(self, dict_path: str):
        lm = pd.read_csv(dict_path)
        lm.columns = [c.strip() for c in lm.columns]
        self.positive_words = set(lm[lm["Positive"] > 0]["Word"].str.lower())
        self.negative_words = set(lm[lm["Negative"] > 0]["Word"].str.lower())
        self.uncertainty_words = set(lm[lm["Uncertainty"] > 0]["Word"].str.lower())

    def score(self, text: str) -> dict:
        words = re.findall(r"\b[a-z]+\b", text.lower())
        total = len(words) or 1  # avoid divide by zero

        pos_count = sum(1 for w in words if w in self.positive_words)
        neg_count = sum(1 for w in words if w in self.negative_words)
        unc_count = sum(1 for w in words if w in self.uncertainty_words)

        return {
            "word_count": total,
            "positive_pct": pos_count / total,
            "negative_pct": neg_count / total,
            "uncertainty_pct": unc_count / total,
            "net_sentiment": (pos_count - neg_count) / total,
        }


if __name__ == "__main__":
    # example — replace with your actual dictionary path
    scorer = LexiconScorer("data/loughran_mcdonald_dict.csv")
    sample = "We are pleased with strong growth, though some uncertainty remains in the back half."
    print(scorer.score(sample))
