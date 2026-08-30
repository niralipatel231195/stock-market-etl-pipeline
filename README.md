# Stock Market ETL Pipeline

An end-to-end stock market data engineering pipeline built using **Python, Docker, Hadoop HDFS, PySpark, Parquet, and DuckDB**.

## Project Goal

The objective of this project is to build and understand a complete data engineering pipeline using real stock market data.

The pipeline covers:

* Data extraction
* Raw data storage
* Distributed data processing
* Data cleaning and transformation
* Columnar data storage using Parquet
* Analytical querying using DuckDB

The project is designed as a practical demonstration of an ETL workflow using the Hadoop and Spark ecosystem.

---

## Architecture

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

---

## Technologies

* **Python** — Data extraction and project scripting
* **yfinance** — Stock market data extraction from Yahoo Finance
* **Hadoop HDFS** — Distributed raw and processed data storage
* **PySpark** — Data transformation and ETL processing
* **Parquet** — Columnar storage format for processed data
* **DuckDB** — Analytical SQL query engine
* **Docker** — Containerized Hadoop and Spark environment
* **PostgreSQL** — Used as the Hive Metastore database during the initial Hive setup attempt (later not used in final pipeline)
* **Ubuntu / WSL** — Development environment
* **Git / GitHub** — Version control and project portfolio

---

## Data Flow

### 1. Data Extraction

Stock market data is downloaded using Python and `yfinance`.

Currently, the pipeline processes:

* RELIANCE.NS
* TCS.NS
* INFY.NS

The raw data is stored as CSV files.

```text
data/raw/
├── INFY_NS.csv
├── RELIANCE_NS.csv
└── TCS_NS.csv
```

### 2. HDFS Raw Layer

The raw CSV files are uploaded into the HDFS raw layer:

```text
/stock-market/raw/
```

HDFS provides the distributed storage layer for the pipeline.

### 3. PySpark Transformation

PySpark reads the raw CSV files from HDFS and performs transformations including:

* Schema inference
* Date conversion
* Ticker extraction from source filenames
* Source file tracking
* Duplicate removal
* Null value removal

### 4. Processed Parquet Layer

The transformed dataset is written to HDFS in **Parquet** format:

```text
/stock-market/processed/
```

Parquet is used as the processed data format because it is a columnar format that is well suited for analytical workloads.

### 5. DuckDB Analytics

A local copy of the processed Parquet dataset is maintained for analytical querying:

```text
data/processed/stock_market.parquet
```

DuckDB reads the Parquet file directly and performs SQL-based analysis.

---

## Project Structure

```text
stock-market-etl-pipeline/
│
├── analysis/
│   └── stock_analysis.py
│
├── config/
│   ├── __init__.py
│   └── settings.py
│
├── data/
│   ├── raw/
│   │   ├── INFY_NS.csv
│   │   ├── RELIANCE_NS.csv
│   │   └── TCS_NS.csv
│   │
│   └── processed/
│       └── stock_market.parquet
│
├── docker/
│   ├── docker-compose.yml
│   ├── hadoop-conf/
│   └── ...
│
├── scripts/
│   ├── extract_stock_data.py
│   ├── transform_stock_data.py
│   └── upload_to_hdfs.py
│
├── README.md
└── requirements.txt
```

---

## Project Status

### Completed

* [x] Repository created
* [x] Project structure created
* [x] Docker environment configured
* [x] Hadoop NameNode configured
* [x] Hadoop DataNode configured
* [x] HDFS connectivity verified
* [x] Yahoo Finance data extraction
* [x] Raw CSV data created
* [x] Raw data uploaded to HDFS
* [x] PySpark ETL pipeline developed
* [x] Data cleaning and transformation implemented
* [x] Parquet output generated
* [x] Processed data stored in HDFS
* [x] HDFS → local Parquet analytical copy created
* [x] DuckDB installed and configured
* [x] DuckDB successfully reading Parquet

### In Progress

* [ ] Complete stock market SQL analytics
* [ ] Calculate daily returns
* [ ] Analyze price performance
* [ ] Analyze trading volume
* [ ] Calculate volatility
* [ ] Add moving-average analysis
* [ ] Generate final analytical insights
* [ ] Finalize project documentation
* [ ] Prepare GitHub portfolio presentation

---

## Running the Pipeline

### Extract Stock Data

From the project root:

```bash
python -m scripts.extract_stock_data
```

### Upload Raw Data to HDFS

```bash
python -m scripts.upload_to_hdfs
```

### Run PySpark Transformation

The transformation runs inside the Spark Docker container:

```bash
docker exec spark bash -c \
'cd /app && PYTHONPATH=/app /opt/spark/bin/spark-submit scripts/transform_stock_data.py'
```

### Run DuckDB Analysis

```bash
python analysis/stock_analysis.py
```

---

## HDFS Layers

### Raw Layer

```text
/stock-market/raw/
```

Contains the original extracted CSV files.

### Processed Layer

```text
/stock-market/processed/
```

Contains the transformed Parquet dataset generated by PySpark.

---

## Why Hive Is Not Used

Hive was initially planned as part of the project architecture. However, the Hive Docker setup introduced significant compatibility and configuration issues involving:

* Hive version compatibility
* Java runtime compatibility
* Hadoop environment configuration
* Hive Metastore configuration
* PostgreSQL Metastore connectivity
* HiveServer2 startup
* Docker networking and service discovery

Resolving these issues would have required additional infrastructure work without providing significant value for the primary objective of this portfolio project.

Therefore, Hive was not continued.

The project instead uses **DuckDB for analytical SQL querying over the processed Parquet dataset**.

This keeps the project focused on the core data engineering workflow:

```text
Extract → Store → Transform → Parquet → Analyze
```

The Hive investigation and related troubleshooting are documented separately for future reference.

---

## Current Pipeline

```text
Python / yfinance
        ↓
      CSV
        ↓
      HDFS
        ↓
     PySpark
        ↓
    Parquet
        ↓
      HDFS
        ↓
 Local Parquet Copy
        ↓
     DuckDB
        ↓
   SQL Analytics
```

---

## Future Improvements

Potential improvements include:

* Increase dataset volume
* Add more stocks and market instruments
* Introduce incremental processing
* Add partitioning to the Parquet dataset
* Implement data quality checks
* Add Airflow orchestration
* Add automated pipeline execution
* Add analytical dashboards
* Explore querying Parquet directly from distributed storage
* Add CI/CD for the project
