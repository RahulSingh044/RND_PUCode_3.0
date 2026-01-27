import os
import uuid
from typing import Optional


# ==================================================
# BASE DIRECTORIES
# ==================================================

GENERATED_BASE_DIR = "data/generated"


# ==================================================
# DIRECTORY UTILITIES
# ==================================================

def ensure_dir(path: str) -> None:
    """
    Ensure a directory exists.
    Creates it recursively if missing.
    """
    os.makedirs(path, exist_ok=True)


def get_generated_dir(subdir: Optional[str] = None) -> str:
    """
    Returns absolute path to generated files directory.

    Example:
        get_generated_dir("checklists")
        → data/generated/checklists
    """
    base = GENERATED_BASE_DIR
    if subdir:
        base = os.path.join(base, subdir)

    ensure_dir(base)
    return base


# ==================================================
# FILE PATH UTILITIES
# ==================================================

def generate_unique_filename(
    prefix: str,
    extension: str
) -> str:
    """
    Generates a collision-safe filename.

    Example:
        host_A_20240205_8f9a2c.pdf
    """
    uid = uuid.uuid4().hex[:6]
    return f"{prefix}_{uid}.{extension.lstrip('.')}"


def build_file_path(
    directory: str,
    filename: str
) -> str:
    """
    Safely join directory and filename.
    """
    ensure_dir(directory)
    return os.path.join(directory, filename)


# ==================================================
# SAFE FILE OPERATIONS
# ==================================================

def safe_write_binary(path: str, data: bytes) -> None:
    """
    Safely writes binary data to file.
    """
    ensure_dir(os.path.dirname(path))
    with open(path, "wb") as f:
        f.write(data)


def safe_file_exists(path: str) -> bool:
    """
    Check if file exists and is readable.
    """
    return os.path.exists(path) and os.path.isfile(path)
