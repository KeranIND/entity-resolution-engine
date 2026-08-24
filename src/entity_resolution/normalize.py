import re
import unicodedata
from typing import Any, Dict


def _ascii_fold(value: str) -> str:
    normalized = unicodedata.normalize("NFKD", value)
    return "".join(ch for ch in normalized if not unicodedata.combining(ch))


def normalize_text(value: Any) -> str:
    if value is None:
        return ""
    text = _ascii_fold(str(value)).lower().strip()
    text = re.sub(r"[^a-z0-9\s@.+-]", " ", text)
    return re.sub(r"\s+", " ", text).strip()


def normalize_email(value: Any) -> str:
    return normalize_text(value).replace(" ", "")


def normalize_phone(value: Any) -> str:
    if value is None:
        return ""
    digits = re.sub(r"\D", "", str(value))
    return digits[-10:] if len(digits) >= 10 else digits


def normalize_record(record: Dict[str, Any]) -> Dict[str, str]:
    return {
        "id": str(record.get("id", "")),
        "name": normalize_text(record.get("name")),
        "email": normalize_email(record.get("email")),
        "phone": normalize_phone(record.get("phone")),
        "address": normalize_text(record.get("address")),
    }
