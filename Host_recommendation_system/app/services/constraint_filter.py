from typing import List
from app.schemas.internal import EventContextSignals


def filter_recommendations(
    recommendations: List[str],
    context: EventContextSignals
) -> List[str]:
    """
    Filters out recommendations that are not feasible
    based on event context and inferred constraints.

    Rules applied:
    - Indoor venues → no infra expansion advice
    - Free + student events → avoid rigid enforcement language
    - Short events → avoid heavy operational changes
    """

    filtered: List[str] = []

    for rec in recommendations:
        rec_lower = rec.lower()

        # --------------------------------------------
        # Venue-based constraints
        # --------------------------------------------
        if context.is_indoor:
            if _mentions_infra_expansion(rec_lower):
                continue

        # --------------------------------------------
        # Event duration constraints
        # --------------------------------------------
        if context.duration_bucket == "short":
            if _mentions_heavy_process(rec_lower):
                continue

        # --------------------------------------------
        # Audience behavior constraints
        # --------------------------------------------
        if context.is_student_audience and context.is_free_event:
            if _mentions_strict_enforcement(rec_lower):
                rec = _soften_language(rec)

        filtered.append(rec)

    return filtered


# ==================================================
# Helper Functions
# ==================================================

def _mentions_infra_expansion(text: str) -> bool:
    """
    Detects recommendations that suggest physical expansion
    which is usually impossible for indoor venues.
    """
    infra_keywords = [
        "add gate",
        "add entry",
        "extra gate",
        "add chairs",
        "expand seating",
        "new entry",
        "additional exit",
        "extend hall"
    ]
    return any(keyword in text for keyword in infra_keywords)


def _mentions_heavy_process(text: str) -> bool:
    """
    Detects overly heavy or disruptive processes
    unsuitable for short events.
    """
    heavy_keywords = [
        "multiple rehearsals",
        "full dry run",
        "extended briefing",
        "long coordination meeting"
    ]
    return any(keyword in text for keyword in heavy_keywords)


def _mentions_strict_enforcement(text: str) -> bool:
    """
    Detects language that may feel too rigid
    for free/student-heavy events.
    """
    strict_keywords = [
        "strictly enforce",
        "deny entry",
        "penalty",
        "ban",
        "block entry"
    ]
    return any(keyword in text for keyword in strict_keywords)


def _soften_language(text: str) -> str:
    """
    Softens overly strict language to be host-friendly.
    """
    replacements = {
        "strictly enforce": "gently encourage",
        "deny entry": "discourage late entry",
        "block entry": "limit entry temporarily",
        "penalty": "guideline"
    }

    for k, v in replacements.items():
        text = text.replace(k, v)

    return text
