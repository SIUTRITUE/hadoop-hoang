# Hadoop-Spark Cluster on Docker Compose

Một hệ thống Big Data phân tán hoàn chỉnh chạy trên Docker Compose bao gồm Hadoop, Spark, và Jupyter Notebook.

## 📋 Kiến Trúc Hệ Thống

```
┌─────────────────────────────────────────────────────────────┐
│                    Docker Network                           │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  ┌────────────────────────────────────────────────────────┐ │
│  │             HADOOP CLUSTER                            │ │
│  │  ┌──────────────┐  ┌──────────┐  ┌──────────┐        │ │
│  │  │ Master Node  │  │ Worker 1 │  │ Worker 2 │        │ │
│  │  │(NameNode +   │  │(DataNode │  │(DataNode │        │ │
│  │  │ResourceMgr)  │  │+NodeMgr) │  │+NodeMgr) │        │ │
│  │  └──────────────┘  └──────────┘  └──────────┘        │ │
│  └────────────────────────────────────────────────────────┘ │
│                           ▲                                  │
│                           │ HDFS                             │
│  ┌────────────────────────────────────────────────────────┐ │
│  │             SPARK CLUSTER                             │ │
│  │  ┌──────────────┐  ┌──────────┐  ┌──────────┐        │ │
│  │  │ Master       │  │ Worker 1 │  │ Worker 2 │        │ │
│  │  │              │  │          │  │          │        │ │
│  │  └──────────────┘  └──────────┘  └──────────┘        │ │
│  └────────────────────────────────────────────────────────┘ │
│           ▲                                                  │
│           │ Spark                                            │
│  ┌────────────────────────────────────────────────────────┐ │
│  │         JUPYTER NOTEBOOK                              │ │
│  │  (PySpark kernel + Hadoop client)                    │ │
│  └────────────────────────────────────────────────────────┘ │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

### Thành Phần

- **1x Hadoop Master**: NameNode + ResourceManager
- **2x Hadoop Worker**: DataNode + NodeManager
- **1x Spark Master**: Spark Master node
- **2x Spark Worker**: Spark Worker nodes
- **1x Jupyter**: Notebook server với PySpark kernel

### Phiên Bản

- **Hadoop**: 3.3.6
- **Spark**: 3.5.0 (Hadoop 3 compatible)
- **Java**: OpenJDK 11
- **Jupyter**: Latest PySpark
- **Ubuntu**: 22.04

## 🚀 Bắt Đầu Nhanh (Quick Start)

### Yêu Cầu Tiên Quyết

- **Docker Desktop** (hoặc Docker Engine + Docker Compose)
- Ít nhất **8GB RAM** dành cho containers
- **20GB disk space** cho images và volumes
- **Port availability**: 9870, 8088, 8080, 8888 (và các port khác)

### Bước 1: Clone/Setup Project

```bash
cd d:\BIGDATA\Hoang\hadoop-hoang
```

### Bước 2: Khởi Động Cluster

```bash
.\start-cluster.bat
```

### Bước 3: Chờ Services Khởi Động

Script sẽ tự động:
1. Build Docker images
2. Start tất cả containers
3. Chờ services ready
4. Hiển thị URLs

### Bước 4: Truy Cập Web UIs

Mở browser và truy cập:

| Service | URL | Port |
|---------|-----|------|
| Hadoop NameNode | http://localhost:9870 | 9870 |
| YARN ResourceManager | http://localhost:8088 | 8088 |
| Spark Master | http://localhost:8080 | 8080 |
| Spark Worker 1 | http://localhost:8081 | 8081 |
| Spark Worker 2 | http://localhost:8082 | 8082 |
| Jupyter Notebook | http://localhost:8888 | 8888 |

### Bước 5: Dừng Cluster

```bash
.\stop-cluster.bat
```

Hoặc:

```bash
docker-compose down
```

## 📁 Cấu Trúc Thư Mục

```
hadoop-hoang/
├── docker/
│   ├── Dockerfile.hadoop       # Hadoop base image
│   ├── Dockerfile.spark        # Spark base image
│   └── Dockerfile.jupyter      # Jupyter with PySpark
├── config/
│   ├── hadoop/
│   │   ├── core-site.xml       # Hadoop core configuration
│   │   ├── hdfs-site.xml       # HDFS configuration
│   │   └── yarn-site.xml       # YARN configuration
│   └── spark/
│       └── spark-defaults.conf # Spark configuration
├── scripts/
│   ├── init-hadoop.sh          # Initialize Hadoop
│   ├── healthcheck.sh          # Health check script
│   ├── entrypoint-hadoop-master.sh
│   ├── entrypoint-hadoop-worker.sh
│   ├── entrypoint-spark-master.sh
│   └── entrypoint-spark-worker.sh
├── notebooks/
│   ├── 01-Test-Connection.ipynb      # Test HDFS/Spark connection
│   └── 02-WordCount-Example.ipynb    # WordCount example
├── volumes/
│   ├── hadoop_name/            # NameNode persistent storage
│   └── hadoop_data/            # DataNode persistent storage
├── docker-compose.yml          # Main orchestration file
├── start-cluster.bat           # Startup script (Windows)
├── start-cluster.sh            # Startup script (Linux/Mac)
├── stop-cluster.bat            # Stop script (Windows)
├── stop-cluster.sh             # Stop script (Linux/Mac)
└── README.md                   # This file
```

## 🔧 Cấu Hình

### core-site.xml
Cấu hình HDFS NameNode và proxy users

```xml
<property>
    <name>fs.defaultFS</name>
    <value>hdfs://hadoop-master:9000</value>
