"""SQLite loading and SQL reporting helpers."""

import sqlite3
from pathlib import Path

import pandas as pd

from src.data_processing import load_sales_csv


def initialize_database(csv_path: str | Path, db_path: str | Path) -> int:
    """Clean the CSV and replace the SQLite sales table. Return loaded row count."""
    data = load_sales_csv(csv_path)
    db_path = Path(db_path)
    db_path.parent.mkdir(parents=True, exist_ok=True)
    with sqlite3.connect(db_path) as connection:
        data.to_sql("sales", connection, if_exists="replace", index=False)
        connection.execute("CREATE INDEX IF NOT EXISTS idx_sales_date ON sales(order_date)")
        connection.execute("CREATE INDEX IF NOT EXISTS idx_sales_region ON sales(region)")
    return len(data)


def fetch_sales(db_path: str | Path) -> pd.DataFrame:
    """Read analysis-ready rows from SQLite."""
    with sqlite3.connect(db_path) as connection:
        data = pd.read_sql_query("SELECT * FROM sales ORDER BY order_date", connection)
    data["order_date"] = pd.to_datetime(data["order_date"])
    return data


def revenue_by_region(db_path: str | Path) -> pd.DataFrame:
    """Example SQL aggregation used in tests and easy to reuse in reports."""
    query = """
        SELECT region,
               ROUND(SUM(sales), 2) AS revenue,
               ROUND(SUM(profit), 2) AS profit,
               COUNT(DISTINCT order_id) AS orders
        FROM sales
        GROUP BY region
        ORDER BY revenue DESC
    """
    with sqlite3.connect(db_path) as connection:
        return pd.read_sql_query(query, connection)

