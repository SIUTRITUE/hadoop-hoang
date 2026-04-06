# 🐘 Hadoop-Spark Big Data Cluster# 🐘 Hadoop-Spark Big Data Cluster# 🐘 Hadoop-Spark Cluster Infrastructure



Hệ thống Hadoop-Spark phân tán chạy trên Docker Compose. Sẵn sàng cho các bài tập Big Data, xử lý dữ liệu lớn, và phân tích dữ liệu.



**Repository**: https://github.com/SIUTRITUE/hadoop-hoangHệ thống Hadoop-Spark phân tán chạy trên Docker Compose. Sẵn sàng cho các bài tập Big Data, xử lý dữ liệu lớn, và phân tích dữ liệu.> Một hệ thống Big Data phân tán hoàn chỉnh chạy trên Docker Compose, sẵn sàng cho các bài tập Big Data, xử lý dữ liệu lớn, và phân tích dữ liệu.



---



## 📋 Kiến Trúc**Repository**: https://github.com/SIUTRITUE/Hadoop**Tác giả**: SIUTRITUE  



### Services & Components**Repository**: https://github.com/SIUTRITUE/Hadoop  



| Cluster | Container | Role | Port |---**Cập nhật**: 2026-04-06

|---------|-----------|------|------|

| **Hadoop** | hadoop-master | NameNode + YARN RM | 9870, 8088 |

| | hadoop-worker-1 | DataNode + NodeManager | 9864, 8042 |

| | hadoop-worker-2 | DataNode + NodeManager | 9865, 8043 |## 📋 Kiến Trúc## 📋 Kiến Trúc Hệ Thống

| **Spark** | spark-master | Master + Driver | 8080, 7077 |

| | spark-worker-1 | Executor | 8081, 7078 |

| | spark-worker-2 | Executor | 8082, 7079 |

| **Tools** | jupyter | Notebook Server | 8888 |``````

| | streamlit | Dashboard | 8501 |

Docker Network┌──────────────────────────────────────────────────────────────┐

**Technology Stack:**

- Hadoop 3.3.6 (HDFS + YARN)├── Hadoop Cluster│              Docker Compose Network (hadoop-net)             │

- Spark 3.5.0

- Java OpenJDK 11│   ├── hadoop-master (NameNode + YARN ResourceManager)├──────────────────────────────────────────────────────────────┤

- Python 3.10

- Docker & Docker Compose│   ├── hadoop-worker-1 (DataNode + NodeManager)│                                                              │



---│   └── hadoop-worker-2 (DataNode + NodeManager)│   HADOOP CLUSTER (HDFS + YARN)                             │



## 🚀 Quick Start││   ┌──────────────┐      ┌──────────┐      ┌──────────┐    │



### Requirements├── Spark Cluster│   │ hadoop-master│      │hadoop-w1 │      │hadoop-w2 │    │

- Docker Desktop (or Docker Engine + Compose)

- 8GB+ RAM for containers│   ├── spark-master (Master + Driver)│   │ :9000 HDFS   │ ◄───►│:9000 HDFS│ ◄───►│:9000 HDFS│    │

- 20GB+ disk space

│   ├── spark-worker-1 (Executor)│   │ :8088 YARN   │      │:8042 YARN│      │:8042 YARN│    │

### Step 1: Start Cluster

│   └── spark-worker-2 (Executor)│   │ :50070 Web   │      │:50075 Web│      │:50075 Web│    │

```bash

cd d:\BIGDATA\Hoang\hadoop-hoang││   └──────────────┘      └──────────┘      └──────────┘    │

.\start-cluster.bat

```├── Jupyter Notebook (PySpark interactive development)│         ▲ ▲ ▲                                               │



On Linux/Mac:└── Streamlit Dashboard (Results visualization)│         │ │ │                                               │

```bash

./start-cluster.sh```│   SPARK CLUSTER (Master + Workers)                        │

