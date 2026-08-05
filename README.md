# Stock Market ETL

A Hadoop-based stock market data pipeline built using Yahoo Finance, HDFS, Hive, PySpark, and PostgreSQL.

## Project Goal

The objective of this project is to learn the Hadoop ecosystem by building an end-to-end stock market data pipeline.

## Architecture

Yahoo Finance API
↓
Data Extraction
↓
HDFS
↓
Hive
↓
PySpark
↓
PostgreSQL
↓
Analytics

## Technologies

- Python
- Hadoop HDFS
- Hive
- PySpark
- PostgreSQL
- Docker
- Ubuntu (WSL)

## Project Status

- [x] Repository Created
- [x] Project Structure Created
- [ ] Hadoop Setup
- [ ] HDFS Operations
- [ ] Yahoo Finance Extraction
- [ ] Hive Integration
- [ ] Spark Analytics
- [ ] PostgreSQL Loading

```bash
python -m scripts.extract_stock_data
```

```bash
python -m scripts.upload_to_hdfs
```