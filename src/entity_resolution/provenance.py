from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Dict, List


@dataclass(frozen=True)
class MergeEdge:
    left_id: str
    right_id: str
    score: float
    reason: str
    merged_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))


@dataclass
class CanonicalEntity:
    canonical_id: str
    member_ids: List[str] = field(default_factory=list)
    field_sources: Dict[str, str] = field(default_factory=dict)
    lineage: List[MergeEdge] = field(default_factory=list)

    def attach(self, record_id: str) -> None:
        if record_id not in self.member_ids:
            self.member_ids.append(record_id)

    def record_field_source(self, field_name: str, record_id: str) -> None:
        self.field_sources[field_name] = record_id

    def add_merge(self, edge: MergeEdge) -> None:
        self.lineage.append(edge)
