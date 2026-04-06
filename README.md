# 🐘 Hadoop-Spark Cluster Infrastructure

> Một hệ thống Big Data phân tán hoàn chỉnh chạy trên Docker Compose, sẵn sàng cho các bài tập Big Data, xử lý dữ liệu lớn, và phân tích dữ liệu.

**Tác giả**: SIUTRITUE  
**Repository**: https://github.com/SIUTRITUE/Hadoop  
**Cập nhật**: 2026-04-06

## 📋 Kiến Trúc Hệ Thống

```
┌──────────────────────────────────────────────────────────────┐
│              Docker Compose Network (hadoop-net)             │
├──────────────────────────────────────────────────────────────┤
│                                                              │
│   HADOOP CLUSTER (HDFS + YARN)                             │
│   ┌──────────────┐      ┌──────────┐      ┌──────────┐    │
│   │ hadoop-master│      │hadoop-w1 │      │hadoop-w2 │    │
│   │ :9000 HDFS   │ ◄───►│:9000 HDFS│ ◄───►│:9000 HDFS│    │
│   │ :8088 YARN   │      │:8042 YARN│      │:8042 YARN│    │
│   │ :50070 Web   │      │:50075 Web│      │:50075 Web│    │
│   └──────────────┘      └──────────┘      └──────────┘    │
│         ▲ ▲ ▲                                               │
│         │ │ │                                               │
│   SPARK CLUSTER (Master + Workers)                        │
│   ┌──────────────┐      ┌──────────┐      ┌──────────┐    │
│   │spark-master  │      │spark-w1  │      │spark-w2  │    │
│   │ :7077 Submit │ ◄───►│:7077 Slot│ ◄───►│:7077 Slot│    │
│   │ :18080 UI    │      │:8081 UI  │      │:8081 UI  │    │
│   └──────────────┘      └──────────┘      └──────────┘    │
│         ▲                                                   │
│         │ PySpark Commands                                 │
│   ┌──────────────┐      ┌──────────────┐                  │
│   │   jupyter    │      │  streamlit   │                  │
│   │ :8888 Notebook│      │ :8501 Dashboard                │
│   │ • Lab work   │      │ • Visualization                │
│   │ • Analysis   │      │ • Results view                 │
│   └──────────────┘      └──────────────┘                  │
│                                                              │
│   SHARED STORAGE (Volumes)                                 │
│   ├── /volumes/hadoop_name     (HDFS metadata)             │
│   ├── /volumes/hadoop_data     (DataNode storage)          │
│   └── /volumes/spark_data      (Temp files)                │
│                                                              │
└──────────────────────────────────────────────────────────────┘
```

### Services (7 containers)

| Container | Role | Key Ports | Purpose |
|-----------|------|-----------|---------|
| `hadoop-master` | NameNode + YARN RM | 9000, 8088, 50070 | Cluster coordination |
| `hadoop-worker1` | DataNode + YARN NM | 9000, 8042, 50075 | Data storage |
| `hadoop-worker2` | DataNode + YARN NM | 9000, 8042, 50075 | Data storage |
| `spark-master` | Spark Master | 7077, 18080 | Job submission & scheduling |
| `spark-worker1` | Spark Executor | 7077, 8081 | Task execution |
| `spark-worker2` | Spark Executor | 7077, 8081 | Task execution |
| `jupyter` | Notebook Server | 8888 | Interactive development |
| `streamlit-app` | Dashboard | 8501 | Results visualization |

## 🎯 Mục Đích

Hệ thống này được thiết kế để:

- ✅ **Học tập & Thực hành**: Hiểu cách hoạt động của Hadoop, Spark, và Big Data
- ✅ **Phát triển ứng dụng**: Xây dựng các jobs Spark, MapReduce trên môi trường thực
- ✅ **Xử lý dữ liệu**: Phân tích dữ liệu lớn bằng Spark SQL, PySpark
- ✅ **Thực hiện bài tập**: Hoàn thành các assignment về Big Data
- ✅ **Prototyping**: Test ideas trước khi deploy lên production

**Không cần setup phức tạp** - một lệnh là cluster chạy!

