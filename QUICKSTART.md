# Hướng Dẫn Nhanh - Hadoop-Spark on Docker (Windows)

## 🚀 Bắt Đầu trong 5 Phút

### 1. Chuẩn Bị
- ✅ Docker Desktop đã cài (version 20.10+)
- ✅ RAM: Min 8GB
- ✅ Disk: Min 20GB
- ✅ Internet connection (để download images)

### 2. Khởi Động Cluster
```bash
cd d:\BIGDATA\Hoang\hadoop-hoang
start-cluster.bat
```

Script sẽ:
1. Build Docker images (~5-10 min lần đầu)
2. Start containers (~30s)
3. Chờ services ready (~1-2 min)
4. Hiển thị URLs

### 3. Truy Cập Web UIs
Mở browser nhập URLs:
- ✅ Hadoop: http://localhost:9870
- ✅ YARN: http://localhost:8088
- ✅ Spark: http://localhost:8080
- ✅ Jupyter: http://localhost:8888

### 4. Dừng Cluster
```bash
stop-cluster.bat
```

---

## ✅ Test Connectivity

### Test 1: HDFS
```bash
docker exec hadoop-master hdfs dfs -ls /
```

### Test 2: YARN
```bash
docker exec hadoop-master yarn node -list
```

### Test 3: Spark
```bash
docker exec spark-master curl -s http://localhost:8080 | findstr worker
```

---

## 🧪 Chạy Ví Dụ

### Jupyter Notebook
1. Truy cập: http://localhost:8888
2. Mở: `01-Test-Connection.ipynb`
3. Run cells từ trên xuống

### Command Line
```bash
# SSH vào Hadoop Master
docker exec -it hadoop-master bash

# Chạy HDFS commands
hdfs dfs -mkdir /test
hdfs dfs -put local_file.txt /test/

# SSH vào Spark Master
docker exec -it spark-master bash

# Chạy Spark shell
spark-shell --master spark://spark-master:7077
```

---

## 📊 Các Lệnh Hữu Ích

| Lệnh | Mô Tả |
|------|-------|
| `docker-compose ps` | Xem status containers |
| `docker-compose logs` | Xem logs tất cả |
| `docker-compose logs hadoop-master` | Logs Hadoop Master |
| `docker exec -it hadoop-master bash` | SSH vào container |
| `docker-compose down` | Dừng cluster |
| `docker-compose down -v` | Dừng + xóa volumes |

---

## ❌ Troubleshooting

### Problem: Containers crash
**Solution**: 
```bash
docker-compose down -v
start-cluster.bat
```

### Problem: Out of memory
**Solution**: Giảm memory trong docker-compose.yml
```yaml
spark.executor.memory 512m
```

### Problem: Port conflicts
**Solution**: Đổi port trong docker-compose.yml
```yaml
ports:
  - "19870:9870"  # Changed from 9870
```

### Problem: Can't SSH into container
**Solution**: 
```bash
# Kiểm tra container running
docker-compose ps

# View logs
docker-compose logs hadoop-master
```

---

## 📚 PySpark Examples

### Example 1: Tạo DataFrame
```python
from pyspark.sql import SparkSession

spark = SparkSession.builder \
    .appName("Test") \
    .master("spark://spark-master:7077") \
    .getOrCreate()

data = [("Alice", 25), ("Bob", 30)]
df = spark.createDataFrame(data, ["Name", "Age"])
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

### Example 4: SQL Queries
```python
df.createOrReplaceTempView("people")
spark.sql("SELECT * FROM people WHERE Age > 25").show()
```

---

## 🔄 Scaling

### Thêm Hadoop Worker
1. Mở `docker-compose.yml`
2. Copy `hadoop-worker-2` section
3. Rename thành `hadoop-worker-3`
4. Đổi hostname, container_name, ports
5. Chạy: `docker-compose up -d hadoop-worker-3`

---

## 📁 Project Structure
```
hadoop-hoang/
├── docker/              # Dockerfile
├── config/              # XML configs
├── scripts/             # Entrypoint scripts
├── notebooks/           # Jupyter examples
├── volumes/             # Persistent data
├── docker-compose.yml   # Main config
├── start-cluster.bat    # Start script
├── stop-cluster.bat     # Stop script
└── README.md           # Full documentation
```

---

## 🔗 Links

- Hadoop: http://localhost:9870
- YARN: http://localhost:8088
- Spark: http://localhost:8080
- Jupyter: http://localhost:8888

---

## 💡 Tips

1. **First time**: Build images takes 5-10 min, next time faster
2. **Data persistence**: Data in `volumes/` is saved even after `docker-compose down`
3. **Performance**: Reduce executor memory if OOM errors occur
4. **Debugging**: Always check `docker-compose logs` first

---

## ✨ Next Steps

1. ✅ Start cluster: `start-cluster.bat`
2. ✅ Check Hadoop: http://localhost:9870
3. ✅ Check Spark: http://localhost:8080
4. ✅ Open Jupyter: http://localhost:8888
5. ✅ Run examples
6. ✅ Create your jobs

---

**Happy Big Data Processing! 🚀**