```

│   ┌──────────────┐      ┌──────────┐      ┌──────────┐    │

### Step 2: Wait for Services (~2-3 minutes)

**Công nghệ:**│   │spark-master  │      │spark-w1  │      │spark-w2  │    │

The script will automatically build images, start containers, and perform health checks.

- Hadoop 3.3.6 (HDFS + YARN)│   │ :7077 Submit │ ◄───►│:7077 Slot│ ◄───►│:7077 Slot│    │

### Step 3: Access Web UIs

- Spark 3.5.0│   │ :18080 UI    │      │:8081 UI  │      │:8081 UI  │    │

| Service | URL | Port |

|---------|-----|------|- Java OpenJDK 11│   └──────────────┘      └──────────┘      └──────────┘    │

| **Hadoop NameNode** | http://localhost:9870 | 9870 |

| **YARN ResourceManager** | http://localhost:8088 | 8088 |- Python 3.10│         ▲                                                   │

| **Spark Master** | http://localhost:8080 | 8080 |

| **Spark Worker 1** | http://localhost:8081 | 8081 |- Docker & Docker Compose│         │ PySpark Commands                                 │

| **Spark Worker 2** | http://localhost:8082 | 8082 |

| **Jupyter Notebook** | http://localhost:8888 | 8888 |│   ┌──────────────┐      ┌──────────────┐                  │

| **Streamlit Dashboard** | http://localhost:8501 | 8501 |

---│   │   jupyter    │      │  streamlit   │                  │

### Step 4: Stop Cluster

│   │ :8888 Notebook│      │ :8501 Dashboard                │

```bash

.\stop-cluster.bat## 🚀 Khởi Động Nhanh│   │ • Lab work   │      │ • Visualization                │

```

│   │ • Analysis   │      │ • Results view                 │

Or:

```bash### Yêu Cầu│   └──────────────┘      └──────────────┘                  │

docker-compose down

```- Docker Desktop (hoặc Docker Engine + Compose)│                                                              │



---- 8GB+ RAM cho containers│   SHARED STORAGE (Volumes)                                 │



## 💻 Useful Commands- 20GB+ disk space│   ├── /volumes/hadoop_name     (HDFS metadata)             │



### Docker Management│   ├── /volumes/hadoop_data     (DataNode storage)          │



```bash### Bước 1: Khởi Động Cluster│   └── /volumes/spark_data      (Temp files)                │

# View running containers

docker-compose ps│                                                              │



# View all logs```bash└──────────────────────────────────────────────────────────────┘

docker-compose logs -f

cd d:\BIGDATA\Hoang\hadoop-hoang```

# View specific service logs

docker-compose logs -f hadoop-master.\start-cluster.bat



# SSH into container```### Services (7 containers)

docker exec -it hadoop-master bash



# Restart services

docker-compose restartHoặc trên Linux/Mac:| Container | Role | Key Ports | Purpose |

```

```bash|-----------|------|-----------|---------|

### HDFS Commands

./start-cluster.sh| `hadoop-master` | NameNode + YARN RM | 9000, 8088, 50070 | Cluster coordination |

```bash

# SSH to Hadoop Master```| `hadoop-worker1` | DataNode + YARN NM | 9000, 8042, 50075 | Data storage |

docker exec -it hadoop-master bash

| `hadoop-worker2` | DataNode + YARN NM | 9000, 8042, 50075 | Data storage |

# List files

hdfs dfs -ls /### Bước 2: Chờ Services Khởi Động (~2-3 phút)| `spark-master` | Spark Master | 7077, 18080 | Job submission & scheduling |



# Create directory| `spark-worker1` | Spark Executor | 7077, 8081 | Task execution |

hdfs dfs -mkdir -p /user/hadoop/test

Script sẽ tự động build images, start containers, và chờ services ready.| `spark-worker2` | Spark Executor | 7077, 8081 | Task execution |

# Upload file

hdfs dfs -put /path/to/file.txt /user/hadoop/test/| `jupyter` | Notebook Server | 8888 | Interactive development |



# Download file### Bước 3: Truy Cập Web UIs| `streamlit-app` | Dashboard | 8501 | Results visualization |

hdfs dfs -get /user/hadoop/test/file.txt /path/to/



# View file content

hdfs dfs -cat /user/hadoop/test/file.txt| Service | URL | Cổng |## 🎯 Mục Đích



# Check HDFS status|---------|-----|------|

hdfs dfsadmin -report

