"""
analysis.py
-----------
End-to-end Sales Data Analysis Project (Python + pandas)

Pipeline:
 1. Load raw data
 2. Clean data (duplicates, missing values, text formatting, invalid values)
 3. Feature engineering (Revenue, Month, Year)
 4. Exploratory Data Analysis (EDA)
 5. Business insights (top products, regions, trends)
 6. Save charts to /charts and a cleaned dataset to /data

Run with:  python3 analysis.py
"""

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker

pd.set_option("display.max_columns", None)

# ---------------------------------------------------------------
# 1. LOAD DATA
# ---------------------------------------------------------------
df = pd.read_csv("data/sales_data_raw.csv", parse_dates=["OrderDate"])
print(f"Raw data loaded: {df.shape[0]} rows, {df.shape[1]} columns")

# ---------------------------------------------------------------
# 2. DATA CLEANING
# ---------------------------------------------------------------

# 2a. Standardize text columns: strip whitespace, title-case
text_cols = ["Region", "Category", "PaymentMethod", "Product"]
for col in text_cols:
    df[col] = df[col].astype(str).str.strip().str.title()

# 2b. Remove exact duplicate rows
before = len(df)
df = df.drop_duplicates(subset=["OrderID"], keep="first")
print(f"Removed {before - len(df)} duplicate rows")

# 2c. Fix invalid (negative) quantities -> take absolute value
neg_qty = (df["Quantity"] < 0).sum()
df["Quantity"] = df["Quantity"].abs()
print(f"Fixed {neg_qty} negative quantity values")

# 2d. Handle missing values
# UnitPrice & Quantity: drop rows if either key value is missing (can't compute revenue)
before = len(df)
df = df.dropna(subset=["UnitPrice", "Quantity"])
print(f"Dropped {before - len(df)} rows missing UnitPrice/Quantity")

# DiscountPct: assume missing = no discount applied
df["DiscountPct"] = df["DiscountPct"].fillna(0)

# CustomerAge: fill missing with median age
median_age = df["CustomerAge"].median()
df["CustomerAge"] = df["CustomerAge"].fillna(median_age)

print(f"Clean data: {df.shape[0]} rows remaining\n")

# ---------------------------------------------------------------
# 3. FEATURE ENGINEERING
# ---------------------------------------------------------------
df["Revenue"] = df["UnitPrice"] * df["Quantity"] * (1 - df["DiscountPct"] / 100)
df["Year"] = df["OrderDate"].dt.year
df["Month"] = df["OrderDate"].dt.to_period("M").astype(str)
df["MonthName"] = df["OrderDate"].dt.month_name()

# Save cleaned dataset
df.to_csv("data/sales_data_cleaned.csv", index=False)

# ---------------------------------------------------------------
# 4. EXPLORATORY DATA ANALYSIS + INSIGHTS
# ---------------------------------------------------------------
report_lines = []

def log(line=""):
    print(line)
    report_lines.append(line)

log("=" * 60)
log("SALES DATA ANALYSIS REPORT")
log("=" * 60)

total_revenue = df["Revenue"].sum()
total_orders = df["OrderID"].nunique()
avg_order_value = total_revenue / total_orders

log(f"\nTotal Revenue:      ${total_revenue:,.2f}")
log(f"Total Orders:        {total_orders:,}")
log(f"Average Order Value: ${avg_order_value:,.2f}")

# ---- Revenue by Category ----
rev_by_category = df.groupby("Category")["Revenue"].sum().sort_values(ascending=False)
log("\nRevenue by Category:")
for cat, val in rev_by_category.items():
    log(f"  {cat:<15} ${val:,.2f}")

# ---- Revenue by Region ----
rev_by_region = df.groupby("Region")["Revenue"].sum().sort_values(ascending=False)
log("\nRevenue by Region:")
for reg, val in rev_by_region.items():
    log(f"  {reg:<15} ${val:,.2f}")

