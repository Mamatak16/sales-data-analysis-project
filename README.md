# Sales Data Analysis Project (Python + pandas)

An end-to-end data analysis project you can run yourself, add to your portfolio,
or use as a template for your own datasets.

## What it does

1. **`generate_data.py`** — creates a synthetic but realistic sales dataset
   (5,000+ orders) with intentional real-world messiness: duplicate rows,
   missing values, inconsistent text casing/whitespace, and invalid
   (negative) quantities. Saved to `data/sales_data_raw.csv`.

2. **`analysis.py`** — the core project. It:
   - **Cleans** the data (removes duplicates, fixes negative values,
     standardizes text, handles missing values)
   - **Engineers features** (Revenue, Year, Month)
   - **Analyzes** revenue by category, region, product, payment method, and
     month
   - **Generates 5 charts** (saved as PNGs in `/charts`)
   - **Writes a text report** (`sales_report.txt`) with all key findings

## How to run it

```bash
pip install pandas numpy matplotlib
python3 generate_data.py   # creates the raw dataset
python3 analysis.py        # cleans data, runs analysis, builds charts
```

## Output

- `data/sales_data_raw.csv` — raw (messy) dataset
- `data/sales_data_cleaned.csv` — cleaned dataset ready for further analysis
- `sales_report.txt` — full text summary of findings
- `charts/monthly_revenue_trend.png`
- `charts/revenue_by_category.png`
- `charts/revenue_by_region.png`
- `charts/top_5_products.png`
- `charts/payment_method_distribution.png`

## Skills demonstrated (great for a resume/portfolio)

- Data cleaning (duplicates, missing values, invalid entries, text
  standardization)
- Feature engineering
- Group-by aggregation and business analysis
- Data visualization with matplotlib
- Turning raw data into a written business report

## Using your own data

Swap `data/sales_data_raw.csv` for your own CSV and adjust the column names
in `analysis.py` to match. The cleaning → feature engineering → EDA →
visualization pipeline structure will work for most tabular business
datasets (retail, subscriptions, marketing, etc.).
