import pandas as pd
import random
from datetime import datetime, timedelta
import uuid

products = ["Laptop", "Smartphone", "Headphones", "Keyboard", "Monitor", "Mouse", "Tablet", "Smartwatch", "Charger", "Camera"]
categories = ["Electronics", "Accessories", "Gadgets"]
locations = ["New York", "Los Angeles", "Chicago", "Houston", "Phoenix"]
customer_types = ["Regular", "Premium", "Guest"]
payment_methods = ["Credit Card", "Cash", "PayPal", "Debit Card"]
sales_channels = ["In-store", "Online"]
brands = ["BrandA", "BrandB", "BrandC", "BrandD"]
currencies = ["USD", "EUR", "GBP"]

def random_date(start_year=2021, end_year=2024):
    start = datetime(start_year, 1, 1)
    end = datetime(end_year, 12, 31)
    return (start + timedelta(days=random.randint(0, (end - start).days))).strftime("%Y-%m-%d")

def generate_sale(index):
    product = random.choice(products)
    price = round(random.uniform(20.0, 1500.0), 2)
    quantity = random.randint(1, 5)
    total = round(price * quantity, 2)

    return {
        "Transaction_ID": str(uuid.uuid4())[:8].upper(),
        "Transaction_Date": random_date(),
        "Store_Location": random.choice(locations),
        "Customer_Type": random.choice(customer_types),
        "Sales_Channel": random.choice(sales_channels),
        "Product_Name": product,
        "Product_Category": random.choice(categories),
        "Brand": random.choice(brands),
        "Currency": random.choice(currencies),
        "Unit_Price": price,
        "Quantity_Sold": quantity,
        "Total_Amount": total,
        "Discount_Applied": f"{random.choice([0, 5, 10, 15, 20])}%",
        "Sales_Rep_ID": f"SR{random.randint(1000,9999)}",
        "Payment_Method": random.choice(payment_methods)
    }

df = pd.DataFrame([generate_sale(i) for i in range(1200)])
df.to_csv("synthetic_retail_store_sales_data2.csv", index=False)
print("Synthetic retail store sales data generated and saved.")
