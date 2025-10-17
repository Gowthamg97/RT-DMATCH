import re
from pprint import pprint

def semantic_rule_check(row: dict) -> dict:
    results = {}

    specs = {
        "age": "number",
        "salary": "number",
        "first_name": "alpha",
        "last_name": "alpha",
        "order_number": "alphanumeric",
        "customer_id": "alphanumeric",
        "postal_code": "number",
        "city": "alpha",
        "remarks": "special_only",
        "currency_code": "alpha"
    }

    patterns = {
        "number": r"^\d+$",
        "alpha": r"^[A-Za-z]+$",
        "alphanumeric": r"^[A-Za-z0-9]+$",
        "special_only": r"^[^A-Za-z0-9]+$",
    }

    for field, rule in specs.items():
        value = str(row.get(field, "")).strip()
        result = {"status": "PASS", "error": ""}

        if value == "":
            result["status"] = "IGNORE"
            result["error"] = "Value missing"
        elif not re.fullmatch(patterns[rule], value):
            result["status"] = "FAIL"
            result["error"] = f"Value '{value}' is not valid for rule '{rule}'"
        
        results[field] = result

    return results

sample_row = {
    "age": "30",
    "salary": "55000",
    "first_name": "John",
    "last_name": "Doe",
    "order_number": "ORD1234",
    "customer_id": "CUST001",
    "postal_code": "12345",
    "city": "NewYork",
    "remarks": "!@#$",
    "currency_code": "USD"
}

pprint(semantic_rule_check(sample_row))