```| **Hadoop NameNode** | http://localhost:9870 | 9870 |Hệ thống này được thiết kế để:



### Spark Commands| **YARN ResourceManager** | http://localhost:8088 | 8088 |



```bash| **Spark Master** | http://localhost:8080 | 8080 |- ✅ **Học tập & Thực hành**: Hiểu cách hoạt động của Hadoop, Spark, và Big Data

# SSH to Spark Master

docker exec -it spark-master bash| **Spark Worker 1** | http://localhost:8081 | 8081 |- ✅ **Phát triển ứng dụng**: Xây dựng các jobs Spark, MapReduce trên môi trường thực



# Submit job| **Spark Worker 2** | http://localhost:8082 | 8082 |- ✅ **Xử lý dữ liệu**: Phân tích dữ liệu lớn bằng Spark SQL, PySpark

spark-submit --master spark://spark-master:7077 \

             --executor-memory 1g \| **Jupyter Notebook** | http://localhost:8888 | 8888 |- ✅ **Thực hiện bài tập**: Hoàn thành các assignment về Big Data

             your_script.py

| **Streamlit Dashboard** | http://localhost:8501 | 8501 |- ✅ **Prototyping**: Test ideas trước khi deploy lên production

# Spark shell

spark-shell --master spark://spark-master:7077



# PySpark shell### Bước 4: Dừng Cluster**Không cần setup phức tạp** - một lệnh là cluster chạy!

pyspark --master spark://spark-master:7077

```



### Jupyter```bash## 🛠️ Công Nghệ Sử Dụng



Access: http://localhost:8888.\stop-cluster.bat



Get token:```| Thành Phần | Phiên Bản | Vai Trò |

```bash

docker logs jupyter-notebook | grep "token="|-----------|----------|--------|

```

Hoặc:| **Hadoop** | 3.3.6 | Distributed filesystem (HDFS) & Resource management (YARN) |

---

```bash| **Spark** | 3.5.0 | Distributed computing framework |

## 🧪 Test Cluster

docker-compose down| **Java** | OpenJDK 11 | Runtime environment |

### Test 1: HDFS Connectivity

```| **Jupyter** | Latest | Interactive notebook environment |

```bash

docker exec hadoop-master hdfs dfs -ls /| **Docker** | 20.10+ | Containerization |

```

---| **Docker Compose** | 2.0+ | Orchestration |

Expected: List of directories



### Test 2: YARN Nodes

## 💻 Các Lệnh Hữu Ích## 🚀 Bắt Đầu Nhanh (Quick Start)

```bash

docker exec hadoop-master yarn node -list

```

### Docker Management### Yêu Cầu Tiên Quyết

Expected: 2 DataNodes listed



### Test 3: Spark Master

```bash- **Docker Desktop** (hoặc Docker Engine + Docker Compose)

Visit http://localhost:8080

# View running containers- Ít nhất **8GB RAM** dành cho containers

Expected: Spark Master UI with 2 workers

docker-compose ps- **20GB disk space** cho images và volumes

### Test 4: PySpark in Jupyter

- **Port availability**: 9870, 8088, 8080, 8888 (và các port khác)

1. Open http://localhost:8888

2. Create new Python notebook# View logs (all services)

3. Run:

docker-compose logs -f### Bước 1: Clone/Setup Project

```python

from pyspark.sql import SparkSession



spark = SparkSession.builder \# View logs of specific service```bash

    .appName("Test") \

    .master("spark://spark-master:7077") \docker-compose logs -f hadoop-mastercd d:\BIGDATA\Hoang\hadoop-hoang

    .config("spark.hadoop.fs.defaultFS", "hdfs://hadoop-master:9000") \

    .getOrCreate()```



# Create DataFrame# SSH into container

data = [("Alice", 25), ("Bob", 30), ("Charlie", 35)]

df = spark.createDataFrame(data, ["Name", "Age"])docker exec -it hadoop-master bash### Bước 2: Khởi Động Cluster

df.show()

```



Expected: DataFrame displayed with 3 rows# Stop/restart services```bash



---docker-compose stop.\start-cluster.bat



## 📊 Streamlit Dashboarddocker-compose restart```



