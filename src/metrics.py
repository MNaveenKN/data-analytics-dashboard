"""Business metric calculations used by the dashboard."""

import pandas as pd


def calculate_kpis(data: pd.DataFrame) -> dict[str, float | int]:
    """Calculate the top-level business metrics for the selected rows."""
    revenue = float(data["sales"].sum()) if not data.empty else 0.0
    profit = float(data["profit"].sum()) if not data.empty else 0.0
    orders = int(data["order_id"].nunique()) if not data.empty else 0
    average_order_value = revenue / orders if orders else 0.0
    margin = (profit / revenue) * 100 if revenue else 0.0
    return {
        "revenue": round(revenue, 2),
        "profit": round(profit, 2),
        "orders": orders,
        "average_order_value": round(average_order_value, 2),
        "profit_margin_pct": round(margin, 2),
    }

