from pathlib import Path

# Local Directories
RAW_DATA_DIR = Path("data/raw")

# Container Directories
CONTAINER_RAW_DATA_DIR = "/data/raw"

# Default download settings
DEFAULT_PERIOD = "1y"
DEFAULT_INTERVAL = "1d"

# HDFS
HDFS_RAW_DIR = "/stock-market/raw"

HDFS_HOST = "namenode"
HDFS_PORT = 9000

HDFS_URI = f"hdfs://{HDFS_HOST}:{HDFS_PORT}"

HDFS_PROCESSED_DIR = "/stock-market/processed"

# Docker
NAMENODE_CONTAINER = "namenode"

# Stock symbols
STOCKS = [
    "RELIANCE.NS",
    "TCS.NS",
    "INFY.NS"
]