</property>
```

### hdfs-site.xml
Cấu hình HDFS DataNode và replication

```xml
<property>
    <name>dfs.replication</name>
    <value>2</value>
</property>
```

### yarn-site.xml
Cấu hình YARN ResourceManager

```xml
<property>
    <name>yarn.resourcemanager.hostname</name>
    <value>hadoop-master</value>
</property>
```

### spark-defaults.conf
Cấu hình Spark cluster

```conf
spark.master                        spark://spark-master:7077
spark.hadoop.fs.defaultFS          hdfs://hadoop-master:9000
spark.executor.memory               1g
spark.executor.cores                2
```

## 💻 Các Lệnh Hữu Ích

### Quản Lý Containers

```bash
# View logs
docker-compose logs -f

# View logs of specific service
docker-compose logs -f hadoop-master

# SSH into container
docker exec -it hadoop-master bash

# View running containers
docker-compose ps

# Remove all containers (and networks)
docker-compose down
```

### HDFS Commands

```bash
# SSH vào Hadoop Master
docker exec -it hadoop-master bash

# List HDFS files
hdfs dfs -ls /

# Create directory
hdfs dfs -mkdir -p /user/hadoop/test

# Upload local file to HDFS
hdfs dfs -put /local/path/file.txt /user/hadoop/test/

# Download file from HDFS
hdfs dfs -get /user/hadoop/test/file.txt /local/path/

# Remove file from HDFS
hdfs dfs -rm /user/hadoop/test/file.txt

# View file content
hdfs dfs -cat /user/hadoop/test/file.txt

# Check HDFS status
hdfs dfsadmin -report
```

### Spark Commands

```bash
# SSH vào Spark Master
docker exec -it spark-master bash

# Submit Spark job
spark-submit --master spark://spark-master:7077 \
             --executor-memory 1g \
             --executor-cores 2 \
             your_script.py

# Run Spark shell
spark-shell --master spark://spark-master:7077

# Run PySpark shell
pyspark --master spark://spark-master:7077
```

### Jupyter

Truy cập Jupyter tại http://localhost:8888

Để lấy token:

```bash
docker logs jupyter-notebook | grep "token="
```

## 🧪 Test Connection & Functionality

### Test 1: HDFS Connectivity

```bash
docker exec hadoop-master hdfs dfs -ls /
```

Expected output:
```
Found X items
drwxr-xr-x  - hadoop supergroup    ...  /spark-logs
drwxr-xr-x  - hadoop supergroup    ...  /tmp
drwxr-xr-x  - hadoop supergroup    ...  /user
```

### Test 2: Yarn Status

```bash
docker exec hadoop-master yarn node -list
```

### Test 3: Spark Cluster Status

Truy cập http://localhost:8080 để xem Spark Master UI

Hoặc:

```bash
docker exec spark-master curl -s http://localhost:8080 | grep -i worker
```

### Test 4: PySpark trong Jupyter

1. Truy cập http://localhost:8888
2. Mở notebook `01-Test-Connection.ipynb`
3. Run cells lần lượt
4. Kiểm tra output

## 📚 Ví Dụ PySpark

### Example 1: Tạo DataFrame

```python
from pyspark.sql import SparkSession

