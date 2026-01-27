from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from functools import lru_cache


@lru_cache(maxsize=1)
def _get_analyzer():
    """
    Lazy-load sentiment analyzer.
    Safe for tests and faster startup.
    """
    return SentimentIntensityAnalyzer()


def get_sentiment(text: str) -> float:
    """
    Return compound sentiment score in range [-1, 1].
    Always safe and deterministic.
    """

    if not text or not text.strip():
        return 0.0

    analyzer = _get_analyzer()
    score = analyzer.polarity_scores(text).get("compound", 0.0)

    # Defensive clamp
    score = max(-1.0, min(score, 1.0))

    # Optional calibration hook (future)
    # score = calibrate_sentiment(score)

    return round(score, 3)
