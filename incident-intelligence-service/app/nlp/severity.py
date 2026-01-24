import re

SEVERE_WORDS = {
    "unsafe",
    "danger",
    "dangerous",
    "stampede",
    "panic",
    "emergency",
    "injured",
    "injury",
    "collapse"
}


def _tokenize(text: str) -> set:
    """
    Simple, safe tokenizer.
    """
    return set(re.findall(r"\b[a-z]+\b", text.lower()))


def detect_severity(text: str, sentiment: float) -> str:
    """
    Detect severity level from text + sentiment.
    Never crashes. Always explainable.
    """

    if not text or not text.strip():
        return "low"

    tokens = _tokenize(text)

    # --- Strong safety signal ---
    severe_hits = tokens.intersection(SEVERE_WORDS)

    if severe_hits:
        # Require negative context to escalate
        if sentiment < -0.2:
            return "high"
        return "medium"

    # --- Sentiment-based fallback ---
    if sentiment < -0.7:
        return "high"

    if sentiment < -0.4:
        return "medium"

    return "low"
