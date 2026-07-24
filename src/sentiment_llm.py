"""
LLM-based earnings call tone scoring via the Claude API.

Requires ANTHROPIC_API_KEY set as an environment variable.

Usage:
    from sentiment_llm import score_transcript
    score = score_transcript(text, company="Target", quarter="Q1 2025")
"""

import os
import anthropic

client = anthropic.Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))

RUBRIC_PROMPT = """Read this earnings call excerpt from {company} ({quarter}).

Rate management's overall tone on a scale from -5 (very negative/defensive,
heavy hedging, downbeat guidance) to +5 (very confident/optimistic, strong
forward guidance, minimal hedging).

Consider:
- Hedging language ("we believe," "we hope," "challenging environment")
- Confidence in forward guidance
- Tone shifts between prepared remarks and the Q&A section
- Framing of any misses or headwinds mentioned

Respond with ONLY a single number (can include a decimal, e.g. 2.5), nothing else.

Transcript excerpt:
{transcript}
"""


def score_transcript(transcript_text: str, company: str, quarter: str, max_chars: int = 12000) -> float:
    """
    Scores a transcript's tone from -5 to +5 using Claude.
    Truncates very long transcripts to max_chars to keep cost/latency reasonable —
    consider passing just the prepared remarks + Q&A highlights rather than
    the full raw transcript for better signal-to-noise.
    """
    prompt = RUBRIC_PROMPT.format(
        company=company,
        quarter=quarter,
        transcript=transcript_text[:max_chars],
    )

    response = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=10,
        messages=[{"role": "user", "content": prompt}],
    )

    raw = response.content[0].text.strip()
    try:
        return float(raw)
    except ValueError:
        print(f"Unexpected response for {company} {quarter}: {raw!r}")
        return None


def score_batch(transcript_log: list, transcripts_dir: str = "data/transcripts") -> list:
    """
    transcript_log: list of dicts like
        {"ticker": "TGT", "quarter": "Q1_2025", "file": "TGT_Q1_2025.txt"}
    Returns the same list with an added "llm_sentiment" field.
    """
    results = []
    for entry in transcript_log:
        path = f"{transcripts_dir}/{entry['file']}"
        with open(path, "r", encoding="utf-8") as f:
            text = f.read()
        score = score_transcript(text, company=entry["ticker"], quarter=entry["quarter"])
        entry_with_score = {**entry, "llm_sentiment": score}
        results.append(entry_with_score)
    return results


if __name__ == "__main__":
    sample = """We're pleased to report another quarter of solid comparable sales growth,
    though we remain cautious given some softness in discretionary categories heading
    into the back half of the year."""
    print(score_transcript(sample, company="Example Retailer", quarter="Q1 2025"))
