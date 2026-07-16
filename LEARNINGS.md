# What I Learned - Hadoop & Docker

## Project

**Stock Market ETL Pipeline**

---

# Docker Concepts

## 1. Docker Containers

* Containers are lightweight isolated environments.
* Each Hadoop service (NameNode, DataNode) runs inside its own container.
* Containers communicate through a Docker network.

---

## 2. Docker Images

* Images are templates used to create containers.
* Used:

  * `bde2020/hadoop-namenode`
  * `bde2020/hadoop-datanode`

---

## 3. Docker Volumes

Purpose:

* Persist data even if containers are deleted.

NameNode Volume:

```yaml
namenode-data:/hadoop/dfs/name
```

Stores:

* HDFS Metadata

DataNode Volume:

```yaml
datanode-data:/hadoop/dfs/data
```

Stores:

* Actual HDFS blocks

---

## 4. Docker Network

Created:

```yaml
networks:
  hadoop-network:
```

Purpose:

* Allows NameNode and DataNode to communicate using hostnames.

Example:

```text
NameNode <-------> DataNode
```

---

## 5. depends_on

```yaml
depends_on:
  - namenode
```

Meaning:

* Docker starts NameNode before DataNode.

Important:

* It **does not** guarantee NameNode is fully ready.

---

## 6. SERVICE_PRECONDITION

```yaml
SERVICE_PRECONDITION: "namenode:9870"
```

Purpose:

* DataNode waits until NameNode becomes reachable before starting Hadoop services.

---

## 7. Hostname

```yaml
hostname: namenode
```

Purpose:

* Used for communication inside Docker network.

---

# Hadoop Concepts

## 1. HDFS

HDFS = Hadoop Distributed File System

Purpose:

* Distributed storage system
* Stores huge files across multiple machines.

---

## 2. NameNode

Role:

* Master node
* Stores metadata only.

Metadata includes:

* File names
* Folder structure
* Block locations
* Permissions

NameNode never stores actual file data.

---

## 3. DataNode

Role:

* Worker node

Stores:

* Actual file blocks

One DataNode can store millions of blocks.

---

## 4. HDFS Block

Large files are divided into blocks.

Example:

300 MB file

↓

Block 1

Block 2

Block 3

Each block is stored inside DataNode.

---

## 5. Replication

Configuration:

```yaml
HDFS_CONF_dfs_replication: 1
```

Purpose:

* Number of copies maintained for every block.

Development:

* Replication = 1

Production:

* Usually Replication = 3

Higher replication provides better fault tolerance.

---

## 6. CORE_CONF_fs_defaultFS

```yaml
CORE_CONF_fs_defaultFS: hdfs://namenode:9000
```

Purpose:

* Defines the default HDFS location.
* Every Hadoop component uses this to locate HDFS.

---

## 7. Cluster Name

```yaml
CLUSTER_NAME: stock-cluster
```

Purpose:

* Identifies the Hadoop cluster.
* Every node in the cluster belongs to the same cluster name.

---

## 8. HDFS Communication

File Upload Flow:

Client

↓

NameNode

↓

Metadata Created

↓

Client uploads blocks

↓

DataNode stores blocks

The file data never passes through the NameNode.

---

## 9. NameNode vs DataNode

| NameNode                  | DataNode           |
| ------------------------- | ------------------ |
| Stores metadata           | Stores actual data |
| Master                    | Worker             |
| Maintains block locations | Stores HDFS blocks |
| Small amount of storage   | Large storage      |

---

## 10. Hadoop Cluster Created

Built a working Hadoop cluster using Docker.

Components:

* 1 NameNode
* 1 DataNode
* Docker Network
* Docker Volumes
* HDFS successfully initialized
* Live DataNode connected
* Verified using:

```bash
hdfs dfsadmin -report
```

Result:

* Live DataNode = 1
* Healthy HDFS Cluster
* No under-replicated blocks
* No missing blocks

---

# Key Learning

* Docker provides isolated environments for Hadoop services.
* Docker Network enables inter-container communication.
* Docker Volumes persist HDFS data.
* NameNode stores metadata, while DataNode stores actual data blocks.
* HDFS distributes storage across DataNodes.
* Replication improves fault tolerance.
* Every Hadoop service needs to know where HDFS is using `fs.defaultFS`.
* A healthy HDFS cluster can be verified using `hdfs dfsadmin -report`.
