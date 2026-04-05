# Network & Port Configuration Guide

## 📡 Docker Network

All containers communicate via a single Docker bridge network: `hadoop-spark-network`

### Service Hostnames (Internal DNS)
- `hadoop-master` - Hadoop Master node
- `hadoop-worker-1` - Hadoop Worker 1
- `hadoop-worker-2` - Hadoop Worker 2
- `spark-master` - Spark Master node
- `spark-worker-1` - Spark Worker 1
- `spark-worker-2` - Spark Worker 2
- `jupyter` - Jupyter Notebook

---

## 🔌 Port Mapping

### Hadoop Services

| Service | Container Port | Host Port | Purpose |
|---------|---|---|---|
| NameNode RPC | 9000 | 9000 | HDFS client connections |
| NameNode Web UI | 9870 | 9870 | Hadoop NameNode UI |
| Secondary NameNode | 9868 | - | Internal only |
| DataNode | 50010 | - | Internal only |
| DataNode Web UI | 9864 | 9864 (worker1) / 9865 (worker2) | DataNode status |
| ResourceManager | 8032 | - | Internal only |
| ResourceManager Scheduler | 8030 | - | Internal only |
| ResourceManager Resource Tracker | 8031 | - | Internal only |
| ResourceManager Web UI | 8088 | 8088 | YARN UI |
| NodeManager Web UI | 8042 | 8042 (worker1) / 8043 (worker2) | NodeManager status |
| Job History Server | 10020 | - | Internal only |
| Job History Server Web UI | 19888 | - | Internal only |

### Spark Services

| Service | Container Port | Host Port | Purpose |
|---------|---|---|---|
| Spark Master | 7077 | 7077 | Spark cluster communication |
| Spark Master Web UI | 8080 | 8080 | Spark Master UI |
| Spark Worker | 7078 | 7078 (worker1) / 7079 (worker2) | Worker communication |
| Spark Worker Web UI | 8081 | 8081 (worker1) / 8082 (worker2) | Worker UI |
| Spark Driver UI | 4040 | 4040 | Application UI (dynamic) |
| Spark REST API | 6066 | 6066 | Rest API (optional) |

### Jupyter Services

| Service | Container Port | Host Port | Purpose |
|---------|---|---|---|
| Jupyter Notebook | 8888 | 8888 | Jupyter UI |

---

## 🌐 Accessing Services

### From Localhost (Windows/Local Machine)

| Service | URL |
|---------|-----|
| Hadoop NameNode | http://localhost:9870 |
| Hadoop YARN | http://localhost:8088 |
| Spark Master | http://localhost:8080 |
| Spark Worker 1 | http://localhost:8081 |
| Spark Worker 2 | http://localhost:8082 |
| Jupyter | http://localhost:8888 |

### From Inside Containers

Use container hostnames and internal ports:

```bash
# From Hadoop Master container
curl http://hadoop-master:9870

# From Spark container
curl http://spark-master:8080

# HDFS commands
hdfs dfs -fs hdfs://hadoop-master:9000 -ls /
```

### From PySpark Code

```python
from pyspark.sql import SparkSession

spark = SparkSession.builder \
    .master("spark://spark-master:7077") \
    .config("spark.hadoop.fs.defaultFS", "hdfs://hadoop-master:9000") \
    .getOrCreate()
```

---

## 📋 Environment Variables (inside containers)

```bash
# Java
JAVA_HOME=/usr/lib/jvm/java-11-openjdk-amd64

# Hadoop
HADOOP_HOME=/opt/hadoop
HADOOP_HDFS_HOME=/opt/hadoop
HADOOP_YARN_HOME=/opt/hadoop

# Spark
SPARK_HOME=/opt/spark

# LD_LIBRARY_PATH
LD_LIBRARY_PATH=/opt/hadoop/lib/native
```

---

## 🔄 Network Communication Flow

```
User/Local Browser
        ↓
   Localhost Ports
   (9870, 8088, 8080, 8888)
        ↓
Docker Port Mapping
        ↓
Docker Bridge Network (hadoop-spark-network)
        ↓
Container Internal Services
(hadoop-master, spark-master, jupyter, etc.)
```

---

## 🚨 Port Conflict Resolution

If any port is already in use on your machine, edit `docker-compose.yml`:

**Before:**
```yaml
ports:
  - "9870:9870"    # Hadoop NameNode
  - "8088:8088"    # YARN
```

**After (change host port):**
```yaml
ports:
  - "19870:9870"   # Access via localhost:19870
  - "18088:8088"   # Access via localhost:18088
```

