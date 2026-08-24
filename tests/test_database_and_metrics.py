import pandas as pd

from src.database import fetch_sales, initialize_database, revenue_by_region
from src.metrics import calculate_kpis


def test_database_load_query_and_kpis(tmp_path):
    csv_path = tmp_path / "sales.csv"
    db_path = tmp_path / "sales.db"
    pd.DataFrame(
        [
            {
                "order_id": "A-1",
                "order_date": "2025-01-01",
                "region": "North",
                "category": "Electronics",
                "product": "Mouse",
                "quantity": 2,
                "unit_price": 25,
                "discount_pct": 0,
                "cost_per_unit": 10,
            },
            {
                "order_id": "A-2",
                "order_date": "2025-01-02",
                "region": "South",
                "category": "Office",
                "product": "Pen Set",
                "quantity": 5,
                "unit_price": 10,
                "discount_pct": 0,
                "cost_per_unit": 4,
            },
        ]
    ).to_csv(csv_path, index=False)

    assert initialize_database(csv_path, db_path) == 2
    data = fetch_sales(db_path)
    kpis = calculate_kpis(data)
    summary = revenue_by_region(db_path)

    assert kpis["revenue"] == 100.0
    assert kpis["profit"] == 60.0
    assert kpis["orders"] == 2
    assert set(summary["region"]) == {"North", "South"}


def test_empty_kpis_are_zero():
    empty = pd.DataFrame(columns=["sales", "profit", "order_id"])
    assert calculate_kpis(empty)["average_order_value"] == 0.0

