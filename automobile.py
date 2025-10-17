import pandas as pd
import random
from datetime import datetime, timedelta

columns = [
    "VIN ID", "COUNTRY", "CITY", "STATE", "POSTAL CODE", "MODEL YEAR",
    "MAKE", "MODEL", "ELECTRIC VEHICLE TYPE",
    "CLEAN ALTERNATIVE FUEL VEHICLE(CAFV) ELIGIBILITY",
    "ELECTRIC RANGE", "BASE MSRP", "LEGISLATIVE DISTRICT",
    "DOL VEHICLE ID", "VEHICLE LOCATION", "ELECTRIC UTILITY"
]

countries = ["USA", "Canada"]
states = ["CA", "WA", "TX", "NY", "FL"]
cities = ["Seattle", "Los Angeles", "New York", "Toronto", "Houston"]
makes = ["Tesla", "Ford", "Chevrolet", "Nissan", "BMW"]
models = ["Model S", "F-150", "Bolt", "Leaf", "i3"]
ev_types = ["Battery Electric Vehicle (BEV)", "Plug-in Hybrid Electric Vehicle (PHEV)"]
cafv_eligibility = ["Clean Alternative Fuel Vehicle Eligible", "Not Eligible"]
utilities = ["Seattle City Light", "PG&E", "ConEdison", "BC Hydro", "Florida Power & Light"]

def random_date(start_year=2012, end_year=2024):
    start = datetime(start_year, 1, 1)
    end = datetime(end_year, 12, 31)
    return (start + timedelta(days=random.randint(0, (end - start).days))).strftime("%Y-%m-%d")

def generate_row(index):
    make = random.choice(makes)
    model = random.choice(models)
    year = random.randint(2015, 2024)
    
    row = {
        "VIN ID": f"1HGCM82633A{random.randint(100000, 999999)}",
        "COUNTRY": random.choice(countries),
        "CITY": random.choice(cities),
        "STATE": random.choice(states),
        "POSTAL CODE": f"{random.randint(10000, 99999)}",
        "MODEL YEAR": year,
        "MAKE": make,
        "MODEL": model,
        "ELECTRIC VEHICLE TYPE": random.choice(ev_types),
        "CLEAN ALTERNATIVE FUEL VEHICLE(CAFV) ELIGIBILITY": random.choice(cafv_eligibility),
        "ELECTRIC RANGE": random.randint(50, 400),
        "BASE MSRP": round(random.uniform(30000, 90000), 2),
        "LEGISLATIVE DISTRICT": f"{random.randint(1, 50)}",
        "DOL VEHICLE ID": f"DOL{100000 + index}",
        "VEHICLE LOCATION": f"{random.choice(cities)}, {random.choice(states)}",
        "ELECTRIC UTILITY": random.choice(utilities)
    }
    return row

df = pd.DataFrame([generate_row(i) for i in range(1200)])

file_path = "car_electric_vehicles_synthetic_data.csv"
df.to_csv(file_path, index=False)
print(f"Synthetic data saved to: {file_path}")
