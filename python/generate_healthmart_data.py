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

# Generate loyalty accounts
loyalty_accounts = []

loyalty_customers = customers_df.sample(frac=0.70, random_state=42)

for i, row in enumerate(loyalty_customers.itertuples(), start=1):
    loyalty_accounts.append({
        "loyalty_id": f"L{i:06}",
        "customer_id": row.customer_id,
        "loyalty_tier": random.choice(["Bronze", "Silver", "Gold", "Platinum"]),
        "points_balance": random.randint(0, 10000),
        "enrollment_date": fake.date_between(start_date=row.signup_date, end_date="today"),
        "account_status": random.choice(["Active", "Active", "Active", "Inactive"])
    })

loyalty_accounts_df = pd.DataFrame(loyalty_accounts)

loyalty_accounts_df.to_csv(RAW_DIR / "loyalty_accounts.csv", index=False)

print("loyalty_accounts.csv created successfully!")
print(loyalty_accounts_df.head())


# Generate customer addresses
customer_addresses = []
address_id_counter = 1

for row in customers_df.itertuples():
    number_of_addresses = random.choice([1, 1, 1, 2])

    for address_number in range(number_of_addresses):
        address_type = "Home" if address_number == 0 else "Mailing"

        customer_addresses.append({
            "address_id": f"A{address_id_counter:06}",
            "customer_id": row.customer_id,
            "address_type": address_type,
            "street_address": fake.street_address(),
            "city": random.choice(FLORIDA_CITIES),
            "state": "FL",
            "zip_code": fake.zipcode()
        })

        address_id_counter += 1
customer_addresses_df = pd.DataFrame(customer_addresses)

customer_addresses_df.to_csv(RAW_DIR / "customer_addresses.csv", index=False)

print("customer_addresses.csv created successfully!")
print(customer_addresses_df.head())


# Generate customer preferences
customer_preferences = []

for i, row in enumerate(customers_df.itertuples(), start=1):
    email_opt_in = random.choice([True, True, True, False])
    sms_opt_in = random.choice([True, True, False])

    preferred_channel = random.choice(["Email", "SMS", "Mobile App", "None"])

    customer_preferences.append({
        "preference_id": f"PR{i:06}",
        "customer_id": row.customer_id,
        "email_opt_in": email_opt_in,
        "sms_opt_in": sms_opt_in,
        "preferred_language": random.choice(["English", "English", "English", "Spanish"]),
        "preferred_channel": preferred_channel,
        "last_updated_date": fake.date_between(start_date=row.signup_date, end_date="today")
    })

customer_preferences_df = pd.DataFrame(customer_preferences)

customer_preferences_df.to_csv(RAW_DIR / "customer_preferences.csv", index=False)

print("customer_preferences.csv created successfully!")
print(customer_preferences_df.head())

