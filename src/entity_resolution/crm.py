from dataclasses import dataclass
from enum import Enum
from typing import Any, Dict, Mapping, Optional


class CRMObjectType(str, Enum):
    LEAD = "lead"
    CONTACT = "contact"
    ACCOUNT = "account"


@dataclass(frozen=True)
class CRMRecord:
    record_id: str
    object_type: CRMObjectType
    source_system: str
    name: str = ""
    email: str = ""
    phone: str = ""
    account_name: str = ""
    external_id: str = ""

    def to_resolution_record(self) -> Dict[str, Any]:
        return {
            "id": self.record_id,
            "name": self.name,
            "email": self.email,
            "phone": self.phone,
            "account_name": self.account_name,
            "external_id": self.external_id,
            "object_type": self.object_type.value,
            "source_system": self.source_system,
        }


def _first(mapping: Mapping[str, Any], *keys: str) -> str:
    for key in keys:
        value: Optional[Any] = mapping.get(key)
        if value not in (None, ""):
            return str(value)
    return ""


def from_salesforce_like(payload: Mapping[str, Any], object_type: CRMObjectType) -> CRMRecord:
    """Adapt a Salesforce-shaped synthetic record into the public resolution model.

    Field aliases are intentionally generic and contain no employer-specific schema names.
    """
    return CRMRecord(
        record_id=_first(payload, "Id", "id"),
        object_type=object_type,
        source_system=_first(payload, "SourceSystem", "source_system") or "crm",
        name=_first(payload, "Name", "name"),
        email=_first(payload, "Email", "email"),
        phone=_first(payload, "Phone", "MobilePhone", "phone"),
        account_name=_first(payload, "Company", "AccountName", "account_name"),
        external_id=_first(payload, "ExternalId", "external_id"),
    )
