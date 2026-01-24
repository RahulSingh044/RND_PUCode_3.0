def clamp(value: float, min_v: float = 0.0, max_v: float = 1.0) -> float:
    return max(min_v, min(value, max_v))


def update_rolling_average(
    old_avg: float,
    count: int,
    new_score: float,
    decay: float = 1.0
):
    """
    Update rolling average with optional decay.
    decay < 1.0 slowly forgets older events.
    """

    old_avg = clamp(old_avg)
    new_score = clamp(new_score)
    count = max(count, 0)

    if count == 0:
        return new_score

    weighted_old = old_avg * count * decay
    weighted_new = new_score

    new_avg = (weighted_old + weighted_new) / (count * decay + 1)
    return round(clamp(new_avg), 3)


def classify_risk(avg_score: float) -> str:
    """
    Stable risk classification with small hysteresis.
    """
    avg_score = clamp(avg_score)

    if avg_score >= 0.72:
        return "high"
    if avg_score >= 0.42:
        return "medium"
    return "low"
