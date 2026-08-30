import logging

from pyspark.sql import SparkSession
from pyspark.sql.functions import (
    col,
    input_file_name,
    regexp_extract,
    to_date,
)

from config.settings import (
    HDFS_URI,
    HDFS_RAW_DIR,
    HDFS_PROCESSED_DIR,
    PROCESSED_DATA_DIR,
)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)


def create_spark_session() -> SparkSession:
    """
    Create and return Spark Session.
    """

    logging.info("Creating Spark Session...")

    spark = (
        SparkSession.builder
        .appName("Stock Market ETL")
        .master("local[*]")
        .getOrCreate()
    )

    logging.info("Spark Session created successfully.")

    return spark


def read_raw_data(spark: SparkSession):
    """
    Read all CSV files from HDFS Raw layer.
    """

    input_path = f"{HDFS_URI}{HDFS_RAW_DIR}"

    logging.info(f"Reading files from: {input_path}")

    df = (
        spark.read
        .option("header", True)
        .option("inferSchema", True)
        .csv(input_path)
    )

    df.printSchema()
    df.show(5, truncate=False)
    print(df.columns)

    return df


def transform_data(df):
    """
    Apply data transformations.
    """

    logging.info("Applying transformations...")

    df = (
        df
        .withColumn("SourceFile", input_file_name())
        .withColumn(
            "Ticker",
            regexp_extract(
                col("SourceFile"),
                r"([A-Z]+)_NS\.csv",
                1,
            ),
        )
        .withColumn(
            "Date",
            to_date(col("Date"), "yyyy-MM-dd"),
        )
        .dropDuplicates()
        .dropna(subset=["Date", "Open", "High", "Low", "Close", "Volume"])
    )

    logging.info("Transformations completed.")

    return df


def write_processed_data(df):
    """
    Write transformed data to HDFS as Parquet.
    """

    output_path = f"{HDFS_URI}{HDFS_PROCESSED_DIR}"
    logging.info(f"Writing Parquet to: {output_path}")

    (
        df.write
        .mode("overwrite")
        .parquet(output_path)
    )

    logging.info("HDFS Parquet files written successfully.")

    local_output_path = str(PROCESSED_DATA_DIR)
    logging.info(f"Writing Parquet locally: {local_output_path}")

    (
        df.write
        .mode("overwrite")
        .parquet(local_output_path)
    )

    logging.info("Local Parquet files written successfully.")

def main():

    spark = create_spark_session()

    df = read_raw_data(spark)

    logging.info("Raw Schema")
    df.printSchema()

    transformed_df = transform_data(df)

    logging.info("Transformed Schema")
    transformed_df.printSchema()

    transformed_df.show(10, truncate=False)

    write_processed_data(transformed_df)

    spark.stop()

    logging.info("Spark Session stopped.")


if __name__ == "__main__":
    main()