## 🛠️ Công Nghệ Sử Dụng

| Thành Phần | Phiên Bản | Vai Trò |
|-----------|----------|--------|
| **Hadoop** | 3.3.6 | Distributed filesystem (HDFS) & Resource management (YARN) |
| **Spark** | 3.5.0 | Distributed computing framework |
| **Java** | OpenJDK 11 | Runtime environment |
| **Jupyter** | Latest | Interactive notebook environment |
| **Docker** | 20.10+ | Containerization |
| **Docker Compose** | 2.0+ | Orchestration |

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
│   ├── 02-WordCount-Example.ipynb    # WordCount MapReduce example
│   └── 03-Data-Processing-Pipeline.ipynb # Spark data processing
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

### Sử Dụng Cho Các Bài Toán Khác

**Hệ thống này không giới hạn cho một bài tập!** Bạn có thể sử dụng nó cho bất kỳ Big Data project nào:

#### Ví dụ 1: Log Analysis

```python
# Read web server logs from HDFS
logs = spark.read.text("hdfs://hadoop-master:9000/logs/*.log")
errors = logs.filter(logs.value.contains("ERROR"))
errors.count()
```

#### Ví dụ 2: Machine Learning

```python
from pyspark.ml.classification import LogisticRegression

# Load data từ HDFS
df = spark.read.parquet("hdfs://hadoop-master:9000/ml-data")

# Train model
lr = LogisticRegression(maxIter=10)
model = lr.fit(df)

# Save model
model.save("hdfs://hadoop-master:9000/models/lr-model")
```

#### Ví dụ 3: Data Pipeline

```python
# ETL job
data = spark.read.csv("hdfs://hadoop-master:9000/raw/*.csv", header=True)
cleaned = data.dropna().filter(data.age > 18)
cleaned.write.mode("overwrite").parquet("hdfs://hadoop-master:9000/processed/")
```

#### Ví dụ 4: SQL Analysis (Hive)

```python
# Create table from HDFS data
df = spark.read.csv("hdfs://hadoop-master:9000/sales.csv", header=True)
df.createOrReplaceTempView("sales")

# Query
results = spark.sql("""
    SELECT category, SUM(amount) as total
    FROM sales
    GROUP BY category
    ORDER BY total DESC
""")
results.show()
```

#### Ví dụ 5: Stream Processing

```python
# Read streaming data
stream = spark.readStream.csv("hdfs://hadoop-master:9000/stream", header=True)
query = stream.groupBy("user").count().writeStream.format("console").start()
query.awaitTermination()
```

**Các use cases phổ biến:**
- ✅ Word Count, Text Analysis
- ✅ Data Cleaning & Preprocessing
- ✅ Statistical Analysis
- ✅ Machine Learning (MLlib)
- ✅ SQL Analytics (Spark SQL)
- ✅ Graph Processing (GraphX)
- ✅ Streaming Data Processing
- ✅ ETL Jobs
- ✅ Batch Processing
- ✅ Log Analysis & Monitoring

**Bạn có thể:**
1. Upload datasets của riêng bạn vào HDFS
2. Viết Spark/MapReduce jobs
3. Lưu kết quả vào HDFS
4. Visualize kết quả bằng Jupyter hoặc Streamlit
5. Commit code lên GitHub

Hệ thống hoàn toàn agnostic - nó không biết về LAB 5 hay bất kỳ bài tập cụ thể nào.

---

## � Streamlit Dashboard

Hệ thống cung cấp **Streamlit Dashboard** để trực quan hóa kết quả từ Spark jobs.

### Khởi Động Dashboard

Dashboard tự động chạy khi bạn chạy `start-cluster.bat`:

```bash
# Truy cập tại:
http://localhost:8501
```

### Dashboard Features

Dashboard có 4 tabs chính:

#### Tab 1: 📈 Data Analysis
- Hiển thị dữ liệu từ HDFS
- Visualize distributions
- Statistical summaries
- Data preview

#### Tab 2: 🎯 Query Results
- Hiển thị kết quả từ Spark SQL queries
- Aggregations & Group by
- Top N results
- Charts & graphs

