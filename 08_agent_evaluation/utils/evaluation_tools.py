"""Reusable evaluation utilities for agent performance metrics."""

from typing import List, Dict, Optional


def success_rate(results: List[bool]) -> float:
    """Return the percentage of successful evaluations."""
    if not results:
        return 0.0
    return sum(1 for r in results if r) / len(results)


def average_score(scores: List[float]) -> float:
    """Return the average score for a list of numeric evaluation values."""
    if not scores:
        return 0.0
    return sum(scores) / len(scores)


def normalized_metric(value: float, min_value: float = 0.0, max_value: float = 1.0) -> float:
    """Normalize a score into the range [0.0, 1.0]."""
    if max_value <= min_value:
        raise ValueError("max_value must be greater than min_value")
    clipped = min(max(value, min_value), max_value)
    return (clipped - min_value) / (max_value - min_value)


def compare_responses(reference: str, candidate: str) -> Dict[str, Optional[float]]:
    """Compute a simple token-based similarity score between two responses."""
    if not reference or not candidate:
        return {"overlap": 0.0, "reference_length": len(reference.split()), "candidate_length": len(candidate.split())}

    reference_tokens = set(reference.lower().split())
    candidate_tokens = set(candidate.lower().split())
    overlap = reference_tokens.intersection(candidate_tokens)
    total = len(reference_tokens)
    score = len(overlap) / total if total else 0.0
    return {
        "overlap": score,
        "reference_length": len(reference_tokens),
        "candidate_length": len(candidate_tokens),
    }
