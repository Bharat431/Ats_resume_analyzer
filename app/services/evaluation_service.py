"""Resume evaluation service.

This project originally used scikit-learn + sentence-transformers for semantic similarity.
Those packages often lag support for brand-new Python versions (e.g., 3.14 on Windows),
causing install failures due to missing wheels / source builds.

To keep the app runnable out-of-the-box, we use a lightweight pure-Python approach:
- tokenize text
- build term-frequency vectors
- compute cosine similarity

This is not as strong as transformer embeddings, but it is fast, dependency-light, and
good enough for a demo ATS-style score.
"""

from __future__ import annotations

import math
import re
from collections import Counter
from typing import Iterable

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


def _cosine(counter_a: Counter[str], counter_b: Counter[str]) -> float:
    if not counter_a or not counter_b:
        return 0.0

    # dot product
    dot = 0.0
    # iterate the smaller dict for speed
    if len(counter_a) <= len(counter_b):
        for k, va in counter_a.items():
            vb = counter_b.get(k)
            if vb:
                dot += va * vb
    else:
        for k, vb in counter_b.items():
            va = counter_a.get(k)
            if va:
                dot += va * vb

    norm_a = math.sqrt(sum(v * v for v in counter_a.values()))
    norm_b = math.sqrt(sum(v * v for v in counter_b.values()))
    if norm_a == 0.0 or norm_b == 0.0:
        return 0.0
    return float(dot / (norm_a * norm_b))

def keyword_score(resume, jd):
    """Calculate keyword matching score between resume and job description"""
    try:
        resume_words = set(_tokens(resume))
        jd_tokens = _tokens(jd)
        if not jd_tokens:
            return 0

        # Pick "important" JD terms by frequency (top 100)
        jd_counts = Counter(jd_tokens)
        top_terms = {t for t, _ in jd_counts.most_common(100)}

        overlap = len(resume_words & top_terms)
        total = len(top_terms) if top_terms else 1
        return (overlap / total) * 4000
    except:
        return 0

def semantic_similarity(text1, text2):
    """Calculate semantic similarity between texts"""
    try:
        c1 = Counter(_tokens(text1))
        c2 = Counter(_tokens(text2))
        return _cosine(c1, c2)
    except:
        return 0

def format_score(resume):
    """Score resume formatting and structure"""
    score = 0
    if "experience" in resume.lower():
        score += 800
    if "education" in resume.lower():
        score += 800
    if len(resume.split()) > 350:
        score += 400
    return min(score, 2000)

def bullet_score(resume):
    """Score quality of achievement bullets with quantified results"""
    quantified = resume.count("%") + resume.count("improved") + resume.count("increased")
    return min(quantified * 120, 1000)

def evaluate(resume, jd):
    """Complete resume evaluation against job description"""
    k = keyword_score(resume, jd)
    s = semantic_similarity(resume, jd) * 3000
    f = format_score(resume)
    b = bullet_score(resume)
    
    final = k + s + f + b
    
    return {
        "keyword_score": round(k, 2),
        "semantic_score": round(s, 2),
        "format_score": f,
        "bullet_score": b,
        "final_score": round(final, 2)
    }