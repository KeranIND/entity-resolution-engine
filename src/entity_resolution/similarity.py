from difflib import SequenceMatcher
from typing import Dict


def ratio(a: str, b: str) -> float:
    if not a or not b:
        return 0.0
    return SequenceMatcher(None, a, b).ratio()


def feature_scores(a: Dict[str, str], b: Dict[str, str]) -> Dict[str, float]:
    return {
        "name": ratio(a.get("name", ""), b.get("name", "")),
        "email": 1.0 if a.get("email") and a.get("email") == b.get("email") else 0.0,
        "phone": 1.0 if a.get("phone") and a.get("phone") == b.get("phone") else 0.0,
        "address": ratio(a.get("address", ""), b.get("address", "")),
    }


def weighted_score(scores: Dict[str, float], weights: Dict[str, float] | None = None) -> float:
    weights = weights or {"name": 0.35, "email": 0.35, "phone": 0.2, "address": 0.1}
    total = sum(weights.values()) or 1.0
    return sum(scores.get(k, 0.0) * w for k, w in weights.items()) / total