# ---- Top 5 Products ----
top_products = df.groupby("Product")["Revenue"].sum().sort_values(ascending=False).head(5)
log("\nTop 5 Products by Revenue:")
for prod, val in top_products.items():
    log(f"  {prod:<15} ${val:,.2f}")

# ---- Payment Method Popularity ----
payment_counts = df["PaymentMethod"].value_counts()
log("\nOrders by Payment Method:")
for method, count in payment_counts.items():
    log(f"  {method:<15} {count:,} orders")

# ---- Monthly Revenue Trend ----
monthly_rev = df.groupby("Month")["Revenue"].sum().sort_index()

# ---- Best & Worst performing month ----
best_month = monthly_rev.idxmax()
worst_month = monthly_rev.idxmin()
log(f"\nBest month:  {best_month} (${monthly_rev.max():,.2f})")
log(f"Worst month: {worst_month} (${monthly_rev.min():,.2f})")

# Save text report
with open("sales_report.txt", "w") as f:
    f.write("\n".join(report_lines))
print("\nSaved text report -> sales_report.txt")

# ---------------------------------------------------------------
# 5. VISUALIZATIONS
# ---------------------------------------------------------------
plt.style.use("seaborn-v0_8-whitegrid")

# Chart 1: Monthly Revenue Trend
fig, ax = plt.subplots(figsize=(11, 5))
monthly_rev.plot(kind="line", marker="o", ax=ax, color="#2C6E91")
ax.set_title("Monthly Revenue Trend", fontsize=14, fontweight="bold")
ax.set_xlabel("Month")
ax.set_ylabel("Revenue ($)")
ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"${x:,.0f}"))
plt.xticks(rotation=45, ha="right")
plt.tight_layout()
plt.savefig("charts/monthly_revenue_trend.png", dpi=150)
plt.close()

# Chart 2: Revenue by Category
fig, ax = plt.subplots(figsize=(8, 5))
rev_by_category.plot(kind="bar", ax=ax, color="#4C9A6A")
ax.set_title("Revenue by Category", fontsize=14, fontweight="bold")
ax.set_xlabel("Category")
ax.set_ylabel("Revenue ($)")
ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"${x:,.0f}"))
plt.xticks(rotation=30, ha="right")
plt.tight_layout()
plt.savefig("charts/revenue_by_category.png", dpi=150)
plt.close()

# Chart 3: Revenue by Region (pie chart)
fig, ax = plt.subplots(figsize=(7, 7))
colors = ["#2C6E91", "#4C9A6A", "#D98E3B", "#B34D4D"]
rev_by_region.plot(kind="pie", ax=ax, autopct="%1.1f%%", colors=colors, ylabel="")
ax.set_title("Revenue Share by Region", fontsize=14, fontweight="bold")
plt.tight_layout()
plt.savefig("charts/revenue_by_region.png", dpi=150)
plt.close()

# Chart 4: Top 5 Products
fig, ax = plt.subplots(figsize=(8, 5))
top_products.sort_values().plot(kind="barh", ax=ax, color="#6A4C9A")
ax.set_title("Top 5 Products by Revenue", fontsize=14, fontweight="bold")
ax.set_xlabel("Revenue ($)")
ax.xaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"${x:,.0f}"))
plt.tight_layout()
plt.savefig("charts/top_5_products.png", dpi=150)
plt.close()

# Chart 5: Payment Method Distribution
fig, ax = plt.subplots(figsize=(8, 5))
payment_counts.plot(kind="bar", ax=ax, color="#D9A73B")
ax.set_title("Orders by Payment Method", fontsize=14, fontweight="bold")
ax.set_xlabel("Payment Method")
ax.set_ylabel("Number of Orders")
plt.xticks(rotation=20, ha="right")
plt.tight_layout()
plt.savefig("charts/payment_method_distribution.png", dpi=150)
plt.close()

print("Saved 5 charts -> /charts")
print("\nDone! Project complete.")
