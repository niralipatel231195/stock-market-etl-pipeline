```text
Yahoo Finance
     │
     ▼
Python / yfinance
     │
     ▼
Raw CSV Files
     │
     ▼
HDFS Raw Layer
/stock-market/raw
     │
     ▼
PySpark ETL
     │
     ├── Data cleaning
     ├── Duplicate removal
     ├── Date conversion
     ├── Ticker extraction
     └── Schema transformation
     │
     ▼
Parquet
     │
     ▼
HDFS Processed Layer
/stock-market/processed
     │
     │ Local analytical copy
     ▼
data/processed/stock_market.parquet
     │
     ▼
DuckDB
     │
     ▼
SQL Analytics
```