#### Tab 3: 🤖 Model Metrics
- Machine Learning model performance
- Accuracy, Precision, Recall, F1-Score
- Confusion Matrix
- Feature Importance

#### Tab 4: ℹ️ Project Info
- Hệ thống information
- Kiến trúc chi tiết
- Cluster status
- Configuration

### Sử Dụng Dashboard

#### Cách 1: Tự động (Recommended)
1. Run `start-cluster.bat`
2. Dashboard tự động chạy trên port 8501
3. Mở http://localhost:8501

#### Cách 2: Manual
```bash
# SSH vào streamlit container
docker exec -it streamlit-app bash

# Hoặc chạy directly
streamlit run /app/app.py --server.port=8501 --server.address=0.0.0.0
```

### Tùy Chỉnh Dashboard

Dashboard code nằm tại: `streamlit/app.py`

**Cấu trúc:**
```python
# Load data from HDFS
def load_data_hdfs():
    # Read CSV từ HDFS
    
# Load results from HDFS
def load_results_hdfs():
    # Read query results từ HDFS

# Create visualizations
st.bar_chart(data)
st.line_chart(data)
st.plotly_chart(fig)
```

**Thêm tab mới:**
```python
with st.tabs(["Tab 1", "Tab 2", "New Tab"]):
    with st.tabs(["New Tab"]):
        # Your visualization code here
        st.write(data)
```

**Thêm metric card:**
```python
col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Accuracy", "95%", "+5%")
with col2:
    st.metric("Precision", "92%", "+2%")
with col3:
    st.metric("Recall", "90%", "-1%")
```

### Kết Nối Dashboard với Spark Jobs

**Luồng dữ liệu:**
1. **Data Input** → Upload CSV vào HDFS
2. **Process** → Run Spark job từ Jupyter/Script
3. **Save Results** → Ghi output vào HDFS (CSV/Parquet)
4. **Visualize** → Dashboard đọc từ HDFS và display

**Ví dụ:**

```python
# Jupyter: Xử lý dữ liệu
df = spark.read.csv("hdfs://hadoop-master:9000/input.csv", header=True)
result = df.groupBy("category").agg({"amount": "sum"})
result.write.mode("overwrite").csv("hdfs://hadoop-master:9000/results/top_categories")

# Streamlit: Hiển thị kết quả
df_results = spark.read.csv("hdfs://hadoop-master:9000/results/top_categories")
st.bar_chart(df_results)
```

### Dashboard Architecture

```
┌─────────────────────────────────────┐
│      Jupyter Notebook               │
│  (Data Processing & Analysis)       │
│                                     │
│  • Read from HDFS                   │
│  • Process with Spark               │
│  • Save results to HDFS             │
└──────────────┬──────────────────────┘
               │ (HDFS Path)
               ▼
┌─────────────────────────────────────┐
│      HDFS Storage                   │
│  /results/top_categories            │
│  /results/model_metrics             │
│  /results/predictions               │
└──────────────┬──────────────────────┘
               │ (Read)
               ▼
┌─────────────────────────────────────┐
│      Streamlit Dashboard            │
│      (Visualization Layer)          │
│                                     │
│  • Load data from HDFS              │
│  • Display charts/tables            │
│  • Show metrics & KPIs              │
│  • Export/Download results          │
└─────────────────────────────────────┘
               │
               ▼
         (Port 8501)
         Web Browser
```

### Best Practices

1. **Cache HDFS reads**: Streamlit caches automatically
   ```python
   @st.cache_data
   def load_data():
       return spark.read.csv(...)
   ```

2. **Handle errors gracefully**:
   ```python
   try:
       df = spark.read.csv(hdfs_path)
   except:
       st.error("Cannot read from HDFS")
   ```

3. **Update dashboard periodically**:
   ```python
   st.set_page_config(initial_sidebar_state="expanded")
   if st.button("Refresh"):
       st.cache_data.clear()
       st.rerun()
   ```

4. **Optimize performance**:
   - Collect dữ liệu từ Spark vào Pandas
   - Giới hạn số rows hiển thị
   - Sử dụng sampling cho large datasets

---

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
