from datetime import datetime, timedelta

TIME_FORMATS = ["%H:%M", "%H:%M:%S"]


def _parse_time(t: str) -> datetime | None:
    for fmt in TIME_FORMATS:
        try:
            return datetime.strptime(t, fmt)
        except Exception:
            continue
    return None


def _to_minutes(t1: str, t2: str) -> int:
    """
    Safe difference in minutes between two times.
    Handles midnight crossover.
    """
    d1 = _parse_time(t1)
    d2 = _parse_time(t2)

    if not d1 or not d2:
        return 0

    # Handle midnight crossover
    if d2 < d1:
        d2 += timedelta(days=1)

    return int((d2 - d1).total_seconds() / 60)


def compute_schedule_delay(timing: dict) -> int:
    """
    Compute delay between scheduledStart and actualStart.
    Always returns >= 0.
    """
    scheduled = timing.get("scheduledStart")
    actual = timing.get("actualStart")

    if not scheduled or not actual:
        return 0

    delay = _to_minutes(scheduled, actual)
    return max(delay, 0)


def compute_early_exit_rate(attendance: dict) -> float:
    """
    Proxy early exit using registered vs checked-in.
    Safe against bad data.
    """
    registered = max(attendance.get("registeredCount", 0), 0)
    checked_in = max(attendance.get("checkedInCount", 0), 0)

    if registered == 0:
        return 0.0

    # Clamp to avoid negative or >1 values
    drop = max(registered - checked_in, 0)
    rate = drop / registered

    return round(min(rate, 1.0), 3)


def normalize_delay(minutes: int) -> float:
    """
    Normalize delay to 0–1 scale (cap at 60 mins).
    Always safe.
    """
    if minutes <= 0:
        return 0.0
    if minutes >= 60:
        return 1.0
    return round(minutes / 60, 3)
