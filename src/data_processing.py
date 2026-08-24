"""Load, clean, validate, and filter sales data."""

from pathlib import Path

import numpy as np
import pandas as pd

REQUIRED_COLUMNS = {
    "order_id",
    "order_date",
    "region",
    "category",
    "product",
    "quantity",
    "unit_price",
    "discount_pct",
    "cost_per_unit",
}


def clean_sales_data(data: pd.DataFrame) -> pd.DataFrame:
    """Return analysis-ready sales rows without modifying the input DataFrame."""
    df = data.copy()
    df.columns = [column.strip().lower().replace(" ", "_") for column in df.columns]

    missing = REQUIRED_COLUMNS - set(df.columns)
    if missing:
        raise ValueError(f"Missing required columns: {', '.join(sorted(missing))}")

    df = df.drop_duplicates()
    df["order_date"] = pd.to_datetime(df["order_date"], errors="coerce")

    numeric_columns = [
        "quantity",
        "unit_price",
        "discount_pct",
        "cost_per_unit",
    ]
    if "customer_rating" in df.columns:
        numeric_columns.append("customer_rating")
    for column in numeric_columns:
        df[column] = pd.to_numeric(df[column], errors="coerce")

    text_columns = ["order_id", "region", "category", "product"]
    for column in text_columns:
        df[column] = df[column].astype("string").str.strip()

    df = df.dropna(
        subset=[
            "order_id",
            "order_date",
            "region",
            "category",
            "product",
            "quantity",
            "unit_price",
            "cost_per_unit",
        ]
    )
    df = df[(df["quantity"] > 0) & (df["unit_price"] > 0) & (df["cost_per_unit"] >= 0)]
    df["discount_pct"] = df["discount_pct"].fillna(0).clip(0, 100)

    for column in ["region", "category", "product"]:
        df[column] = df[column].str.title()

    if "customer_rating" in df.columns:
        df["customer_rating"] = df["customer_rating"].clip(1, 5)

    gross_sales = df["quantity"] * df["unit_price"]
    df["sales"] = gross_sales * (1 - df["discount_pct"] / 100)
    df["cost"] = df["quantity"] * df["cost_per_unit"]
    df["profit"] = df["sales"] - df["cost"]
    df["profit_margin_pct"] = np.where(
        df["sales"] > 0, (df["profit"] / df["sales"]) * 100, 0
    )

    money_columns = ["sales", "cost", "profit", "profit_margin_pct"]
    df[money_columns] = df[money_columns].round(2)
    return df.sort_values("order_date").reset_index(drop=True)


def load_sales_csv(csv_path: str | Path) -> pd.DataFrame:
    """Read and clean a sales CSV file."""
    return clean_sales_data(pd.read_csv(csv_path))


def filter_sales_data(
    data: pd.DataFrame,
    start_date,
    end_date,
    regions: list[str] | None = None,
    categories: list[str] | None = None,
) -> pd.DataFrame:
    """Apply dashboard filters to already-clean data."""
    start = pd.Timestamp(start_date)
    end = pd.Timestamp(end_date)
    mask = data["order_date"].between(start, end)
    if regions:
        mask &= data["region"].isin(regions)
    if categories:
        mask &= data["category"].isin(categories)
    return data.loc[mask].copy()

