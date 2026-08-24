from collections import defaultdict
from typing import Any, Dict, Iterable, List

from .normalize import normalize_record
from .similarity import feature_scores, weighted_score


class UnionFind:
    def __init__(self, ids: Iterable[str]):
        self.parent = {i: i for i in ids}

    def find(self, x: str) -> str:
        while self.parent[x] != x:
            self.parent[x] = self.parent[self.parent[x]]
            x = self.parent[x]
        return x

    def union(self, a: str, b: str) -> None:
        ra, rb = self.find(a), self.find(b)
        if ra != rb:
            self.parent[rb] = ra


class EntityResolver:
    def __init__(self, threshold: float = 0.72):
        self.threshold = threshold

    def _block_key(self, record: Dict[str, str]) -> str:
        if record.get("email"):
            return f"email:{record['email']}"
        if record.get("phone"):
            return f"phone:{record['phone']}"
        name = record.get("name", "")
        return f"name:{name[:4]}"

    def resolve(self, records: List[Dict[str, Any]]) -> List[List[Dict[str, Any]]]:
        normalized = [normalize_record(r) for r in records]
        by_id = {str(r.get("id", "")): r for r in records}
        uf = UnionFind(r["id"] for r in normalized)

        blocks: Dict[str, List[Dict[str, str]]] = defaultdict(list)
        for record in normalized:
            blocks[self._block_key(record)].append(record)

        for block in blocks.values():
            for i, left in enumerate(block):
                for right in block[i + 1 :]:
                    score = weighted_score(feature_scores(left, right))
                    if score >= self.threshold:
                        uf.union(left["id"], right["id"])

        clusters: Dict[str, List[Dict[str, Any]]] = defaultdict(list)
        for record in normalized:
            clusters[uf.find(record["id"])].append(by_id[record["id"]])
        return list(clusters.values())
