from pathlib import Path
import pandas as pd
from faker import Faker
import random

# Project paths
BASE_DIR = Path(__file__).resolve().parents[1]
RAW_DIR = BASE_DIR / "data" / "raw_sources"

RAW_DIR.mkdir(parents=True, exist_ok=True)

fake = Faker()

FLORIDA_CITIES = [
    "Miami",
    "Fort Lauderdale",
    "Orlando",
    "Tampa",
    "Jacksonville",
    "Pembroke Pines",
    "Hollywood",
    "Davie",
    "West Palm Beach",
    "Naples",
    "Sarasota",
    "Gainesville",
    "Tallahassee",
    "Boca Raton",
    "Coral Springs"
]


# Generate customers
customers = []

for i in range(1, 10001):
    customers.append({
        "customer_id": f"C{i:06}",
        "first_name": fake.first_name(),
        "last_name": fake.last_name(),
        "email": fake.email(),
        "phone": fake.phone_number(),
        "gender": random.choice(["Male", "Female"]),
        "birth_date": fake.date_of_birth(minimum_age=18, maximum_age=90),
        "signup_date": fake.date_between(start_date="-5y", end_date="today")
    })

# Convert the list of customers into a DataFrame
customers_df = pd.DataFrame(customers)


# Save the DataFrame as a CSV file
customers_df.to_csv(RAW_DIR / "customers.csv", index=False)

print("customers.csv created successfully!")
print(customers_df.head())