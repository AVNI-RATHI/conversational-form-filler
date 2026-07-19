"""Tools and utilities for the agent."""

import re
from typing import Optional

def extract_email(text: str) -> Optional[str]:
    """Extract email address from text."""
    pattern = r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b"
    match = re.search(pattern, text)
    return match.group(0) if match else None

def extract_phone(text: str) -> Optional[str]:
    """Extract phone number from text."""
    patterns = [
        r"\b(?:\+?1[-.]?)?\(?([0-9]{3})\)?[-.]?([0-9]{3})[-.]?([0-9]{4})\b",
        r"\b[0-9]{10}\b",
    ]
    for pattern in patterns:
        match = re.search(pattern, text)
        if match:
            return match.group(0)
    return None

def extract_name(text: str) -> Optional[str]:
    """Extract name from text."""
    words = text.split()
    if len(words) >= 1:
        name_words = [w.capitalize() for w in words if len(w) > 1]
        if name_words:
            return " ".join(name_words[:3])
    return None

def calculate_confidence(text: str, field_type: str) -> float:
    """Calculate confidence score for extracted value."""
    if not text:
        return 0.0

    if field_type == "email":
        return 0.95 if "@" in text and "." in text else 0.5
    elif field_type == "phone":
        digits = "".join(c for c in text if c.isdigit())
        return 0.9 if len(digits) >= 10 else 0.3
    elif field_type == "name":
        return 0.7 if len(text.split()) >= 1 else 0.3
    else:
        return 0.5
