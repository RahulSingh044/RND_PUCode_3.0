from app.utils.text_cleaner import clean_text
from app.nlp.sentiment import get_sentiment
from app.nlp.aspects import extract_aspects
from app.nlp.severity import detect_severity


def analyze_feedback(text: str) -> dict:
    """
    Analyze a single feedback text and return structured NLP signals.
    This function must NEVER crash.
    """

    if not text or not text.strip():
        return {
            "sentiment": 0.0,
            "aspects": [],
            "keyPhrases": [],
            "severity": "low",
            "incidentHint": False,
            "signalStrength": 0.0
        }

    clean = clean_text(text)

    sentiment = get_sentiment(clean)
    aspects, phrases = extract_aspects(clean)
    severity = detect_severity(clean, sentiment)

    # --- Signal strength (used later for weighting) ---
    signal_strength = 0.0
    if severity == "high":
        signal_strength += 0.6
    if sentiment < -0.4:
        signal_strength += min(abs(sentiment), 0.4)

    signal_strength = round(min(signal_strength, 1.0), 3)

    # --- Smarter incident hint ---
    incident_hint = (
        severity == "high" or
        (sentiment < -0.6 and len(aspects) > 0)
    )

    return {
        "sentiment": round(sentiment, 3),
        "aspects": aspects,
        "keyPhrases": phrases,
        "severity": severity,
        "incidentHint": incident_hint,
        "signalStrength": signal_strength
    }
