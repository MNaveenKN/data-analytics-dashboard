import pandas as pd
import pytest

from src.data_processing import clean_sales_data, filter_sales_data


def raw_rows():
    return pd.DataFrame(
        [
            {
                "order_id": "A-1",
                "order_date": "2025-01-01",
                "region": " north ",
                "category": "electronics",
                "product": "mouse",
                "quantity": 2,
                "unit_price": 25,
                "discount_pct": 10,
                "cost_per_unit": 12,
            },
            {
                "order_id": "A-2",
                "order_date": "invalid",
                "region": "South",
                "category": "Office",
                "product": "Pen",
                "quantity": 1,
                "unit_price": 5,
                "discount_pct": 0,
                "cost_per_unit": 2,
            },
        ]
    )


def test_clean_sales_data_calculates_business_fields():
    cleaned = clean_sales_data(raw_rows())
    assert len(cleaned) == 1
    assert cleaned.loc[0, "region"] == "North"
    assert cleaned.loc[0, "sales"] == 45.0
    assert cleaned.loc[0, "profit"] == 21.0


def test_filter_sales_data_filters_region_and_category():
    cleaned = clean_sales_data(raw_rows())
    result = filter_sales_data(
        cleaned, "2025-01-01", "2025-01-31", ["North"], ["Electronics"]
    )
    assert len(result) == 1


def test_missing_columns_raise_helpful_error():
    with pytest.raises(ValueError, match="Missing required columns"):
        clean_sales_data(pd.DataFrame({"order_id": ["A-1"]}))

