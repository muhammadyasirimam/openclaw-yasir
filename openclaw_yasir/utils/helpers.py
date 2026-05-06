"""Common utility functions."""

import re
from datetime import datetime
from typing import Optional


def sanitize_filename(filename: str, max_length: int = 100) -> str:
    """Sanitize a string for use as a filename."""
    # Remove invalid characters
    sanitized = re.sub(r'[<>:"/\\|?*]', '', filename)
    # Replace spaces with underscores
    sanitized = sanitized.replace(' ', '_')
    # Limit length
    if len(sanitized) > max_length:
        sanitized = sanitized[:max_length]
    return sanitized


def truncate_text(text: str, max_length: int = 200, suffix: str = "...") -> str:
    """Truncate text to maximum length."""
    if len(text) <= max_length:
        return text
    return text[:max_length - len(suffix)] + suffix


def format_timestamp(dt: Optional[datetime] = None, fmt: str = "%Y-%m-%d %H:%M:%S") -> str:
    """Format a datetime object as a string."""
    if dt is None:
        dt = datetime.now()
    return dt.strftime(fmt)


def estimate_reading_time(text: str, wpm: int = 200) -> int:
    """Estimate reading time in minutes."""
    word_count = len(text.split())
    return max(1, round(word_count / wpm))


def extract_keywords(text: str, min_length: int = 4, top_n: int = 10) -> list:
    """Extract top keywords from text."""
    words = re.findall(r'\b[a-zA-Z]{' + str(min_length) + r',}\b', text.lower())
    from collections import Counter
    return [word for word, count in Counter(words).most_common(top_n)]
