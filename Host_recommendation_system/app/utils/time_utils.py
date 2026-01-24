from datetime import datetime, timezone, timedelta
from typing import Optional


# ==================================================
# CURRENT TIME HELPERS
# ==================================================

def now_utc() -> datetime:
    """
    Returns current UTC time (timezone-aware).
    """
    return datetime.now(timezone.utc)


def utc_timestamp_str(fmt: str = "%Y%m%d_%H%M%S") -> str:
    """
    Returns current UTC time formatted as string.

    Default format: 20240205_143012
    """
    return now_utc().strftime(fmt)


# ==================================================
# DURATION & WINDOW HELPERS
# ==================================================

def minutes_to_timedelta(minutes: int) -> timedelta:
    """
    Converts minutes to timedelta safely.
    """
    return timedelta(minutes=minutes)


def is_within_window(
    reference_time: datetime,
    window_minutes: int,
    current_time: Optional[datetime] = None
) -> bool:
    """
    Checks if current_time is within +/- window_minutes of reference_time.
    """
    if current_time is None:
        current_time = now_utc()

    window = minutes_to_timedelta(window_minutes)
    return abs(current_time - reference_time) <= window


# ==================================================
# EVENT-RELATED HELPERS
# ==================================================

def format_duration(minutes: int) -> str:
    """
    Formats duration into human-readable form.

    Example:
        125 → "2h 5m"
    """
    if minutes <= 0:
        return "0m"

    hours = minutes // 60
    mins = minutes % 60

    if hours > 0 and mins > 0:
        return f"{hours}h {mins}m"
    if hours > 0:
        return f"{hours}h"
    return f"{mins}m"


# ==================================================
# FILE / LOG TIMESTAMPS
# ==================================================

def timestamp_for_filename() -> str:
    """
    Returns safe timestamp for filenames.
    """
    return utc_timestamp_str()
