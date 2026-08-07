# Hive Integration Notes (Paused)

## Why Hive implementation was paused

The original goal was to use **Apache Hive** for querying transformed Parquet data stored in HDFS. However, after several implementation attempts, the setup proved significantly more complex than expected for the current project timeline.

## What was completed

* Hadoop NameNode and DataNode configured successfully
* Spark configured and running
* ETL pipeline created using PySpark
* Transformed data successfully written as Parquet files to HDFS
* PostgreSQL configured as the Hive Metastore database
* Multiple Hive Docker images evaluated
* Custom Hive Docker image created and tested
* Hive Metastore schema initialized successfully

## Issues encountered

### 1. Apache Hive 4.x Docker Image

* Hive Metastore could be started.
* HiveServer2 repeatedly failed to accept client connections.
* Beeline always returned:

```
Connection refused
Could not open client transport with JDBC URI
```

Despite:

* Metastore running
* Schema initialized
* Port 10000 exposed
* Configuration files mounted correctly

The root cause could not be identified within a reasonable amount of time.

---

### 2. Hive Configuration Complexity

Hive requires many configuration files and dependencies, including:

* hive-site.xml
* core-site.xml
* hdfs-site.xml
* Hadoop environment variables
* Hive Metastore configuration
* Warehouse directory configuration
* Tez configuration
* JDBC drivers
* Java classpath
* Hadoop installation compatibility

Small configuration differences can prevent HiveServer2 from starting correctly.

---

### 3. Docker Image Compatibility

Several images were evaluated:

* apache/hive:4.0.1
* apache/hive:standalone-metastore-nightly
* bde2020/hive (very old)
* Custom Hive 3.1.3 image

Each introduced different compatibility issues.

---

### 4. Time vs. Benefit

Continuing to debug Hive would likely require several additional days.

The objective of this project is to demonstrate a complete data engineering pipeline rather than mastering Hive deployment.

At this stage, further Hive debugging provides limited value compared to continuing with analytics.

## Decision

Hive integration is **paused** for this project.

The ETL pipeline already produces Parquet files successfully.

Instead of Hive, analytics will be implemented using **DuckDB**, which:

* Reads Parquet files directly
* Supports standard SQL
* Requires almost no configuration
* Integrates easily with Python
* Is widely used for local analytical workloads

## Current Pipeline

```
Yahoo Finance CSV
        │
        ▼
PySpark ETL
        │
        ▼
Parquet
        │
        ├── HDFS (Data Lake)
        └── Local Parquet
                │
                ▼
             DuckDB
                │
                ▼
        Analytical Reports
```

## Future Enhancement

Hive can be revisited later as a separate enhancement once the complete pipeline is finished.

Possible future work:

* Resolve HiveServer2 startup issue
* Connect DuckDB and Hive for comparison
* Demonstrate querying the same Parquet data using both Hive and DuckDB
* Add Hive partitioning and optimization examples
