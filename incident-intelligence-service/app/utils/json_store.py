import json
import os
from threading import Lock

_lock = Lock()


def load_json(path: str) -> dict:
    """
    Safely load JSON file.
    Never crashes the app.
    """
    if not os.path.exists(path):
        return {}

    with _lock:
        try:
            with open(path, "r") as f:
                return json.load(f)
        except Exception:
            # Corrupted or unreadable file
            return {}


def save_json(path: str, data: dict):
    """
    Atomically save JSON to disk.
    Prevents corruption on crash.
    """
    os.makedirs(os.path.dirname(path), exist_ok=True)

    temp_path = f"{path}.tmp"

    with _lock:
        with open(temp_path, "w") as f:
            json.dump(data, f, indent=2)

        # Atomic replace
        os.replace(temp_path, path)
