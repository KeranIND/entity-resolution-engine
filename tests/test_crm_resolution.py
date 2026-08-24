from entity_resolution.crm import CRMObjectType, from_salesforce_like
from entity_resolution.merge_policy import SurvivorshipRule, merge_records


def test_salesforce_like_lead_adapter_preserves_source_context():
    record = from_salesforce_like(
        {
            "Id": "00Q-example",
            "Name": "Kiran Indugula",
            "Email": "kiran@example.com",
            "Phone": "+1 551 344 7943",
            "Company": "Example Retail",
            "SourceSystem": "lead-import",
        },
        CRMObjectType.LEAD,
    )
    assert record.object_type == CRMObjectType.LEAD
    assert record.source_system == "lead-import"
    assert record.account_name == "Example Retail"


def test_survivorship_prefers_trusted_source():
    records = [
        {"name": "K. Indugula", "source_system": "lead-import"},
        {"name": "Kiran Indugula", "source_system": "verified-profile"},
    ]
    merged = merge_records(
        records,
        [SurvivorshipRule("name", ["verified-profile", "lead-import"])],
    )
    assert merged["name"] == "Kiran Indugula"
