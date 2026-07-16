# Hadoop & Docker Project - Interview Notes

## Project Overview

I built a Hadoop HDFS cluster from scratch using Docker instead of installing Hadoop directly on my machine. My goal was to understand Hadoop architecture and learn how distributed storage works.

---

## Why I Used Docker

I used Docker because every Hadoop component can run in its own isolated container.

Instead of installing Hadoop manually, Docker allowed me to create:

* One NameNode container
* One DataNode container

This approach makes the environment portable, reproducible, and easy to manage.

---

## Hadoop Architecture

HDFS mainly consists of two components:

### NameNode

The NameNode is the master node.

Its responsibility is to store metadata only, such as:

* File names
* Directory structure
* Block locations
* Permissions

The NameNode never stores the actual file contents.

---

### DataNode

The DataNode is the worker node.

It stores the actual HDFS blocks.

One DataNode can store millions of blocks depending on available storage.

---

## How File Upload Works

When a client uploads a file:

1. The client contacts the NameNode.
2. The NameNode decides where each block should be stored.
3. The client directly uploads the blocks to the DataNode.
4. The NameNode only updates the metadata.

This design prevents the NameNode from becoming a performance bottleneck.

---

## HDFS Blocks

HDFS does not store a large file as a single file.

It splits the file into multiple blocks.

For example:

A 300 MB file becomes:

* Block 1
* Block 2
* Block 3

These blocks are stored on DataNodes.

---

## Replication

HDFS supports block replication for fault tolerance.

In my development environment, I configured:

Replication Factor = 1

because I had only one DataNode.

In production, replication is typically 3, so every block exists on three different DataNodes. This ensures data remains available even if one server fails.

---

## Docker Volumes

I created separate Docker volumes for NameNode and DataNode.

NameNode volume stores HDFS metadata.

DataNode volume stores actual file blocks.

Using Docker volumes ensures that data is not lost when containers are recreated.

---

## Docker Network

I created a dedicated Docker network so that NameNode and DataNode could communicate using hostnames.

For example:

* NameNode hostname: `namenode`
* DataNode hostname: `datanode`

Both services communicate through this internal Docker network.

---

## Important Docker Configurations

### depends_on

I used `depends_on` to ensure Docker starts the NameNode before the DataNode.

I also learned that `depends_on` only controls startup order and does not guarantee the service is fully ready.

---

### SERVICE_PRECONDITION

The DataNode waits until the NameNode becomes reachable before starting Hadoop services.

This avoids startup failures caused by the NameNode still initializing.

---

### CORE_CONF_fs_defaultFS

I configured:

`hdfs://namenode:9000`

This tells every Hadoop component where the default HDFS cluster is located.

---

## Cluster Verification

After creating the cluster, I verified it using:

```bash
hdfs dfsadmin -report
```

The report confirmed:

* One Live DataNode
* No missing blocks
* No corrupt replicas
* Healthy HDFS cluster

---

## Key Learnings

Through this project, I learned:

* Hadoop architecture
* Difference between NameNode and DataNode
* HDFS block storage
* Block replication
* Docker networking
* Docker volumes
* Hadoop cluster configuration
* How Docker is used to simulate distributed systems on a single machine

---

## Future Improvements

Next, I plan to extend this project by:

* Extracting stock market data from Yahoo Finance
* Storing raw data in HDFS
* Processing data using PySpark
* Creating Hive tables
* Performing analytical queries

This will convert the project into a complete end-to-end Data Engineering pipeline.