Dashboard automatically runs on port 8501.```



**Access**: http://localhost:8501### Bước 3: Chờ Services Khởi Động



**Features:**### HDFS Commands

- Tab 1: Data Analysis (from HDFS)

- Tab 2: Query Results (Spark SQL results)Script sẽ tự động:

- Tab 3: Model Metrics (ML performance)

- Tab 4: Project Info```bash1. Build Docker images



Edit `streamlit/app.py` to customize.# SSH vào Hadoop Master2. Start tất cả containers



---docker exec -it hadoop-master bash3. Chờ services ready



## 📁 Directory Structure4. Hiển thị URLs



```# List files

hadoop-hoang/

├── docker/                 # Docker imageshdfs dfs -ls /### Bước 4: Truy Cập Web UIs

│   ├── Dockerfile.hadoop

│   ├── Dockerfile.spark

│   ├── Dockerfile.jupyter

│   └── Dockerfile.streamlit# Create directoryMở browser và truy cập:

├── config/                 # Configuration files

│   ├── hadoop/hdfs dfs -mkdir -p /user/hadoop/test

│   │   ├── core-site.xml

│   │   ├── hdfs-site.xml| Service | URL | Port |

│   │   └── yarn-site.xml

│   └── spark/# Upload file|---------|-----|------|

│       └── spark-defaults.conf

├── scripts/                # Startup scriptshdfs dfs -put /path/to/file.txt /user/hadoop/test/| Hadoop NameNode | http://localhost:9870 | 9870 |

├── notebooks/              # Jupyter notebooks

├── streamlit/              # Dashboard| YARN ResourceManager | http://localhost:8088 | 8088 |

│   └── app.py

├── volumes/                # Persistent storage# Download file| Spark Master | http://localhost:8080 | 8080 |

├── docker-compose.yml

├── start-cluster.bathdfs dfs -get /user/hadoop/test/file.txt /path/to/| Spark Worker 1 | http://localhost:8081 | 8081 |

├── stop-cluster.bat

└── README.md| Spark Worker 2 | http://localhost:8082 | 8082 |

```

# View file| Jupyter Notebook | http://localhost:8888 | 8888 |

---

hdfs dfs -cat /user/hadoop/test/file.txt

## 📚 Usage Examples

### Bước 5: Dừng Cluster

### Example 1: Read CSV from HDFS

# Check HDFS status

```python

df = spark.read.csv("hdfs://hadoop-master:9000/data.csv", header=True)hdfs dfsadmin -report```bash

df.show()

``````.\stop-cluster.bat



### Example 2: SQL Query```



```python### Spark Commands

df.createOrReplaceTempView("data")

results = spark.sql("SELECT * FROM data WHERE age > 25")Hoặc:

results.show()

``````bash



### Example 3: Save Results to HDFS# SSH vào Spark Master```bash



```pythondocker exec -it spark-master bashdocker-compose down

df.write.mode("overwrite").csv("hdfs://hadoop-master:9000/output")

``````



### Example 4: Machine Learning# Submit job



```pythonspark-submit --master spark://spark-master:7077 \## 📁 Cấu Trúc Thư Mục

from pyspark.ml.classification import LogisticRegression

             --executor-memory 1g \

lr = LogisticRegression(maxIter=10)

model = lr.fit(df)             your_script.py```

model.save("hdfs://hadoop-master:9000/models/lr")

```hadoop-hoang/



---# Spark shell├── docker/



## 🔧 Configurationspark-shell --master spark://spark-master:7077│   ├── Dockerfile.hadoop       # Hadoop base image



### Adjust Memory│   ├── Dockerfile.spark        # Spark base image



Edit `config/spark/spark-defaults.conf`:# PySpark shell│   └── Dockerfile.jupyter      # Jupyter with PySpark



```confpyspark --master spark://spark-master:7077├── config/

spark.executor.memory    1g      # Change to 512m if low RAM

spark.executor.cores     2```│   ├── hadoop/

