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

# Generate suppliers
suppliers = []

supplier_types = [
    "Pharmaceutical",
    "Medical Device",
    "Supplement",
    "Personal Care",
    "OTC Products"
]

for i in range(1, 101):
    suppliers.append({
        "supplier_id": f"S{i:04}",
        "supplier_name": fake.company(),
        "supplier_type": random.choice(supplier_types),
        "country": "USA",
        "state": "FL",
        "city": random.choice(FLORIDA_CITIES),
        "contact_email": fake.company_email(),
        "phone": fake.phone_number(),
        "active_status": random.choice(["Active", "Active", "Active", "Inactive"])
    })

suppliers_df = pd.DataFrame(suppliers)

suppliers_df.to_csv(RAW_DIR / "suppliers.csv", index=False)

print("suppliers.csv created successfully!")
print(suppliers_df.head())

# Generate products
products = []

categories = {
    "OTC Medicine": [
        "Ibuprofen 200 mg",
        "Acetaminophen 500 mg",
        "Allergy Relief Tablets",
        "Cough Syrup",
        "Antacid Tablets"
    ],
    "Vitamin": [
        "Vitamin C 1000 mg",
        "Vitamin D3 1000 IU",
        "Multivitamin Gummies",
        "Fish Oil Capsules",
        "Calcium Tablets"
    ],
    "Medical Device": [
        "Digital Thermometer",
        "Blood Pressure Monitor",
        "Pulse Oximeter",
        "Glucose Meter",
        "Heating Pad"
    ],
    "Personal Care": [
        "Toothpaste",
        "Shampoo",
        "Body Lotion",
        "Hand Sanitizer",
        "Face Wash"
    ]
}

product_counter = 1

for category, product_list in categories.items():
    for product in product_list:
        products.append({
            "product_id": f"P{product_counter:06}",
            "product_name": product,
            "category": category,
            "brand": fake.company(),
            "supplier_id": random.choice(suppliers_df["supplier_id"]),
            "cost_price": round(random.uniform(2, 40), 2),
            "unit_price": round(random.uniform(5, 60), 2),
            "active_status": random.choice(["Active", "Active", "Active", "Discontinued"])
        })

        product_counter += 1

products_df = pd.DataFrame(products)

products_df.to_csv(RAW_DIR / "products.csv", index=False)

print("products.csv created successfully!")
print(products_df.head())



# Generate stores
stores = []

regions = {
    "South Florida": ["Miami", "Fort Lauderdale", "Pembroke Pines", "Hollywood", "Davie", "Boca Raton"],
    "Central Florida": ["Orlando", "Tampa", "Sarasota"],
    "North Florida": ["Jacksonville", "Gainesville", "Tallahassee"],
    "West Florida": ["Naples"]
}

store_counter = 1

for region, city_list in regions.items():
    for city in city_list:
        for _ in range(random.randint(15, 35)):
            stores.append({
                "store_id": f"ST{store_counter:04}",
                "store_name": f"HealthMart {city} #{store_counter}",
                "city": city,
                "state": "FL",
                "region": region,
                "store_type": random.choice(["Retail", "Retail", "Retail", "Pharmacy Plus"]),
                "open_date": fake.date_between(start_date="-15y", end_date="-1y"),
                "active_status": random.choice(["Active", "Active", "Active", "Inactive"])
            })

            store_counter += 1

stores_df = pd.DataFrame(stores)

stores_df.to_csv(RAW_DIR / "stores.csv", index=False)

print("stores.csv created successfully!")
print(stores_df.head())
print(f"Total stores generated: {len(stores_df)}")




# Generate inventory
inventory = []

inventory_counter = 1

for store in stores_df.itertuples():
    store_products = products_df.sample(frac=0.75, random_state=random.randint(1, 100000))

    for product in store_products.itertuples():
        inventory.append({
            "inventory_id": f"INV{inventory_counter:07}",
            "store_id": store.store_id,
            "product_id": product.product_id,
            "quantity_on_hand": random.randint(0, 500),
            "reorder_level": random.randint(20, 100),
            "last_updated_date": fake.date_between(start_date="-30d", end_date="today")
        })

        inventory_counter += 1

inventory_df = pd.DataFrame(inventory)

inventory_df.to_csv(RAW_DIR / "inventory.csv", index=False)

print("inventory.csv created successfully!")
print(inventory_df.head())
print(f"Total inventory rows generated: {len(inventory_df)}")

# Generate transactions
transactions = []

payment_methods = ["Credit Card", "Debit Card", "Cash", "Mobile Payment"]

for i in range(1, 5001):
    transactions.append({
        "transaction_id": f"T{i:07}",
        "customer_id": random.choice(customers_df["customer_id"]),
        "store_id": random.choice(stores_df["store_id"]),
        "transaction_date": fake.date_between(start_date="-2y", end_date="today"),
        "payment_method": random.choice(payment_methods),
        "transaction_total": round(random.uniform(5, 250), 2)
    })

transactions_df = pd.DataFrame(transactions)

transactions_df.to_csv(RAW_DIR / "transactions.csv", index=False)

print("transactions.csv created successfully!")
print(transactions_df.head())
print(f"Total transactions generated: {len(transactions_df)}")



# Generate transaction items
transaction_items = []

transaction_item_counter = 1

for transaction in transactions_df.itertuples():
    number_of_items = random.randint(1, 5)
    selected_products = products_df.sample(n=number_of_items)

    for product in selected_products.itertuples():
        quantity = random.randint(1, 4)
        unit_price = product.unit_price
        line_total = round(quantity * unit_price, 2)

        transaction_items.append({
            "transaction_item_id": f"TI{transaction_item_counter:08}",
            "transaction_id": transaction.transaction_id,
            "product_id": product.product_id,
            "quantity": quantity,
            "unit_price": unit_price,
            "line_total": line_total
        })

        transaction_item_counter += 1

transaction_items_df = pd.DataFrame(transaction_items)

transaction_items_df.to_csv(RAW_DIR / "transaction_items.csv", index=False)

print("transaction_items.csv created successfully!")
print(transaction_items_df.head())
print(f"Total transaction items generated: {len(transaction_items_df)}")