---

## 💾 Volume Mounts

| Volume | Type | Host Location | Container Location | Purpose |
|--------|------|---|---|---|
| hadoop_config | Bind | `./config/hadoop` | `/config` | Hadoop config files |
| spark_config | Bind | `./config/spark` | `/config` | Spark config files |
| hadoop_namenode | Volume | `./volumes/hadoop_name` | `/data/namenode` | NameNode metadata |
| hadoop_datanode | Volume | `./volumes/hadoop_data/worker[1-2]` | `/data/datanode` | DataNode blocks |
| notebooks | Bind | `./notebooks` | `/home/jovyan/work` | Jupyter notebooks |

---

## 🔐 Security Notes

### Current Configuration
- All services accessible without authentication (development mode)
- SSH key-based authentication enabled between nodes
- Default user: hadoop (Hadoop services), spark (Spark services), jovyan (Jupyter)

### For Production
- Enable Kerberos authentication
- Configure firewall rules
- Use private Docker network (no port exposure)
- Enable TLS/SSL for all services
- Use proper user permissions

---

## 📊 Network Topology

```
┌────────────────────────────────────────────────────┐
│         Docker Host Machine                        │
│  (Windows/Linux/Mac)                               │
├────────────────────────────────────────────────────┤
│  localhost:9870 ──→ hadoop-master:9870             │
│  localhost:8088 ──→ hadoop-master:8088             │
│  localhost:8080 ──→ spark-master:8080              │
│  localhost:8888 ──→ jupyter:8888                   │
│                                                    │
│  ┌─────────────────────────────────────────────┐  │
│  │  Docker Bridge Network                      │  │
│  │  (hadoop-spark-network)                     │  │
│  │                                             │  │
│  │  ┌──────────────┐ ┌──────────┐            │  │
│  │  │ hadoop-      │ │ hadoop-  │            │  │
│  │  │ master:9000  │←→│ worker-1 │            │  │
│  │  └──────────────┘ └──────────┘            │  │
│  │         ↑ ↓              ↓                  │  │
│  │  ┌──────────────┐ ┌──────────┐            │  │
│  │  │ spark-       │ │ spark-   │            │  │
│  │  │ master:7077  │←→│ worker-1 │            │  │
│  │  └──────────────┘ └──────────┘            │  │
│  │         ↑ ↓                                │  │
│  │  ┌──────────────┐                         │  │
│  │  │ jupyter:8888 │                         │  │
│  │  └──────────────┘                         │  │
│  │                                             │  │
│  └─────────────────────────────────────────────┘  │
│                                                    │
└────────────────────────────────────────────────────┘
```

---

## 🧪 Testing Network Connectivity

### Test 1: Ping containers
```bash
# From host machine
docker exec hadoop-master ping spark-master
docker exec spark-master ping hadoop-master
```

### Test 2: Test HTTP endpoints
```bash
# From host machine
curl http://localhost:9870    # Hadoop NameNode
curl http://localhost:8088    # YARN UI
curl http://localhost:8080    # Spark Master
curl http://localhost:8888    # Jupyter
```

### Test 3: Test HDFS from Jupyter
```python
from pyspark.sql import SparkSession

spark = SparkSession.builder \
    .master("spark://spark-master:7077") \
    .config("spark.hadoop.fs.defaultFS", "hdfs://hadoop-master:9000") \
    .getOrCreate()

# This will test HDFS connectivity
spark.sparkContext.hadoopConfiguration.get("fs.defaultFS")
```

---

## 📝 Network Configuration Files

### core-site.xml
```xml
<property>
    <name>fs.defaultFS</name>
    <value>hdfs://hadoop-master:9000</value>
</property>
```

### yarn-site.xml
```xml
<property>
    <name>yarn.resourcemanager.hostname</name>
    <value>hadoop-master</value>
</property>
```

### spark-defaults.conf
```conf
spark.master                    spark://spark-master:7077
spark.hadoop.fs.defaultFS      hdfs://hadoop-master:9000
```

---

## 🔍 Debugging Network Issues

### Check Docker network
```bash
docker network ls
docker network inspect hadoop-spark-network
```

### Test DNS resolution inside container
```bash
docker exec hadoop-master nslookup spark-master
docker exec hadoop-master nslookup hadoop-worker-1
```

### Check port availability
```bash
# Windows
netstat -ano | findstr LISTEN

# Linux/Mac
lsof -i -P -n | grep LISTEN
```

### Monitor container network traffic
```bash
docker exec hadoop-master ss -tupln
```

---

**Network Configuration Ready! 🌐**
