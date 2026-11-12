CATEGORY_MAP = {
    "GROCERY": "ESSENTIALS", "SUPERMARKET": "ESSENTIALS",
    "FUEL": "TRANSPORT", "TRANSPORT": "TRANSPORT",
    "DINING": "DINING", "RESTAURANT": "DINING",
    "SHOPPING": "SHOPPING", "E_COMMERCE": "SHOPPING",
    "UTILITIES": "BILLS", "BILLS": "BILLS",
}


def categorize_merchant(merchant_category: str) -> str:
    if not merchant_category:
        return "OTHER"
    return CATEGORY_MAP.get(merchant_category.strip().upper(), "OTHER")


def is_valid_transaction(transaction: dict) -> bool:
    try:
        return (
            bool(transaction.get("transaction_id"))
            and bool(transaction.get("customer_id"))
            and float(transaction.get("amount", 0)) > 0
            and transaction.get("currency") == "INR"
        )
    except (TypeError, ValueError):
        return False
