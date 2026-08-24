from dataclasses import dataclass
from typing import Dict, Optional


@dataclass(frozen=True)
class RoutingContext:
    canonical_customer_id: str
    account_id: Optional[str]
    region: Optional[str]
    segment: Optional[str]
    existing_owner_id: Optional[str]
    source_system: str


@dataclass(frozen=True)
class RoutingDecision:
    owner_id: str
    queue: str
    reason: str


def choose_route(
    context: RoutingContext,
    account_owners: Dict[str, str],
    regional_queues: Dict[str, str],
    default_queue: str = "unassigned",
) -> RoutingDecision:
    if context.account_id and context.account_id in account_owners:
        return RoutingDecision(
            owner_id=account_owners[context.account_id],
            queue="direct_owner",
            reason="canonical identity linked to existing account owner",
        )

    if context.existing_owner_id:
        return RoutingDecision(
            owner_id=context.existing_owner_id,
            queue="existing_owner",
            reason="preserve valid owner after identity resolution",
        )

    if context.region and context.region in regional_queues:
        return RoutingDecision(
            owner_id=regional_queues[context.region],
            queue="regional_queue",
            reason="route canonical customer by region",
        )

    return RoutingDecision(
        owner_id=default_queue,
        queue=default_queue,
        reason="insufficient routing context",
    )
