#!/bin/bash

set -e

export HADOOP_HOME=/opt/hadoop
export HADOOP_PREFIX=/opt/hadoop
export HADOOP_CONF_DIR=/opt/hadoop/etc/hadoop

export HIVE_HOME=/opt/hive
export PATH=$PATH:$HADOOP_HOME/bin:$HADOOP_HOME/sbin:$HIVE_HOME/bin

SERVICE=${SERVICE_NAME}

echo "========================================="
echo "Starting Hive service: $SERVICE"
echo "========================================="

if [ "$SERVICE" = "metastore" ]; then

    echo "Waiting for PostgreSQL..."

    until nc -z hive-postgres 5432; do
        sleep 2
    done

    echo "PostgreSQL is ready."

    echo "Initializing Metastore Schema..."

    schematool \
        -dbType postgres \
        -initSchema \
        || true

    echo "Starting Hive Metastore..."

    exec hive --service metastore

elif [ "$SERVICE" = "hiveserver2" ]; then

    echo "Waiting for Hive Metastore..."

    until nc -z hive-metastore 9083; do
        sleep 2
    done

    echo "Hive Metastore is ready."

    echo "Starting HiveServer2..."

    exec hive --service hiveserver2

else

    echo "Unknown SERVICE_NAME: $SERVICE"

    exit 1

fi