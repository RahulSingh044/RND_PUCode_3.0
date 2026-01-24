import re


def clean_text(text: str) -> str:
    """
    Light, meaning-preserving text normalization.
    """

    if not text or not text.strip():
        return ""

    text = text.lower()

    # Remove URLs
    text = re.sub(r"http\S+|www\S+", "", text)

    # Remove excessive punctuation (keep ! ? .)
    text = re.sub(r"[^\w\s!?\.]", "", text)

    # Normalize whitespace
    text = re.sub(r"\s+", " ", text).strip()

    return text
