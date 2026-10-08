"""
app.py
------
Interactive Localhost Web Dashboard (Streamlit + Plotly)
Sales Data Analysis Project

Run on localhost with:
    streamlit run app.py
"""

import os
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as io
import streamlit as st

# Set Streamlit page configuration
st.set_page_config(
    page_title="Sales Data Analysis Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Custom CSS for modern glassmorphism aesthetic
st.markdown(
    """
    <style>
    /* Main Background & Fonts */
    .stApp {
        background-color: #0E1117;
        font-family: 'Inter', sans-serif;
    }
    
    /* Title Styling */
    .main-title {
        font-size: 2.2rem;
        font-weight: 800;
        background: linear-gradient(90deg, #4F46E5 0%, #06B6D4 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.2rem;
    }
    .sub-title {
        color: #9CA3AF;
        font-size: 1rem;
        margin-bottom: 2rem;
    }
    
    /* Metric Cards */
    div[data-testid="stMetricValue"] {
        font-size: 1.8rem;
        font-weight: 700;
        color: #F3F4F6;
    }
    div[data-testid="stMetricLabel"] {
        font-size: 0.9rem;
        color: #9CA3AF;
        font-weight: 500;
    }
    .metric-card {
        background: #1F2937;
        border: 1px solid #374151;
        border-radius: 12px;
        padding: 1.2rem;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# ---------------------------------------------------------------
# DATA LOADING & CLEANING PIPELINE
# ---------------------------------------------------------------
@st.cache_data
def load_and_clean_data():
    raw_path = "data/sales_data_raw.csv" if os.path.exists("data/sales_data_raw.csv") else "sales_data_raw.csv"
    
    if not os.path.exists(raw_path):
        # Auto-generate raw data if not found
        import generate_data
        
    df = pd.read_csv(raw_path, parse_dates=["OrderDate"])
    
    # 1. Clean categorical text
    text_cols = ["Region", "Category", "PaymentMethod", "Product"]
    for col in text_cols:
        df[col] = df[col].astype(str).str.strip().str.title()
        
    # 2. Remove duplicate order IDs
    df = df.drop_duplicates(subset=["OrderID"], keep="first")
    
    # 3. Absolute value for negative quantities
    df["Quantity"] = df["Quantity"].abs()
    
    # 4. Drop missing essential price/quantity
    df = df.dropna(subset=["UnitPrice", "Quantity"])
    
    # 5. Fill missing values
    df["DiscountPct"] = df["DiscountPct"].fillna(0)
    median_age = df["CustomerAge"].median()
    df["CustomerAge"] = df["CustomerAge"].fillna(median_age)
    
    # 6. Feature Engineering
    df["Revenue"] = df["UnitPrice"] * df["Quantity"] * (1 - df["DiscountPct"] / 100)
    df["Year"] = df["OrderDate"].dt.year
    df["Month"] = df["OrderDate"].dt.to_period("M").astype(str)
    
    return df

df_clean = load_and_clean_data()

# ---------------------------------------------------------------
# SIDEBAR FILTERS
# ---------------------------------------------------------------
st.sidebar.image("https://img.icons8.com/color/96/dashboard--v1.png", width=64)
st.sidebar.title("Dashboard Controls")
st.sidebar.markdown("Filter dataset in real-time:")

# Date Range Filter
min_date = df_clean["OrderDate"].min().date()
max_date = df_clean["OrderDate"].max().date()

date_range = st.sidebar.date_input(
    "Order Date Range",
    value=(min_date, max_date),
    min_value=min_date,
    max_value=max_date,
)

# Region Filter
all_regions = sorted(df_clean["Region"].unique().tolist())
selected_regions = st.sidebar.multiselect(
    "Select Region(s)",
    options=all_regions,
    default=all_regions,
)

# Category Filter
all_categories = sorted(df_clean["Category"].unique().tolist())
selected_categories = st.sidebar.multiselect(
    "Select Category(s)",
    options=all_categories,
    default=all_categories,
)

# Apply Filters
start_d, end_d = (date_range[0], date_range[1]) if len(date_range) == 2 else (min_date, max_date)

filtered_df = df_clean[
    (df_clean["OrderDate"].dt.date >= start_d) &
    (df_clean["OrderDate"].dt.date <= end_d) &
    (df_clean["Region"].isin(selected_regions)) &
    (df_clean["Category"].isin(selected_categories))
]

# ---------------------------------------------------------------
# MAIN DASHBOARD CONTENT
# ---------------------------------------------------------------
st.markdown('<div class="main-title">📈 Sales Data Analysis Dashboard</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-title">Interactive business insights, sales trends, and exploratory analytics</div>', unsafe_allow_html=True)

if filtered_df.empty:
    st.warning("⚠️ No data matches the selected sidebar filters. Please broaden your selection.")
    st.stop()

# Key Performance Indicators (KPIs)
col1, col2, col3, col4 = st.columns(4)

total_rev = filtered_df["Revenue"].sum()
total_orders = filtered_df["OrderID"].nunique()
avg_order_val = total_rev / total_orders if total_orders > 0 else 0
top_cat = filtered_df.groupby("Category")["Revenue"].sum().idxmax() if not filtered_df.empty else "N/A"

with col1:
    st.metric(label="Total Revenue", value=f"${total_rev:,.2f}")
with col2:
    st.metric(label="Total Orders", value=f"{total_orders:,}")
with col3:
    st.metric(label="Avg Order Value", value=f"${avg_order_val:,.2f}")
with col4:
    st.metric(label="Top Category", value=top_cat)

st.markdown("---")

# Charts Row 1
r1_col1, r1_col2 = st.columns([7, 5])

with r1_col1:
    st.subheader("🗓️ Monthly Revenue Trend")
    monthly_trend = filtered_df.groupby("Month")["Revenue"].sum().reset_index()
    fig_monthly = px.line(
        monthly_trend,
        x="Month",
        y="Revenue",
        markers=True,
        line_shape="spline",
        color_discrete_sequence=["#38BDF8"],
    )
    fig_monthly.update_layout(
        template="plotly_dark",
        xaxis_title="Month",
        yaxis_title="Revenue ($)",
        margin=dict(l=20, r=20, t=20, b=20),
        height=350,
    )
    st.plotly_chart(fig_monthly, use_container_width=True)

with r1_col2:
    st.subheader("🌐 Revenue Share by Region")
    reg_rev = filtered_df.groupby("Region")["Revenue"].sum().reset_index()
    fig_pie = px.pie(
        reg_rev,
        names="Region",
        values="Revenue",
        hole=0.4,
        color_discrete_sequence=px.colors.qualitative.Pastel,
    )
    fig_pie.update_layout(
        template="plotly_dark",
        margin=dict(l=20, r=20, t=20, b=20),
        height=350,
    )
    st.plotly_chart(fig_pie, use_container_width=True)

# Charts Row 2
r2_col1, r2_col2 = st.columns([6, 6])

with r2_col1:
    st.subheader("📦 Revenue by Category")
    cat_rev = filtered_df.groupby("Category")["Revenue"].sum().reset_index().sort_values("Revenue", ascending=False)
    fig_cat = px.bar(
        cat_rev,
        x="Category",
        y="Revenue",
        color="Category",
        color_discrete_sequence=px.colors.qualitative.Bold,
    )
    fig_cat.update_layout(
        template="plotly_dark",
        xaxis_title="Category",
        yaxis_title="Revenue ($)",
        margin=dict(l=20, r=20, t=20, b=20),
        height=350,
        showlegend=False,
    )
    st.plotly_chart(fig_cat, use_container_width=True)

with r2_col2:
    st.subheader("⭐ Top 5 Products by Revenue")
    top_prod = filtered_df.groupby("Product")["Revenue"].sum().reset_index().sort_values("Revenue", ascending=True).tail(5)
    fig_prod = px.bar(
        top_prod,
        x="Revenue",
        y="Product",
        orientation="h",
        color_discrete_sequence=["#A855F7"],
    )
    fig_prod.update_layout(
        template="plotly_dark",
        xaxis_title="Revenue ($)",
        yaxis_title="Product",
        margin=dict(l=20, r=20, t=20, b=20),
        height=350,
    )
    st.plotly_chart(fig_prod, use_container_width=True)

# Chart Row 3
st.subheader("💳 Orders by Payment Method")
pay_counts = filtered_df["PaymentMethod"].value_counts().reset_index()
pay_counts.columns = ["PaymentMethod", "Orders"]
fig_pay = px.bar(
    pay_counts,
    x="PaymentMethod",
    y="Orders",
    color="PaymentMethod",
    color_discrete_sequence=px.colors.qualitative.Safe,
)
fig_pay.update_layout(
    template="plotly_dark",
    xaxis_title="Payment Method",
    yaxis_title="Number of Orders",
    margin=dict(l=20, r=20, t=20, b=20),
    height=300,
    showlegend=False,
)
st.plotly_chart(fig_pay, use_container_width=True)

# ---------------------------------------------------------------
# DATA EXPLORER TABLE
# ---------------------------------------------------------------
st.markdown("---")
with st.expander("🔍 Explore Filtered Dataset"):
    st.dataframe(filtered_df, use_container_width=True)
    csv = filtered_df.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="📥 Download Filtered CSV Data",
        data=csv,
        file_name="filtered_sales_data.csv",
        mime="text/csv",
    )
