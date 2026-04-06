# Hadoop-Spark Cluster on Docker - Hướng Dẫn Đầy Đủ

> Hệ thống Big Data Stack với Hadoop, Spark, YARN, và Jupyter trên Docker

## 📋 Mục Lục
1. [Yêu Cầu Hệ Thống](#yêu-cầu-hệ-thống)
2. [Cài Đặt](#cài-đặt)
3. [Khởi Động Cluster](#khởi-động-cluster)
4. [Luồng Hệ Thống](#luồng-hệ-thống)
5. [Cổng Dịch Vụ](#cổng-dịch-vụ)
6. [Lệnh Test Cơ Bản](#lệnh-test-cơ-bản)
7. [Truy Cập Web UI](#truy-cập-web-ui)
8. [Xử Lý Sự Cố](#xử-lý-sự-cố)

---

## 🖥️ Yêu Cầu Hệ Thống

### Phần Cứng
| Thông số | Yêu cầu tối thiểu | Khuyến nghị |
|---------|-------------------|-----------|
| CPU | 4 cores | 8+ cores |
| RAM | 8 GB | 16+ GB |
| Disk | 20 GB | 50+ GB |
| OS | Windows 10+ / Linux / macOS | Windows 11+ |

### Phần Mềm
```bash
✅ Docker Desktop v20.10 hoặc cao hơn
✅ Docker Compose v1.29 hoặc cao hơn
✅ Git (nếu clone từ repository)
✅ WSL 2 (nếu dùng Windows)
```

### Cấu Hình Docker
- **Memory**: Cấp phát ít nhất 8GB cho Docker Desktop
- **CPU**: Cấp phát ít nhất 4 cores
- **Disk**: Cần ít nhất 30GB không gian trống

---

## 📥 Cài Đặt

### Bước 1: Clone hoặc tải dự án
```bash
# Clone từ Git
git clone https://github.com/SIUTRITUE/hadoop-hoang.git
cd hadoop-hoang

# Hoặc tải zip và giải nén
cd d:\BIGDATA\Hoang\hadoop-hoang
```

### Bước 2: Kiểm tra Docker
```bash
docker --version
docker-compose --version
docker run hello-world
```

### Bước 3: Chuẩn bị thư mục (Windows)
```bash
# Nếu bạn đang trên Windows CMD
cd d:\BIGDATA\Hoang\hadoop-hoang
```

### Bước 4: Xây dựng Images (tuỳ chọn)
```bash
# Tự động xây dựng khi khởi động
# Hoặc xây dựng trước:
docker-compose build
```

---

## 🚀 Khởi Động Cluster

### Cách 1: Sử Dụng Script (Windows)
```batch
# Mở CMD và chạy
start-cluster.bat
```

**Script này sẽ:**
1. ✅ Xây dựng Docker images (nếu chưa có)
2. ✅ Khởi động tất cả containers
3. ✅ Chờ tất cả services healthy (~3-5 phút lần đầu)
4. ✅ Hiển thị URLs truy cập

### Cách 2: Sử Dụng Docker Compose
```bash
docker-compose up -d

# Xem logs
docker-compose logs -f

# Hoặc xem logs của service cụ thể
docker-compose logs -f hadoop-master
docker-compose logs -f spark-master
docker-compose logs -f jupyter
```

### Cách 3: Dừng Cluster
```batch
# Windows
stop-cluster.bat

# Hoặc dùng Docker Compose
docker-compose down
```

### Kiểm Tra Trạng Thái
```bash
# Xem danh sách containers
docker-compose ps

# Kiểm tra logs của container
docker logs hadoop-master
docker logs spark-master
docker logs jupyter-notebook
```

---

## 🔄 Luồng Hệ Thống

### Kiến Trúc Tổng Quát
```
┌─────────────────────────────────────────────────────────┐
│           HADOOP-SPARK CLUSTER ARCHITECTURE             │
└─────────────────────────────────────────────────────────┘

┌──────────────────────────────────────────────────────────┐
│                  CLIENTS / APPLICATIONS                  │
│  ┌─────────────┬──────────────┬──────────────────┐       │
│  │   Jupyter   │   Streamlit  │   Local Client   │       │
│  │  (8888)     │   (8501)     │   Commands       │       │
│  └─────────────┴──────────────┴──────────────────┘       │
└──────────────────────────────────────────────────────────┘
                          ↓↓↓

┌──────────────────────────────────────────────────────────┐
│                   HADOOP-SPARK NETWORK                   │
│              (hadoop-spark-network bridge)               │
└──────────────────────────────────────────────────────────┘

        ┌─────────────────────────────────────┐
        │     HADOOP CLUSTER                  │
        │                                     │
        │  ┌──────────────────────────────┐   │
        │  │   HADOOP-MASTER              │   │
        │  │ ├─ NameNode (9870)           │   │
        │  │ ├─ ResourceManager (8088)    │   │
        │  │ └─ JobHistory (19888)        │   │
        │  └──────────────────────────────┘   │
        │           ↓↓↓                       │
        │  ┌──────────────────────────────┐   │
        │  │  HADOOP-WORKER-1             │   │
        │  │ ├─ DataNode (9864)           │   │
        │  │ └─ NodeManager (8042)        │   │
        │  └──────────────────────────────┘   │
        │                                     │
        │  ┌──────────────────────────────┐   │
        │  │  HADOOP-WORKER-2             │   │
        │  │ ├─ DataNode (9865)           │   │
        │  │ └─ NodeManager (8043)        │   │
        │  └──────────────────────────────┘   │
        │                                     │
        └─────────────────────────────────────┘
                      ↓↓↓

        ┌─────────────────────────────────────┐
        │     SPARK CLUSTER                   │
        │                                     │
        │  ┌──────────────────────────────┐   │
        │  │   SPARK-MASTER               │   │
        │  │ ├─ Master (7077)             │   │
        │  │ ├─ Web UI (8080)             │   │
        │  │ ├─ REST API (6066)           │   │
        │  │ └─ Driver UI (4040)          │   │
        │  └──────────────────────────────┘   │
        │           ↓↓↓                       │
        │  ┌──────────────────────────────┐   │
        │  │  SPARK-WORKER-1              │   │
        │  │ ├─ Executor                  │   │
        │  │ └─ Web UI (8081)             │   │
        │  └──────────────────────────────┘   │
        │                                     │
        │  ┌──────────────────────────────┐   │
        │  │  SPARK-WORKER-2              │   │
        │  │ ├─ Executor                  │   │
        │  │ └─ Web UI (8082)             │   │
        │  └──────────────────────────────┘   │
        │                                     │
        └─────────────────────────────────────┘
```

### Luồng Dữ Liệu

```
┌─────────────────────────────────────────────────────────────┐
│              HADOOP-SPARK DATA FLOW ARCHITECTURE            │
└─────────────────────────────────────────────────────────────┘

1. DATA STORAGE LAYER (Hadoop HDFS)
   ┌──────────────────────────────────────┐
   │         HDFS Cluster                 │
   │  ┌──────────────────────────────┐    │
   │  │   NameNode (Metadata)        │    │
   │  │   hadoop-master:9000         │    │
   │  └──────────────────────────────┘    │
   │           ↓↓↓                        │
   │  ┌──────────────────────────────┐    │
   │  │   DataNode Replication=2     │    │
   │  ├─ hadoop-worker-1 (9864)     │    │
   │  ├─ hadoop-worker-2 (9865)     │    │
   │  └──────────────────────────────┘    │
   └──────────────────────────────────────┘
           ↑                    ↑
       (Read/Write)        (Read/Write)

2. INPUT SOURCES
   ├─ Jupyter (Upload files)
   ├─ Streamlit (Stream data)
   └─ External clients (HDFS API)
        ↓↓↓ PUT command ↓↓↓
   Store in HDFS (Distributed)

3. PROCESSING LAYER (Spark)
   ┌──────────────────────────────────────┐
   │       Spark Cluster                  │
   │  ┌──────────────────────────────┐    │
   │  │   Spark Master               │    │
   │  │   spark://spark-master:7077  │    │
   │  └──────────────────────────────┘    │
   │           ↓↓↓                        │
   │  ┌──────────────────────────────┐    │
   │  │   Spark Workers (Executors)  │    │
   │  ├─ spark-worker-1 (8081)      │    │
   │  ├─ spark-worker-2 (8082)      │    │
   │  └──────────────────────────────┘    │
   └──────────────────────────────────────┘
        ↑           |          ↓
        |     (Process Jobs)   |
        |           |          |
   READ DATA   TRANSFORM/   WRITE RESULTS
   from HDFS   AGGREGATE    back to HDFS

4. COMPLETE DATA PIPELINE
   
   ┌─────────────────┐
   │   External      │
   │   Data Source   │
   └────────┬────────┘
            │
            ↓
   ┌─────────────────────────────────────┐
   │  Jupyter / Streamlit / Client       │
   │  Upload Data (HDFS PUT)             │
   └─────────────────────────────────────┘
            │
            ↓
   ┌──────────────────────────────────────┐
   │  HDFS Storage                        │
   │  (Namenode: hadoop-master)           │
   │  (Datanodes: workers)                │
   │  Replication Factor = 2              │
   └──────────────────────────────────────┘
            │
            ↓ (HDFS Read Path)
   ┌──────────────────────────────────────┐
   │  Spark Cluster                       │
   │  Submit Application                  │
   │  - Read from HDFS                    │
   │  - Transform data                    │
   │  - Run MapReduce/SQL/ML              │
   │  - Aggregate results                 │
   └──────────────────────────────────────┘
            │
            ↓ (HDFS Write Path)
   ┌──────────────────────────────────────┐
   │  Output Results in HDFS              │
   │  /output/results/                    │
   └──────────────────────────────────────┘
            │
            ├→ Jupyter: Visualize results
            ├→ Streamlit: Dashboard
            └→ Download: Get output files

5. MONITORING & OBSERVABILITY
   ┌─────────────────────────────────────────────┐
   │  Hadoop NameNode UI (9870)                  │
   │  - HDFS file browser                        │
   │  - Blocks replication status                │
   └─────────────────────────────────────────────┘
   ┌─────────────────────────────────────────────┐
   │  YARN ResourceManager (8088)                │
   │  - Running applications                     │
   │  - Node resources                           │
   │  - Completed jobs history                   │
   └─────────────────────────────────────────────┘
   ┌─────────────────────────────────────────────┐
   │  Spark Master Web UI (8080)                 │
   │  - Application status                       │
   │  - Executor information                     │
   │  - Event timeline                           │
   └─────────────────────────────────────────────┘
```

---

## 🔌 Cổng Dịch Vụ

### Hadoop Master Ports
| Cổng | Dịch vụ | Mô tả |
|------|---------|-------|
| 9870 | NameNode Web UI | Quản lý HDFS |
| 8088 | YARN ResourceManager Web UI | Quản lý tài nguyên & jobs |
| 9000 | HDFS RPC | Client kết nối HDFS |
| 8032 | YARN ResourceManager RPC | Resource Manager RPC |
| 8030 | YARN Scheduler | Scheduler port |
| 8031 | YARN Resource Tracker | Resource Tracker |
| 19888 | Job History Server Web UI | Xem lịch sử jobs |
| 10020 | Job History Server RPC | Job History RPC |

### Hadoop Worker 1 Ports
| Cổng | Dịch vụ | Mô tả |
|------|---------|-------|
| 9864 | DataNode Web UI | Thông tin DataNode |
| 8042 | NodeManager Web UI | Quản lý node |

### Hadoop Worker 2 Ports (Port Mapping)
| Host Port | Container Port | Dịch vụ |
|-----------|----------------|---------|
| 9865 | 9864 | DataNode Web UI |
| 8043 | 8042 | NodeManager Web UI |

### Spark Master Ports
| Cổng | Dịch vụ | Mô tả |
|------|---------|-------|
| 8080 | Spark Master Web UI | Quản lý Spark cluster |
| 7077 | Spark Master | Spark master port |
| 6066 | Spark REST API | REST API endpoint |
| 4040 | Spark Driver UI | Application UI |

### Spark Worker 1 Ports
| Cổng | Dịch vụ | Mô tả |
|------|---------|-------|
| 8081 | Spark Worker Web UI | Worker 1 information |
| 7078 | Spark Worker | Worker 1 port |

### Spark Worker 2 Ports (Port Mapping)
| Host Port | Container Port | Dịch vụ |
|-----------|----------------|---------|
| 8082 | 8081 | Spark Worker Web UI |
| 7079 | 7078 | Spark Worker Port |

### Jupyter & Streamlit Ports
| Cổng | Dịch vụ | Mô tả |
|------|---------|-------|
| 8888 | Jupyter Lab | Notebook interface |
| 8501 | Streamlit | Dashboard interface |

### Tóm Tắt Tất Cả Cổng
```
Hadoop Master:  9870, 8088, 9000, 8032, 8030, 8031, 19888, 10020
Hadoop Worker 1: 9864, 8042
Hadoop Worker 2: 9865, 8043
Spark Master:   8080, 7077, 6066, 4040
Spark Worker 1: 8081, 7078
Spark Worker 2: 8082, 7079
Jupyter:        8888
Streamlit:      8501
```

---

## 🧪 Lệnh Test Cơ Bản

### 1. Test Kết Nối HDFS

#### Test 1.1: Liệt kê HDFS root directory
```bash
docker exec hadoop-master hdfs dfs -ls /
```

**Expected Output:**
```
Found X items
drwxr-xr-x   - root supergroup          0 YYYY-MM-DD HH:MM /tmp
...
```

#### Test 1.2: Tạo thư mục test
```bash
docker exec hadoop-master hdfs dfs -mkdir -p /test/input
```

#### Test 1.3: Upload file test
```bash
# Tạo file test trên host
echo "Hello Hadoop" > test.txt

# Upload vào HDFS
docker exec -i hadoop-master hdfs dfs -put - /test/input/test.txt < test.txt
```

#### Test 1.4: Download file từ HDFS
```bash
docker exec hadoop-master hdfs dfs -get /test/input/test.txt -

# Output: Hello Hadoop
```

#### Test 1.5: Xem thông tin HDFS
```bash
docker exec hadoop-master hdfs dfsadmin -report
```

---

### 2. Test YARN & MapReduce

#### Test 2.1: Liệt kê nodes
```bash
docker exec hadoop-master yarn node -list
```

**Expected Output:**
```
Nodes: 3
        Node-Id             Node-State Node-Http-Address Memory-Used Memory-Avail...
hadoop-worker-1:8042       RUNNING    hadoop-worker-1:8042 ...
hadoop-worker-2:8042       RUNNING    hadoop-worker-2:8042 ...
```

#### Test 2.2: Chạy WordCount example
```bash
docker exec hadoop-master bash -c "
  echo 'hadoop spark hadoop yarn hadoop' > /tmp/wordcount.txt
  hadoop jar /opt/hadoop/share/hadoop/mapreduce/hadoop-mapreduce-examples-*.jar \
    wordcount /tmp/wordcount.txt /output/wordcount
"
```

#### Test 2.3: Xem kết quả WordCount
```bash
docker exec hadoop-master hdfs dfs -cat /output/wordcount/part-r-00000
```

**Expected Output:**
```
hadoop  3
spark   1
yarn    1
```

#### Test 2.4: Xem status của jobs
```bash
docker exec hadoop-master mapred job -list
```

---

### 3. Test Spark

#### Test 3.1: Chạy Spark shell test
```bash
docker exec spark-master spark-shell --master spark://spark-master:7077 \
  --deploy-mode client \
  --executor-memory 1G \
  --total-executor-cores 2 \
  -c "sc.textFile(\"/test/input/test.txt\").collect.foreach(println); System.exit(0)"
```

#### Test 3.2: Submit Spark job từ Docker
```bash
docker exec -i spark-master bash << 'EOF'
spark-submit \
  --master spark://spark-master:7077 \
  --deploy-mode client \
  --executor-memory 1G \
  --total-executor-cores 2 \
  --class org.apache.spark.examples.SparkPi \
  /opt/spark/examples/jars/spark-examples_2.12-3.5.0.jar 100
EOF
```

**Expected Output:** Pi is roughly 3.14XXXX

#### Test 3.3: Test PySpark
```bash
docker exec spark-master python3 << 'EOF'
from pyspark.sql import SparkSession

spark = SparkSession.builder \
    .appName("Test PySpark") \
    .master("spark://spark-master:7077") \
    .getOrCreate()

data = [("Alice", 25), ("Bob", 30), ("Charlie", 35)]
df = spark.createDataFrame(data, ["name", "age"])
df.show()
EOF
```

---

### 4. Test Jupyter Notebook

#### Test 4.1: Kiểm tra Jupyter status
```bash
docker exec jupyter-notebook curl -s http://localhost:8888/api/sessions | head -c 200
```

#### Test 4.2: List notebooks
```bash
docker exec jupyter-notebook ls -la /home/jovyan/work/
```

#### Test 4.3: Chạy cell từ notebook
- Mở: http://localhost:8888
- Chạy notebook: `01-Test-Connection.ipynb`

---

### 5. Test Tích Hợp (End-to-End)

#### Test 5.1: HDFS + Spark + Jupyter
```bash
# 1. Upload data lên HDFS
docker exec -i hadoop-master hdfs dfs -put - /data/test.csv << 'EOF'
name,age,city
Alice,25,NYC
Bob,30,LA
Charlie,35,SF
EOF

# 2. Test đọc từ Jupyter (xem trong notebook)
# 3. Kiểm tra kết quả trong YARN

# 4. Kiểm tra logs
docker exec hadoop-master yarn logs -applicationId <app-id>
```

#### Test 5.2: Data Processing Pipeline
```bash
# Upload dữ liệu
docker cp data/shop_transactions.csv hadoop-master:/tmp/
docker exec hadoop-master hdfs dfs -put /tmp/shop_transactions.csv /data/

# Chạy notebook: 03-Data-Processing-Pipeline.ipynb
```

---

### 6. Test Health & Status

#### Test 6.1: Docker Compose Status
```bash
# Xem status tất cả containers
docker-compose ps

# Xem logs
docker-compose logs

# Xem logs của service cụ thể
docker-compose logs -f hadoop-master
docker-compose logs -f spark-master
```

#### Test 6.2: Health Check Containers
```bash
# Xem health status
docker inspect --format='{{.State.Health.Status}}' hadoop-master
docker inspect --format='{{.State.Health.Status}}' spark-master
docker inspect --format='{{.State.Health.Status}}' jupyter-notebook
```

#### Test 6.3: Network Test
```bash
# Kiểm tra kết nối giữa containers
docker exec hadoop-master ping spark-master
docker exec spark-master ping hadoop-master
docker exec jupyter-notebook ping spark-master
```

---

## 🌐 Truy Cập Web UI

### Bảng Tổng Hợp
| Tên | URL | Mô tả |
|-----|-----|-------|
| **HDFS NameNode** | http://localhost:9870 | Quản lý HDFS, xem file tree |
| **YARN ResourceManager** | http://localhost:8088 | Quản lý tài nguyên, xem running jobs |
| **Spark Master** | http://localhost:8080 | Quản lý Spark cluster, xem workers |
| **Spark Worker 1** | http://localhost:8081 | Thông tin Worker 1 |
| **Spark Worker 2** | http://localhost:8082 | Thông tin Worker 2 (mapped) |
| **Job History Server** | http://localhost:19888 | Lịch sử các jobs |
| **Jupyter Lab** | http://localhost:8888 | Notebook environment |
| **Streamlit Dashboard** | http://localhost:8501 | Data visualization dashboard |

### Hướng Dẫn Chi Tiết

#### 1. HDFS NameNode (9870)
```
URL: http://localhost:9870
├─ Browse File System: Xem và quản lý files
├─ Namenode Logs: Xem logs
├─ Cluster: Xem thông tin cluster
└─ Utilities: Tools khác
```

#### 2. YARN ResourceManager (8088)
```
URL: http://localhost:8088
├─ Active Jobs: Xem các job đang chạy
├─ Completed Jobs: Lịch sử jobs
├─ Nodes: Thông tin nodes
└─ Scheduler: Queue và scheduler info
```

#### 3. Spark Master (8080)
```
URL: http://localhost:8080
├─ Spark Jobs: Applications chạy
├─ Executors: Thông tin executors
├─ Environment: Spark config
└─ Logs: Application logs
```

#### 4. Jupyter Lab (8888)
```
URL: http://localhost:8888
├─ File Browser: Quản lý files
├─ Notebook Editor: Viết code
├─ Terminal: Bash terminal
└─ Kernels: Quản lý kernels
```

---

## 🔧 Xử Lý Sự Cố

### Sự Cố 1: Containers không khởi động
```bash
# Kiểm tra logs
docker-compose logs

# Xóa và khởi động lại
docker-compose down
docker-compose up -d

# Kiểm tra resources
docker stats
```

### Sự Cố 2: HDFS không hoạt động
```bash
# Kiểm tra NameNode
docker exec hadoop-master hdfs dfsadmin -report

# Format HDFS (WARNING: xóa tất cả data)
docker exec hadoop-master hdfs namenode -format

# Restart containers
docker-compose restart hadoop-master
docker-compose restart hadoop-worker-1
docker-compose restart hadoop-worker-2
```

### Sự Cố 3: Spark không kết nối Hadoop
```bash
# Kiểm tra logs
docker logs spark-master

# Kiểm tra environment
docker exec spark-master env | grep -i hadoop

# Restart Spark
docker-compose restart spark-master
docker-compose restart spark-worker-1
docker-compose restart spark-worker-2
```

### Sự Cố 4: Jupyter không tìm thấy Spark
```bash
# Xem logs Jupyter
docker logs jupyter-notebook

# Kiểm tra PySpark
docker exec jupyter-notebook python3 -c "from pyspark.sql import SparkSession; print('OK')"

# Restart Jupyter
docker-compose restart jupyter
```

### Sự Cố 5: Out of Memory
```bash
# Tăng cấp phát Docker Desktop memory
# Docker Desktop → Preferences → Resources → Memory: 12GB+

# Hoặc reduce Spark memory
# Sửa docker-compose.yml, giảm EXECUTOR_MEMORY
```

### Sự Cố 6: Ports bị chiếm dụng
```bash
# Tìm process sử dụng port
netstat -ano | findstr :8888

# Dừng process (Windows PowerShell as Admin)
Get-Process | Where-Object {$_.ProcessName -like "*docker*"} | Stop-Process -Force
```

---

## 📊 Giám Sát & Debugging

### Xem Logs Chi Tiết
```bash
# Tất cả containers
docker-compose logs -f

# Specific container
docker-compose logs -f hadoop-master
docker-compose logs -f spark-master
docker-compose logs -f jupyter

# Last 50 lines
docker-compose logs --tail=50

# Timestamps
docker-compose logs -t
```

### Truy Cập Container Shell
```bash
# Hadoop Master
docker exec -it hadoop-master bash

# Spark Master
docker exec -it spark-master bash

# Jupyter
docker exec -it jupyter-notebook bash
```

### Kiểm Tra Resource Usage
```bash
# Docker stats
docker stats

# Cụ thể container
docker stats hadoop-master
```

---

## 📚 Tài Liệu & Ví Dụ

### Jupyter Notebooks Có Sẵn
1. **01-Test-Connection.ipynb**: Kiểm tra kết nối Hadoop & Spark
2. **02-WordCount-Example.ipynb**: MapReduce WordCount example
3. **03-Data-Processing-Pipeline.ipynb**: Data processing workflow

### Dữ Liệu Sample
- **data/shop_transactions.csv**: Sample transaction data

### Scripts
- **start-cluster.bat**: Khởi động cluster (Windows)
- **stop-cluster.bat**: Dừng cluster (Windows)

---

## 🎓 Các Lệnh Thực Tế Thường Dùng

### HDFS Commands
```bash
# Liệt kê directory
docker exec hadoop-master hdfs dfs -ls /path

# Tạo thư mục
docker exec hadoop-master hdfs dfs -mkdir -p /path

# Upload file
docker exec -i hadoop-master hdfs dfs -put - /hdfs/path < local_file

# Download file
docker exec hadoop-master hdfs dfs -get /hdfs/path - > local_file

# Xóa file
docker exec hadoop-master hdfs dfs -rm /hdfs/path

# Xem nội dung file
docker exec hadoop-master hdfs dfs -cat /hdfs/path

# Copy giữa các thư mục
docker exec hadoop-master hdfs dfs -cp /source /dest
```

### Spark Commands
```bash
# Submit Scala job
docker exec spark-master spark-submit \
  --master spark://spark-master:7077 \
  --deploy-mode client \
  /path/to/job.jar arg1 arg2

# Submit Python job
docker exec spark-master spark-submit \
  --master spark://spark-master:7077 \
  --deploy-mode client \
  /path/to/job.py arg1 arg2

# Spark SQL Shell
docker exec -it spark-master spark-sql --master spark://spark-master:7077
```

### YARN Commands
```bash
# Xem nodes
docker exec hadoop-master yarn node -list

# Xem applications
docker exec hadoop-master yarn application -list

# Kill application
docker exec hadoop-master yarn application -kill app_id

# Xem queue status
docker exec hadoop-master yarn queue -status
```

---

## ✅ Checklist Khởi Động

- [ ] Docker Desktop đã cài và chạy
- [ ] RAM cấp phát ≥ 8GB
- [ ] Chạy `start-cluster.bat`
- [ ] Chờ tất cả containers healthy (~5 phút)
- [ ] Mở http://localhost:9870 (HDFS NameNode)
- [ ] Mở http://localhost:8088 (YARN)
- [ ] Mở http://localhost:8080 (Spark)
- [ ] Mở http://localhost:8888 (Jupyter)
- [ ] Chạy test commands cơ bản
- [ ] Upload test data
- [ ] Chạy Jupyter notebooks

---

## 📞 Hỗ Trợ

### Tài Liệu Tham Khảo
- [Hadoop Documentation](https://hadoop.apache.org/)
- [Spark Documentation](https://spark.apache.org/)
- [Docker Documentation](https://docs.docker.com/)
- [Jupyter Documentation](https://jupyter.org/)

### Thư Mục Cấu Trúc Dự Án
```
hadoop-hoang/
├── docker/                    # Dockerfiles
│   ├── Dockerfile.hadoop
│   ├── Dockerfile.spark
│   ├── Dockerfile.jupyter
│   └── Dockerfile.streamlit
├── config/                    # Configuration files
│   ├── hadoop/
│   │   ├── core-site.xml
│   │   ├── hdfs-site.xml
│   │   └── yarn-site.xml
│   └── spark/
│       └── spark-defaults.conf
├── scripts/                   # Shell scripts
│   ├── entrypoint-hadoop-master.sh
│   ├── entrypoint-hadoop-worker.sh
│   ├── entrypoint-spark-master.sh
│   └── entrypoint-spark-worker.sh
├── notebooks/                 # Jupyter notebooks
│   ├── 01-Test-Connection.ipynb
│   ├── 02-WordCount-Example.ipynb
│   └── 03-Data-Processing-Pipeline.ipynb
├── streamlit/                 # Streamlit app
│   └── app.py
├── data/                      # Sample data
│   └── shop_transactions.csv
├── volumes/                   # Persistent storage
│   ├── hadoop_name/
│   └── hadoop_data/
├── docker-compose.yml         # Main orchestration file
├── start-cluster.bat          # Startup script (Windows)
├── stop-cluster.bat           # Shutdown script (Windows)
├── README.md                  # This file
└── QUICKSTART.md              # Quick start guide
```

---

## 📝 License
Dự án này được cấp phép dưới MIT License.

---

**Tác tác chiếu:** Tháng 4, 2026
**Phiên bản:** 1.0.0
**Status:** ✅ Production Ready

