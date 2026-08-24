from dataclasses import dataclass
from typing import Dict, Iterable, Mapping, Sequence


@dataclass(frozen=True)
class SurvivorshipRule:
    field_name: str
    preferred_sources: Sequence[str]


def choose_value(
    field_name: str,
    records: Iterable[Mapping[str, str]],
    preferred_sources: Sequence[str] = (),
) -> str:
    """Choose a canonical field value with deterministic source precedence."""
    materialized = [record for record in records if record.get(field_name)]
    if not materialized:
        return ""

    by_source: Dict[str, Mapping[str, str]] = {
        str(record.get("source_system", "")): record for record in materialized
    }
    for source in preferred_sources:
        record = by_source.get(source)
        if record:
            return str(record[field_name])

    # Stable fallback: choose the longest non-empty value, then lexical order.
    return str(sorted(
        (str(record[field_name]) for record in materialized),
        key=lambda value: (-len(value), value.lower()),
    )[0])


def merge_records(
    records: Iterable[Mapping[str, str]],
    rules: Iterable[SurvivorshipRule],
) -> Dict[str, str]:
    materialized = list(records)
    result: Dict[str, str] = {}
    for rule in rules:
        result[rule.field_name] = choose_value(
            rule.field_name,
            materialized,
            rule.preferred_sources,
        )
    return result
