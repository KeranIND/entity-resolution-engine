from entity_resolution.routing import RoutingContext, choose_route


def test_existing_account_owner_wins_after_canonicalization():
    context = RoutingContext(
        canonical_customer_id="cust-1",
        account_id="acct-9",
        region="east",
        segment="enterprise",
        existing_owner_id=None,
        source_system="crm",
    )
    decision = choose_route(
        context,
        account_owners={"acct-9": "owner-42"},
        regional_queues={"east": "queue-east"},
    )
    assert decision.owner_id == "owner-42"
    assert decision.queue == "direct_owner"


def test_region_routes_when_no_owner_context_exists():
    context = RoutingContext(
        canonical_customer_id="cust-2",
        account_id=None,
        region="west",
        segment="smb",
        existing_owner_id=None,
        source_system="lead_ingest",
    )
    decision = choose_route(context, account_owners={}, regional_queues={"west": "queue-west"})
    assert decision.owner_id == "queue-west"
