from src.utils.transaction_rules import categorize_merchant, is_valid_transaction

print('testing framework')

def test_categorize_grocery():
    assert categorize_merchant("grocery") == "ESSENTIALS"


def test_unknown_category():
    assert categorize_merchant("UNKNOWN") == "OTHER"


def test_valid_transaction():
    assert is_valid_transaction({
        "transaction_id": "T1", "customer_id": "C1",
        "amount": 250, "currency": "INR"
    })


def test_reject_negative_amount():
    assert not is_valid_transaction({
        "transaction_id": "T1", "customer_id": "C1",
        "amount": -1, "currency": "INR"
    })
