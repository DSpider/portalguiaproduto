from __future__ import annotations

import re
import unicodedata


_STOP_WORDS = {
    "a",
    "as",
    "de",
    "da",
    "das",
    "do",
    "dos",
    "e",
    "o",
    "os",
    "para",
    "por",
}


def generate_slug(text: str, max_length: int = 80) -> str:
    normalized = unicodedata.normalize("NFKD", text.strip().lower())
    ascii_text = normalized.encode("ascii", "ignore").decode("ascii")
    ascii_text = re.sub(r"[^a-z0-9\s-]", "", ascii_text)
    words = [
        word
        for word in re.split(r"[\s-]+", ascii_text)
        if word and word not in _STOP_WORDS
    ]
    slug = "-".join(words)
    slug = re.sub(r"-+", "-", slug).strip("-")

    if len(slug) <= max_length:
        return slug

    truncated = slug[:max_length].rsplit("-", 1)[0]
    return truncated or slug[:max_length].strip("-")
