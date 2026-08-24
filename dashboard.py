"""Interactive Streamlit sales dashboard."""

from pathlib import Path

import pandas as pd
import streamlit as st

from src.data_processing import filter_sales_data
from src.database import fetch_sales, initialize_database
from src.metrics import calculate_kpis

BASE_DIR = Path(__file__).resolve().parent
CSV_PATH = BASE_DIR / "data" / "sample_sales.csv"
DB_PATH = BASE_DIR / "data" / "sales.db"

st.set_page_config(page_title="Sales Analytics", page_icon="📊", layout="wide")


@st.cache_data
def load_data() -> pd.DataFrame:
    if not DB_PATH.exists():
        initialize_database(CSV_PATH, DB_PATH)
    return fetch_sales(DB_PATH)


st.title("Sales Analytics Dashboard")
st.caption("Explore revenue, profit, orders, regions, categories, and products.")

with st.sidebar:
    st.header("Filters")
    if st.button("Reload sample data", width="stretch"):
        initialize_database(CSV_PATH, DB_PATH)
        load_data.clear()
        st.success("Sample data reloaded.")

data = load_data()

with st.sidebar:
    date_value = st.date_input(
        "Order date range",
        value=(data["order_date"].min().date(), data["order_date"].max().date()),
        min_value=data["order_date"].min().date(),
        max_value=data["order_date"].max().date(),
    )
    selected_regions = st.multiselect(
        "Region", sorted(data["region"].unique()), default=sorted(data["region"].unique())
    )
    selected_categories = st.multiselect(
        "Category",
        sorted(data["category"].unique()),
        default=sorted(data["category"].unique()),
    )

if isinstance(date_value, tuple) and len(date_value) == 2:
    start_date, end_date = date_value
else:
    start_date = end_date = date_value

filtered = filter_sales_data(
    data, start_date, end_date, selected_regions, selected_categories
)

if filtered.empty:
    st.warning("No rows match the current filters. Try a wider selection.")
    st.stop()

kpis = calculate_kpis(filtered)
metric_columns = st.columns(5)
metric_columns[0].metric("Revenue", f"${kpis['revenue']:,.2f}")
metric_columns[1].metric("Profit", f"${kpis['profit']:,.2f}")
metric_columns[2].metric("Orders", f"{kpis['orders']:,}")
metric_columns[3].metric("Average order", f"${kpis['average_order_value']:,.2f}")
metric_columns[4].metric("Profit margin", f"{kpis['profit_margin_pct']:.1f}%")

st.divider()

monthly = (
    filtered.assign(month=filtered["order_date"].dt.to_period("M").dt.to_timestamp())
    .groupby("month", as_index=False)[["sales", "profit"]]
    .sum()
    .set_index("month")
)
st.subheader("Revenue and profit trend")
st.line_chart(monthly, y=["sales", "profit"], color=["#2563EB", "#16A34A"])

left, right = st.columns(2)
with left:
    st.subheader("Revenue by category")
    category_sales = (
        filtered.groupby("category")["sales"].sum().sort_values(ascending=False)
    )
    st.bar_chart(category_sales, color="#7C3AED")

with right:
    st.subheader("Profit by region")
    region_profit = filtered.groupby("region")["profit"].sum().sort_values(ascending=False)
    st.bar_chart(region_profit, color="#EA580C")

st.subheader("Top products")
top_products = (
    filtered.groupby("product", as_index=False)
    .agg(revenue=("sales", "sum"), profit=("profit", "sum"), units=("quantity", "sum"))
    .sort_values("revenue", ascending=False)
    .head(10)
)
top_products[["revenue", "profit"]] = top_products[["revenue", "profit"]].round(2)
st.dataframe(top_products, width="stretch", hide_index=True)

with st.expander("View filtered sales rows"):
    display_data = filtered.copy()
    display_data["order_date"] = display_data["order_date"].dt.date
    st.dataframe(display_data, width="stretch", hide_index=True)