```

│   │   ├── core-site.xml       # Hadoop core configuration

### Add Hadoop Worker

### Jupyter│   │   ├── hdfs-site.xml       # HDFS configuration

1. Copy `hadoop-worker-1` service in `docker-compose.yml`

2. Rename to `hadoop-worker-3` and update ports│   │   └── yarn-site.xml       # YARN configuration

3. Run: `docker-compose up -d hadoop-worker-3`

Truy cập: http://localhost:8888│   └── spark/

---

│       └── spark-defaults.conf # Spark configuration

## ❌ Troubleshooting

Lấy token:├── scripts/

### Containers not starting

```bash│   ├── init-hadoop.sh          # Initialize Hadoop

```bash

docker stats  # Check available resourcesdocker logs jupyter-notebook | grep "token="│   ├── healthcheck.sh          # Health check script

docker-compose logs  # Check error logs

``````│   ├── entrypoint-hadoop-master.sh



Ensure 8GB+ RAM available.│   ├── entrypoint-hadoop-worker.sh



### HDFS format error---│   ├── entrypoint-spark-master.sh



```bash│   └── entrypoint-spark-worker.sh

docker-compose down -v  # Remove volumes

```## 🧪 Test Cluster├── notebooks/



### Spark workers not connecting│   ├── 01-Test-Connection.ipynb      # Test HDFS/Spark connection



```bash### Test 1: HDFS│   ├── 02-WordCount-Example.ipynb    # WordCount MapReduce example

docker-compose logs spark-master

docker-compose logs spark-worker-1│   └── 03-Data-Processing-Pipeline.ipynb # Spark data processing

```

```bash├── volumes/

### Jupyter can't connect to Spark

docker exec hadoop-master hdfs dfs -ls /│   ├── hadoop_name/            # NameNode persistent storage

- Run cells one by one

- Wait for Spark to start (30-60 seconds)```│   └── hadoop_data/            # DataNode persistent storage



### Port conflict├── docker-compose.yml          # Main orchestration file



Edit `docker-compose.yml`:Expected: Danh sách thư mục├── start-cluster.bat           # Startup script (Windows)



```yaml├── start-cluster.sh            # Startup script (Linux/Mac)

ports:

  - "19870:9870"  # Map to different port### Test 2: YARN├── stop-cluster.bat            # Stop script (Windows)

```

├── stop-cluster.sh             # Stop script (Linux/Mac)

---

```bash└── README.md                   # This file

## 📖 References

docker exec hadoop-master yarn node -list```

- [Hadoop Documentation](https://hadoop.apache.org/docs/r3.3.6/)

- [Spark Documentation](https://spark.apache.org/docs/3.5.0/)```

