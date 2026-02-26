"""Similarity helper utilities.

The original implementation used sentence-transformers + scikit-learn, which often fails
to install on very new Python versions due to missing wheels (e.g., Python 3.14 on
Windows).

For this project we only need a rough semantic-ish similarity score, so we use a
dependency-light token-frequency cosine similarity.
"""

from __future__ import annotations

import math
import re
from collections import Counter

_WORD_RE = re.compile(r"[A-Za-z0-9]+")
_STOPWORDS = {
    "a",
    "an",
    "and",
    "are",
    "as",
    "at",
    "be",
    "by",
    "for",
    "from",
    "has",
    "have",
    "in",
    "is",
    "it",
    "of",
    "on",
    "or",
    "that",
    "the",
    "this",
    "to",
    "was",
    "were",
    "with",
    "you",
    "your",
}


def _tokens(text: str) -> list[str]:
    return [t.lower() for t in _WORD_RE.findall(text) if t.lower() not in _STOPWORDS]


def get_embeddings(texts: list[str]) -> list[Counter[str]]:
    """Return token-frequency counters as lightweight "embeddings"."""
    return [Counter(_tokens(t)) for t in texts]


def semantic_similarity(text1: str, text2: str) -> float:
    """Cosine similarity between token-frequency "embeddings" (0..1)."""
    c1 = Counter(_tokens(text1))
    c2 = Counter(_tokens(text2))
    if not c1 or not c2:
        return 0.0

    dot = 0.0
    if len(c1) <= len(c2):
        for k, v in c1.items():
            dot += v * c2.get(k, 0)
    else:
        for k, v in c2.items():
            dot += v * c1.get(k, 0)

    n1 = math.sqrt(sum(v * v for v in c1.values()))
    n2 = math.sqrt(sum(v * v for v in c2.values()))
    if n1 == 0.0 or n2 == 0.0:
        return 0.0
    return float(dot / (n1 * n2))