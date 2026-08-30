import duckdb

PARQUET_FILE = "data/processed/stock_market.parquet"

con = duckdb.connect("data/processed/stock_market.duckdb")

print("DuckDB connected successfully.\n")

# 1. Dataset overview
print("=== DATASET OVERVIEW ===")

overview = con.execute(
    f"""
    SELECT
        COUNT(*) AS total_records,
        COUNT(DISTINCT Ticker) AS total_stocks,
        MIN(Date) AS start_date,
        MAX(Date) AS end_date
    FROM read_parquet('{PARQUET_FILE}')
    """
).fetchdf()

print(overview)

# 2. Records per stock
print("\n=== RECORDS PER STOCK ===")

records = con.execute(
    f"""
    SELECT
        Ticker,
        COUNT(*) AS total_records,
        MIN(Date) AS start_date,
        MAX(Date) AS end_date
    FROM read_parquet('{PARQUET_FILE}')
    GROUP BY Ticker
    ORDER BY Ticker
    """
).fetchdf()

print(records)

# 3. Basic price statistics
print("\n=== PRICE STATISTICS ===")

stats = con.execute(
    f"""
    SELECT
        Ticker,
        ROUND(MIN(Low), 2) AS lowest_price,
        ROUND(MAX(High), 2) AS highest_price,
        ROUND(AVG(Close), 2) AS average_close,
        ROUND(AVG(Volume), 0) AS average_volume
    FROM read_parquet('{PARQUET_FILE}')
    GROUP BY Ticker
    ORDER BY Ticker
    """
).fetchdf()

print(stats)

con.close()