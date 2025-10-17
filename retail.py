import pandas as pd
import random
from datetime import datetime, timedelta

product_catalog = [
    ("P001", "Laptop", "Electronics"),
    ("P002", "Smartphone", "Electronics"),
    ("P003", "Headphones", "Accessories"),
    ("P004", "Keyboard", "Accessories"),
    ("P005", "Monitor", "Electronics"),
    ("P006", "Mouse", "Accessories"),
    ("P007", "Tablet", "Electronics"),
    ("P008", "Charger", "Accessories"),
    ("P009", "Smartwatch", "Wearables"),
    ("P010", "Camera", "Electronics")
]

store_locations = ["New York", "Los Angeles", "Chicago", "Houston", "Phoenix"]
customer_types = ["Regular", "Premium", "Guest"]
payment_methods = ["Credit Card", "Cash", "PayPal", "Debit Card"]

def random_date(start_year=2020, end_year=2024):
    start = datetime(start_year, 1, 1)
    end = datetime(end_year, 12, 31)
    return (start + timedelta(days=random.randint(0, (end - start).days))).strftime("%Y-%m-%d")

def generate_sale(index):
    store = random.choice(store_locations)
    customer_id = f"C{random.randint(1000, 9999)}"
    product_id, product_name, category = random.choice(product_catalog)
    unit_price = round(random.uniform(10.0, 1500.0), 2)
    quantity = random.randint(1, 5)
    total_amount = round(unit_price * quantity, 2)

    return {
        "Transaction_ID": f"T{100000 + index}",
        "Transaction_Date": random_date(),
        "Store_ID": f"S{random.randint(100, 999)}",
        "Store_Location": store,
        "Customer_ID": customer_id,
        "Customer_Type": random.choice(customer_types),
        "Payment_Method": random.choice(payment_methods),
        "Product_ID": product_id,
        "Product_Name": product_name,
        "Category": category,
        "Unit_Price": unit_price,
        "Quantity": quantity,
        "Total_Amount": total_amount
    }

df = pd.DataFrame([generate_sale(i) for i in range(100)])
df.to_csv("synthetic_retail_store_sales_data.csv", index=False)
print("Synthetic retail store sales data generated and saved.")
