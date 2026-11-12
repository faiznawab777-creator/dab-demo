# Databricks notebook source
from datetime import datetime, timedelta
from decimal import Decimal
import random
import uuid

_CUSTOMERS = ["CUST1001", "CUST1002", "CUST1003", "CUST1004", "CUST1005"]
_ACCOUNTS = ["ACC9001", "ACC9002", "ACC9003", "ACC9004", "ACC9005"]
_MERCHANTS = [
    ("Fresh Mart", "GROCERY"),
    ("Metro Fuel", "FUEL"),
    ("City Bistro", "DINING"),
    ("ShopOnline", "E_COMMERCE"),
    ("Power Utilities", "UTILITIES"),
    ("City Mall", "SHOPPING"),
]
_CHANNELS = ["POS", "UPI", "ECOM", "ATM"]
_CITIES = ["Pune", "Mumbai", "Bengaluru", "Hyderabad"]


def generate_transaction_rows(batch_size=100, batch_label="poc_batch"):
    random.seed()
    now = datetime.utcnow()
    rows = []
    for _ in range(batch_size):
        merchant, category = random.choice(_MERCHANTS)
        rows.append({
            "transaction_id": str(uuid.uuid4()),
            "customer_id": random.choice(_CUSTOMERS),
            "account_id": random.choice(_ACCOUNTS),
            "transaction_timestamp": now - timedelta(minutes=random.randint(0, 10080)),
            "transaction_type": random.choice(["DEBIT", "CREDIT"]),
            "channel": random.choice(_CHANNELS),
            "merchant_name": merchant,
            "merchant_category": category,
            "amount": Decimal(str(round(random.uniform(100, 25000), 2))),
            "currency": "INR",
            "city": random.choice(_CITIES),
            "batch_label": batch_label,
        })
    return rows
