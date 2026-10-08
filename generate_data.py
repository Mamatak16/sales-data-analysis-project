"""
generate_data.py
-----------------
Creates a realistic, slightly messy synthetic sales dataset so the project
includes a genuine data-cleaning step (duplicates, missing values,
inconsistent text casing, stray whitespace) just like real-world data.

Run this once to produce data/sales_data_raw.csv
"""

import os
import numpy as np
import pandas as pd

os.makedirs("data", exist_ok=True)

np.random.seed(42)

N_ROWS = 5000

regions = ["North", "South", "East", "West"]
categories = ["Electronics", "Furniture", "Clothing", "Groceries", "Toys"]
products = {
    "Electronics": ["Headphones", "Smartphone", "Laptop", "Tablet", "Smartwatch"],
    "Furniture": ["Office Chair", "Desk", "Bookshelf", "Sofa", "Bed Frame"],
    "Clothing": ["T-Shirt", "Jeans", "Jacket", "Sneakers", "Cap"],
    "Groceries": ["Coffee", "Snacks", "Cereal", "Juice", "Pasta"],
    "Toys": ["Puzzle", "Action Figure", "Board Game", "Lego Set", "RC Car"],
}
payment_methods = ["Credit Card", "Debit Card", "Cash", "Online Wallet"]

rows = []
for i in range(N_ROWS):
    category = np.random.choice(categories)
    product = np.random.choice(products[category])
    region = np.random.choice(regions)
    date = pd.Timestamp("2024-01-01") + pd.Timedelta(days=int(np.random.randint(0, 730)))
    unit_price = round(np.random.uniform(5, 500), 2)
    quantity = int(np.random.randint(1, 10))
    discount_pct = np.random.choice([0, 0, 0, 5, 10, 15, 20], p=[0.4,0.15,0.15,0.1,0.1,0.05,0.05])
    payment = np.random.choice(payment_methods)
    customer_age = int(np.random.randint(18, 70))

    rows.append({
        "OrderID": f"ORD{10000+i}",
        "OrderDate": date,
        "Region": region,
        "Category": category,
        "Product": product,
        "UnitPrice": unit_price,
        "Quantity": quantity,
        "DiscountPct": discount_pct,
        "PaymentMethod": payment,
        "CustomerAge": customer_age,
    })

df = pd.DataFrame(rows)

# ---- Inject realistic messiness ----

# 1. Inconsistent text casing / stray whitespace in categorical columns
def messy_text(x):
    r = np.random.random()
    if r < 0.1:
        return f" {x.lower()} "
    elif r < 0.2:
        return x.upper()
    return x

df["Region"] = df["Region"].apply(messy_text)
df["Category"] = df["Category"].apply(messy_text)
df["PaymentMethod"] = df["PaymentMethod"].apply(messy_text)

# 2. Missing values scattered across a few columns
for col in ["UnitPrice", "Quantity", "DiscountPct", "CustomerAge"]:
    idx = df.sample(frac=0.03, random_state=np.random.randint(0, 10000)).index
    df.loc[idx, col] = np.nan

# 3. Duplicate rows (simulate accidental double-entry)
dupes = df.sample(frac=0.02, random_state=7)
df = pd.concat([df, dupes], ignore_index=True)

# 4. A few negative / impossible values (data entry errors)
error_idx = df.sample(frac=0.005, random_state=3).index
df.loc[error_idx, "Quantity"] = -df.loc[error_idx, "Quantity"]

# Shuffle rows so duplicates aren't obviously adjacent
df = df.sample(frac=1, random_state=1).reset_index(drop=True)

df.to_csv("data/sales_data_raw.csv", index=False)
print(f"Generated {len(df)} rows -> data/sales_data_raw.csv")