- [Docker Compose](https://docs.docker.com/compose/)

## 🔧 Cấu Hình

---

Expected: Danh sách nodes (2 DataNodes)

## 📝 Notes

### core-site.xml

- HDFS NameNode RPC: `hdfs://hadoop-master:9000`

- Spark Master: `spark://spark-master:7077`### Test 3: SparkCấu hình HDFS NameNode và proxy users

- Network: `hadoop-spark-network`

- Persistent volumes in `volumes/` directory

- All services have health checks

Truy cập http://localhost:8080```xml

---

<property>

**Version**: 1.0  

**Last Updated**: 2026-04-06  Expected: Spark Master UI với 2 workers    <name>fs.defaultFS</name>

**License**: MIT

    <value>hdfs://hadoop-master:9000</value>

### Test 4: PySpark trong Jupyter</property>

```

1. Mở http://localhost:8888

2. Create new Python notebook### hdfs-site.xml

3. Chạy:Cấu hình HDFS DataNode và replication

```python

from pyspark.sql import SparkSession```xml

<property>

spark = SparkSession.builder \    <name>dfs.replication</name>

    .appName("Test") \    <value>2</value>

    .master("spark://spark-master:7077") \</property>

    .config("spark.hadoop.fs.defaultFS", "hdfs://hadoop-master:9000") \```

    .getOrCreate()

### yarn-site.xml

# Tạo DataFrameCấu hình YARN ResourceManager

data = [("Alice", 25), ("Bob", 30), ("Charlie", 35)]

df = spark.createDataFrame(data, ["Name", "Age"])```xml

df.show()<property>

    <name>yarn.resourcemanager.hostname</name>

# Read từ HDFS    <value>hadoop-master</value>

# df = spark.read.csv("hdfs://hadoop-master:9000/data.csv", header=True)</property>

# df.show()```

```

### spark-defaults.conf

---Cấu hình Spark cluster



## 📊 Streamlit Dashboard```conf

spark.master                        spark://spark-master:7077

Dashboard tự động chạy trên port 8501 khi cluster khởi động.spark.hadoop.fs.defaultFS          hdfs://hadoop-master:9000

spark.executor.memory               1g

**Truy cập**: http://localhost:8501spark.executor.cores                2

```

**Tính năng:**

- Tab 1: Data Analysis (từ HDFS)## 💻 Các Lệnh Hữu Ích

- Tab 2: Query Results (kết quả Spark SQL)

- Tab 3: Model Metrics (ML model performance)### Quản Lý Containers

- Tab 4: Project Info

```bash

**Tùy chỉnh**: Edit `streamlit/app.py`# View logs

docker-compose logs -f

---

# View logs of specific service

## 📁 Cấu Trúc Thư Mụcdocker-compose logs -f hadoop-master



```# SSH into container

hadoop-hoang/docker exec -it hadoop-master bash

├── docker/                    # Docker images

│   ├── Dockerfile.hadoop# View running containers

│   ├── Dockerfile.sparkdocker-compose ps

│   ├── Dockerfile.jupyter

│   └── Dockerfile.streamlit# Remove all containers (and networks)

├── config/                    # Configuration filesdocker-compose down

│   ├── hadoop/```

│   │   ├── core-site.xml

│   │   ├── hdfs-site.xml### HDFS Commands

│   │   └── yarn-site.xml

│   └── spark/```bash

│       └── spark-defaults.conf# SSH vào Hadoop Master

├── scripts/                   # Startup scriptsdocker exec -it hadoop-master bash

│   ├── entrypoint-hadoop-master.sh

│   ├── entrypoint-hadoop-worker.sh# List HDFS files

│   ├── entrypoint-spark-master.shhdfs dfs -ls /

│   └── entrypoint-spark-worker.sh

├── notebooks/                 # Jupyter notebooks# Create directory

│   ├── 01-Test-Connection.ipynbhdfs dfs -mkdir -p /user/hadoop/test

│   ├── 02-WordCount-Example.ipynb

│   └── 03-Data-Processing-Pipeline.ipynb# Upload local file to HDFS

├── streamlit/                 # Dashboardhdfs dfs -put /local/path/file.txt /user/hadoop/test/

│   └── app.py

├── volumes/                   # Persistent storage# Download file from HDFS

│   ├── hadoop_name/hdfs dfs -get /user/hadoop/test/file.txt /local/path/

│   └── hadoop_data/

├── docker-compose.yml# Remove file from HDFS

├── start-cluster.bathdfs dfs -rm /user/hadoop/test/file.txt

├── stop-cluster.bat

└── README.md# View file content

```hdfs dfs -cat /user/hadoop/test/file.txt



---# Check HDFS status

hdfs dfsadmin -report

## 🎯 Ví Dụ Sử Dụng```



### Ví dụ 1: Đọc CSV từ HDFS### Spark Commands



```python```bash

df = spark.read.csv("hdfs://hadoop-master:9000/data.csv", header=True)# SSH vào Spark Master

df.show()docker exec -it spark-master bash

```

# Submit Spark job

### Ví dụ 2: SQL Queryspark-submit --master spark://spark-master:7077 \

             --executor-memory 1g \

```python             --executor-cores 2 \

df.createOrReplaceTempView("data")             your_script.py

results = spark.sql("SELECT * FROM data WHERE age > 25")

results.show()# Run Spark shell

```spark-shell --master spark://spark-master:7077



### Ví dụ 3: Lưu kết quả vào HDFS# Run PySpark shell

pyspark --master spark://spark-master:7077

```python```

df.write.mode("overwrite").csv("hdfs://hadoop-master:9000/output")

```### Jupyter



### Ví dụ 4: Machine LearningTruy cập Jupyter tại http://localhost:8888



```pythonĐể lấy token:

from pyspark.ml.classification import LogisticRegression

```bash

# Train modeldocker logs jupyter-notebook | grep "token="

lr = LogisticRegression(maxIter=10)```

model = lr.fit(df)

## 🧪 Test Connection & Functionality

# Save model

model.save("hdfs://hadoop-master:9000/models/lr")### Test 1: HDFS Connectivity

```

```bash

---docker exec hadoop-master hdfs dfs -ls /

```

## 🔧 Cấu Hình

Expected output:

### Thêm/Giảm Memory```

Found X items

Edit `config/spark/spark-defaults.conf`:drwxr-xr-x  - hadoop supergroup    ...  /spark-logs

```confdrwxr-xr-x  - hadoop supergroup    ...  /tmp

spark.executor.memory    1g      # Giảm xuống 512m nếu không đủ RAMdrwxr-xr-x  - hadoop supergroup    ...  /user

spark.executor.cores     2```

```

### Test 2: Yarn Status

### Thêm Hadoop Worker

```bash

1. Copy service `hadoop-worker-1` trong `docker-compose.yml`docker exec hadoop-master yarn node -list

2. Đổi tên sang `hadoop-worker-3`, port mapping, volume names```

3. Chạy: `docker-compose up -d hadoop-worker-3`

### Test 3: Spark Cluster Status

---

Truy cập http://localhost:8080 để xem Spark Master UI

## ❌ Troubleshooting

Hoặc:

### Containers không start

```bash```bash

# Kiểm tra resourcesdocker exec spark-master curl -s http://localhost:8080 | grep -i worker

docker stats```



# Kiểm tra logs### Test 4: PySpark trong Jupyter

docker-compose logs

```1. Truy cập http://localhost:8888

2. Mở notebook `01-Test-Connection.ipynb`

Đảm bảo có 8GB+ RAM available.3. Run cells lần lượt

4. Kiểm tra output

### HDFS NameNode format error

```bash## 📚 Ví Dụ PySpark

# Xóa persistent volumes

docker-compose down -v### Sử Dụng Cho Các Bài Toán Khác

```

**Hệ thống này không giới hạn cho một bài tập!** Bạn có thể sử dụng nó cho bất kỳ Big Data project nào:

### Spark workers không kết nối

```bash#### Ví dụ 1: Log Analysis

# Kiểm tra logs

docker-compose logs spark-master```python

docker-compose logs spark-worker-1# Read web server logs from HDFS

```logs = spark.read.text("hdfs://hadoop-master:9000/logs/*.log")

errors = logs.filter(logs.value.contains("ERROR"))

### Jupyter không kết nối Sparkerrors.count()

- Chạy từng cell từ từ```

- Chờ Spark khởi động (có thể mất 30-60 giây)

#### Ví dụ 2: Machine Learning

### Port conflict

Edit `docker-compose.yml` và đổi port mapping:```python

```yamlfrom pyspark.ml.classification import LogisticRegression

ports:

  - "19870:9870"  # Changed from 9870:9870# Load data từ HDFS

```df = spark.read.parquet("hdfs://hadoop-master:9000/ml-data")



---# Train model

lr = LogisticRegression(maxIter=10)

## 📚 Tài Liệu Tham Khảomodel = lr.fit(df)



- [Hadoop Docs](https://hadoop.apache.org/docs/r3.3.6/)# Save model

- [Spark Docs](https://spark.apache.org/docs/3.5.0/)model.save("hdfs://hadoop-master:9000/models/lr-model")

- [Docker Compose](https://docs.docker.com/compose/)```



---#### Ví dụ 3: Data Pipeline



## 📝 Notes```python

# ETL job

- HDFS NameNode RPC: `hdfs://hadoop-master:9000`data = spark.read.csv("hdfs://hadoop-master:9000/raw/*.csv", header=True)

- Spark Master: `spark://spark-master:7077`cleaned = data.dropna().filter(data.age > 18)

- Network name: `hadoop-spark-network`cleaned.write.mode("overwrite").parquet("hdfs://hadoop-master:9000/processed/")

- Volumes trong thư mục `volumes/````

- Tất cả services có health checks

#### Ví dụ 4: SQL Analysis (Hive)

---

```python

**Version**: 1.0  # Create table from HDFS data

**Last Updated**: 2026-04-06  df = spark.read.csv("hdfs://hadoop-master:9000/sales.csv", header=True)

**License**: MITdf.createOrReplaceTempView("sales")


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
