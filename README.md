# Data Analytics Dashboard

An interactive sales dashboard that turns a raw CSV into an analysis-ready SQLite table, calculates business metrics, and lets users explore results with filters and charts.

## Highlights

- Cleans column names, dates, numbers, missing values, duplicates, and text labels
- Uses NumPy and Pandas to derive sales, cost, profit, and profit margin
- Loads the cleaned dataset into SQLite and creates useful indexes
- Includes a reusable SQL aggregation for regional performance
- Filters by date range, region, and product category
- Displays revenue, profit, orders, average order value, and margin
- Shows time trends, category revenue, regional profit, and top products
- Includes 42 sample sales rows and automated tests

## Tech stack

Python, SQL/SQLite, Pandas, NumPy, Streamlit, pytest

## Project structure

```text
data-analytics-dashboard/
├── data/
│   └── sample_sales.csv
├── src/
│   ├── data_processing.py
│   ├── database.py
│   └── metrics.py
├── tests/
│   ├── test_data_processing.py
│   └── test_database_and_metrics.py
├── dashboard.py
├── .gitignore
├── README.md
└── requirements.txt
```

## Run locally

1. Create and activate a virtual environment:

   ```bash
   python -m venv .venv
   # Windows
   .venv\Scripts\activate
   # macOS/Linux
   source .venv/bin/activate
   ```

2. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

3. Start the dashboard:

   ```bash
   streamlit run dashboard.py
   ```

The first run cleans `data/sample_sales.csv` and creates `data/sales.db`. The database is ignored by Git because it is generated from the included CSV.

## Run tests

```bash
pytest -q
```

## Use your own dataset

Replace `data/sample_sales.csv` with a CSV containing these columns:

```text
order_id, order_date, region, category, product, quantity,
unit_price, discount_pct, cost_per_unit, customer_rating (optional)
```

Then select **Reload sample data** in the dashboard sidebar.

## Portfolio talking points

- Explain why the raw file is cleaned before it enters the database.
- Show how the SQLite query in `src/database.py` performs a grouped business report.
- Discuss how date and category filters change every KPI and chart.
- Describe why revenue, profit, and order count answer different business questions.

