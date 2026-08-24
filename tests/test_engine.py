from entity_resolution.engine import EntityResolver
from entity_resolution.normalize import normalize_phone


def test_normalize_phone_keeps_last_ten_digits():
    assert normalize_phone("+1 (551) 344-7943") == "5513447943"


def test_exact_email_duplicates_cluster_together():
    records = [
        {"id": "1", "name": "Kiran Indugula", "email": "kiran@example.com"},
        {"id": "2", "name": "K. Indugula", "email": "kiran@example.com"},
        {"id": "3", "name": "Other Person", "email": "other@example.com"},
    ]
    clusters = EntityResolver().resolve(records)
    sizes = sorted(len(cluster) for cluster in clusters)
    assert sizes == [1, 2]