spark = SparkSession.builder \
    .appName("Test") \
    .master("spark://spark-master:7077") \
    .config("spark.hadoop.fs.defaultFS", "hdfs://hadoop-master:9000") \
    .getOrCreate()

data = [("Alice", 25), ("Bob", 30)]
columns = ["Name", "Age"]
df = spark.createDataFrame(data, schema=columns)
df.show()
```

### Example 2: Read từ HDFS

```python
df = spark.read.parquet("hdfs://hadoop-master:9000/path/to/data")
df.show()
```

### Example 3: Save to HDFS

```python
df.write.mode("overwrite").parquet("hdfs://hadoop-master:9000/output")
```

### Example 4: SQL Operations

```python
df.createOrReplaceTempView("people")
spark.sql("SELECT * FROM people WHERE Age > 28").show()
```

### Example 5: RDD Operations

```python
sc = spark.sparkContext
rdd = sc.parallelize([1, 2, 3, 4, 5])
result = rdd.map(lambda x: x * 2).collect()
print(result)  # [2, 4, 6, 8, 10]
```

## 🛠️ Troubleshooting

### Issue: Containers không start

**Solution**: Kiểm tra Docker resources
```bash
docker stats
```

Đảm bảo có ít nhất 8GB RAM available

### Issue: HDFS NameNode không format

**Solution**: Xóa persistent volumes
```bash
docker-compose down -v
```

### Issue: Spark workers không kết nối

**Solution**: Kiểm tra logs
```bash
docker-compose logs spark-master
docker-compose logs spark-worker-1
```

### Issue: Jupyter không kết nối với Spark

**Solution**: Chạy từng cell từ từ, cho phép Spark khởi động

### Issue: Port conflicts

Nếu ports đã được sử dụng, chỉnh sửa `docker-compose.yml`:

```yaml
ports:
  - "19870:9870"  # Changed from 9870:9870
```

### Issue: Out of memory

Giảm executor memory trong `spark-defaults.conf`:
```conf
spark.executor.memory                512m
```

## 📊 Scaling

### Thêm Hadoop Worker

1. Tạo mục mới trong `docker-compose.yml` dựa trên `hadoop-worker-1`
2. Thay đổi hostname, container name
3. Đổi port mapping nếu cần
4. Chạy: `docker-compose up -d hadoop-worker-3`

### Thêm Spark Worker

Tương tự như Hadoop Worker, copy service `spark-worker-1` và đổi tên

## 🔐 Security Notes

Cấu hình hiện tại:
- ✅ SSH key-based authentication
- ⚠️ HDFS permissions disabled (cho development)
- ⚠️ Không có authentication trên Spark
- ⚠️ All users trusted (hadoop.proxyuser.* = *)

**Cho production**: Enable security, kerberos, authentication

## 📖 Tài Liệu Tham Khảo

- [Hadoop Official Docs](https://hadoop.apache.org/docs/r3.3.6/)
- [Spark Official Docs](https://spark.apache.org/docs/3.5.0/)
- [Docker Compose Docs](https://docs.docker.com/compose/)
- [Jupyter Documentation](https://jupyter.org/)

## 🤝 Hỗ Trợ

Nếu gặp vấn đề:

1. Kiểm tra logs: `docker-compose logs`
2. Kiểm tra container health: `docker ps`
3. SSH vào container: `docker exec -it <container-name> bash`
4. Kiểm tra web UIs trực tiếp

## 📝 Notes

- Cluster sử dụng bridge network tên là `hadoop-spark-network`
- Persistent volumes được lưu trong `volumes/` directory
- Tất cả services có health checks
- Services khởi động với đúng thứ tự nhờ `depends_on`
- SSH không password được enable cho các nodes

## 🎯 Next Steps

1. Chạy `start-cluster.bat` hoặc `start-cluster.sh`
2. Mở http://localhost:9870 để kiểm tra Hadoop
3. Mở http://localhost:8080 để kiểm tra Spark
4. Mở http://localhost:8888 để mở Jupyter
5. Chạy các example notebooks
6. Tạo jobs của bạn

---

**Created**: 2026-04-01  
**Version**: 1.0  
**Compatibility**: Docker Desktop, Docker Engine 20.10+, Docker Compose 2.0+
