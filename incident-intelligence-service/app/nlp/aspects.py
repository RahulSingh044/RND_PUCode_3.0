import re
import spacy
from functools import lru_cache

# Domain-aware aspect keywords
ASPECT_KEYWORDS = {
    "security": ["unsafe", "security", "guards", "panic", "emergency"],
    "crowd": ["crowded", "overcrowded", "packed", "stampede"],
    "entry": ["queue", "waiting", "gate", "entry"],
    "logistics": ["water", "toilet", "electricity", "food"],
    "delay": ["late", "delay", "postponed"]
}

# Aspect importance (used later in scoring / explainability)
ASPECT_PRIORITY = {
    "security": 3,
    "crowd": 2,
    "entry": 2,
    "delay": 1,
    "logistics": 1
}


@lru_cache(maxsize=1)
def get_nlp():
    """
    Lazy-load spaCy model.
    Prevents crashes & speeds startup.
    """
    try:
        return spacy.load("en_core_web_sm")
    except Exception:
        return None


def _tokenize(text: str) -> list[str]:
    """
    Simple tokenizer for safe keyword matching.
    """
    return re.findall(r"\b[a-z]+\b", text.lower())


def extract_aspects(text: str):
    """
    Extract aspects + meaningful noun phrases.
    """
    aspects_found = set()
    tokens = _tokenize(text)

    # --- Keyword-based aspect detection (safe) ---
    for aspect, keywords in ASPECT_KEYWORDS.items():
        for kw in keywords:
            if kw in tokens:
                aspects_found.add(aspect)

    # --- NLP phrase extraction (best-effort) ---
    phrases = []
    nlp = get_nlp()

    if nlp:
        doc = nlp(text)
        for chunk in doc.noun_chunks:
            cleaned = chunk.text.strip().lower()
            # Filter useless phrases
            if len(cleaned) > 3 and not cleaned.startswith(("the ", "a ", "an ")):
                phrases.append(cleaned)

    # Sort aspects by importance (security first)
    sorted_aspects = sorted(
        aspects_found,
        key=lambda a: ASPECT_PRIORITY.get(a, 0),
        reverse=True
    )

    return sorted_aspects, phrases
