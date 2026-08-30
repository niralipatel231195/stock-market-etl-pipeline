import logging
import subprocess
from pathlib import Path

from config.settings import (
    CONTAINER_RAW_DATA_DIR,
    HDFS_RAW_DIR,
    NAMENODE_CONTAINER,
    RAW_DATA_DIR,
)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

def upload_file_to_hdfs(file_path: Path) -> bool:
    """
    Upload a single CSV file to HDFS.

    Args:
        file_path (Path): Local CSV file path.

    Returns:
        bool: True if upload succeeds, otherwise False.
    """

    logging.info(f"Uploading {file_path.name} to HDFS")

    container_file_path: str = (f"{CONTAINER_RAW_DATA_DIR}/{file_path.name}")

    result = subprocess.run(
        [
            "docker",
            "exec",
            NAMENODE_CONTAINER,
            "hdfs",
            "dfs",
            "-put",
            "-f",
            container_file_path,
            HDFS_RAW_DIR,
        ],
        capture_output=True,
        text=True,
    )

    if result.returncode == 0:
        logging.info(f"{file_path.name} uploaded successfully.")
        return True

    logging.error(result.stderr)
    return False

def upload_directory_to_hdfs(directory: Path) -> None:
    """
    Upload all CSV files from a directory to HDFS.

    Args:
        directory (Path): Local directory containing CSV files.
    """

    csv_files = sorted(directory.glob("*.csv"))

    if not csv_files:
        logging.warning(f"No CSV files found in {directory}")
        return

    logging.info(f"Found {len(csv_files)} CSV file(s).")

    successful_uploads = 0

    for file_path in csv_files:
        if upload_file_to_hdfs(file_path):
            successful_uploads += 1

    logging.info(
        f"Upload completed. "
        f"Success: {successful_uploads}/{len(csv_files)}"
    )

def main():
    upload_directory_to_hdfs(RAW_DATA_DIR)

if __name__ == "__main__":
    main()