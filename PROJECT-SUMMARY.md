# Hadoop-Spark Cluster - Project Summary

## ✅ Đã Hoàn Thành

### 1. ✅ Kiến Trúc Hệ Thống
- 1x Hadoop Master (NameNode + ResourceManager)
- 2x Hadoop Worker (DataNode + NodeManager)
- 1x Spark Master
- 2x Spark Worker
- 1x Jupyter Notebook with PySpark

### 2. ✅ Docker Images
- **Dockerfile.hadoop**: Ubuntu 22.04 + Hadoop 3.3.6 + Java 11
- **Dockerfile.spark**: Ubuntu 22.04 + Spark 3.5.0 + Hadoop 3.3.6
- **Dockerfile.jupyter**: Jupyter + PySpark + Hadoop + Spark

### 3. ✅ Configuration Files
- **core-site.xml**: HDFS NameNode, proxy settings
- **hdfs-site.xml**: DataNode, replication (factor=2), web UI ports
- **yarn-site.xml**: ResourceManager, NodeManager, memory configs
- **spark-defaults.conf**: Spark cluster, executor configs

### 4. ✅ Scripts & Entrypoints
- **entrypoint-hadoop-master.sh**: Khởi động NameNode + ResourceManager
- **entrypoint-hadoop-worker.sh**: Khởi động DataNode + NodeManager
- **entrypoint-spark-master.sh**: Khởi động Spark Master
- **entrypoint-spark-worker.sh**: Khởi động Spark Worker

### 5. ✅ Orchestration
- **docker-compose.yml**: Toàn bộ cluster orchestration
  - Service dependencies
  - Health checks
  - Volume mounting
  - Port exposure
  - Network configuration

### 6. ✅ Startup Scripts
- **start-cluster.bat**: Windows startup script
- **stop-cluster.bat**: Windows stop script

### 7. ✅ Documentation
- **README.md**: Full documentation (Tiếng Anh)
- **QUICKSTART.md**: Quick reference guide
- **WELCOME.bat**: Welcome screen

### 8. ✅ Jupyter Examples
- **01-Test-Connection.ipynb**
  - PySpark connection test
  - HDFS read/write
  - DataFrame operations
  - SQL queries
  - RDD operations

- **02-WordCount-Example.ipynb**
  - WordCount MapReduce example
  - RDD-based approach
  - DataFrame-based approach
  - Results saved to HDFS

- **03-Data-Processing-Pipeline.ipynb**
  - Sample sales data generation
  - Data cleaning and transformation
  - Aggregation and analysis
  - Window functions
  - Joins
  - SQL queries
  - Visualization

### 9. ✅ Configuration Files
- **.env**: Environment variables
- **.dockerignore**: Docker build optimization
- **Makefile**: Useful commands

---

## 📁 Project Structure

```
hadoop-hoang/
├── docker/
│   ├── Dockerfile.hadoop
│   ├── Dockerfile.spark
│   └── Dockerfile.jupyter
├── config/
│   ├── hadoop/
│   │   ├── core-site.xml
│   │   ├── hdfs-site.xml
│   │   └── yarn-site.xml
│   └── spark/
│       └── spark-defaults.conf
├── scripts/
│   ├── init-hadoop.sh
│   ├── healthcheck.sh
│   ├── entrypoint-hadoop-master.sh
│   ├── entrypoint-hadoop-worker.sh
│   ├── entrypoint-spark-master.sh
│   └── entrypoint-spark-worker.sh
├── notebooks/
│   ├── 01-Test-Connection.ipynb
│   ├── 02-WordCount-Example.ipynb
│   └── 03-Data-Processing-Pipeline.ipynb
├── volumes/
│   ├── hadoop_name/
│   └── hadoop_data/
├── docker-compose.yml
├── start-cluster.bat
├── stop-cluster.bat
├── .env
├── .dockerignore
├── README.md
├── QUICKSTART.md
├── WELCOME.bat
└── PROJECT-SUMMARY.md (this file)
```

---

## 🚀 Cách Sử Dụng

```bash
cd d:\BIGDATA\Hoang\hadoop-hoang
start-cluster.bat
```

---

## 🌐 Web UIs

| Service | URL | Port |
|---------|-----|------|
| Hadoop NameNode | http://localhost:9870 | 9870 |
| YARN ResourceManager | http://localhost:8088 | 8088 |
| Spark Master | http://localhost:8080 | 8080 |
| Spark Worker 1 | http://localhost:8081 | 8081 |
| Spark Worker 2 | http://localhost:8082 | 8082 |
| Jupyter Notebook | http://localhost:8888 | 8888 |

---

## 🔧 Versions

- **Hadoop**: 3.3.6
- **Spark**: 3.5.0
- **Java**: OpenJDK 11
- **Python**: 3.9 (Jupyter)
- **Ubuntu**: 22.04
- **Docker**: 20.10+ required

---

## ✨ Features

✅ Distributed Hadoop cluster with 1 Master + 2 Workers
✅ Distributed Spark cluster with 1 Master + 2 Workers
✅ Complete HDFS with replication
✅ YARN ResourceManager
✅ Jupyter Notebook with PySpark
✅ Health checks for all services
✅ Persistent volumes for data
✅ Docker network isolation
✅ Service dependencies management
✅ Complete configuration files
✅ Multiple example notebooks
✅ Easy startup/stop scripts
✅ Full documentation

---

## 📊 Key Configurations

### HDFS
- Replication Factor: 2
- NameNode: hadoop-master:9000
- Web UI: http://hadoop-master:9870

### YARN
- ResourceManager: hadoop-master:8088
- NodeManager Memory: 2048MB per worker
- NodeManager Cores: 2 per worker

### Spark
- Master: spark://spark-master:7077
- Web UI: http://spark-master:8080
- Executor Memory: 1GB each
- Executor Cores: 2 each

### HDFS Connectivity
- Hadoop clients in all containers
- Spark configured to use HDFS
- Jupyter can read/write to HDFS

---

## 🧪 Quick Tests

### Test HDFS
```bash
docker exec hadoop-master hdfs dfs -ls /
```

### Test YARN
```bash
docker exec hadoop-master yarn node -list
```

### Test Spark
Open http://localhost:8080

### Test Jupyter
Open http://localhost:8888

---

## 🔄 Scaling

### Add Hadoop Worker
1. Copy `hadoop-worker-2` section in docker-compose.yml
2. Rename to `hadoop-worker-3`
3. Run: `docker-compose up -d hadoop-worker-3`

### Add Spark Worker
1. Copy `spark-worker-2` section in docker-compose.yml
2. Rename to `spark-worker-3`
3. Run: `docker-compose up -d spark-worker-3`

---

## 💡 Production Considerations

⚠️ Current setup is for development/testing

For production:
- [ ] Enable Kerberos authentication
- [ ] Enable HDFS encryption
- [ ] Configure backup/replication
- [ ] Setup monitoring (Prometheus, Grafana)
- [ ] Configure logging (ELK stack)
- [ ] Setup proper resource limits
- [ ] Enable Spark history server
- [ ] Configure YARN queues

---

## 📚 Documentation Files

1. **README.md** - Complete documentation with all details
2. **QUICKSTART.md** - Quick reference for common tasks
3. **PROJECT-SUMMARY.md** - This file, overview
4. **docker-compose.yml** - Service definitions with comments
5. **Example Notebooks** - Jupyter notebooks with PySpark code

---

## 🎯 What's Next?

1. ✅ Review all files in the project
2. ✅ Run `start-cluster.bat` to start the cluster
3. ✅ Wait for all services to be ready (5-10 minutes)
4. ✅ Access Hadoop UI (http://localhost:9870)
5. ✅ Access Spark UI (http://localhost:8080)
6. ✅ Access Jupyter (http://localhost:8888)
7. ✅ Run example notebooks
8. ✅ Create your own Big Data jobs

---

## 🤝 Support

If you encounter issues:

1. Check docker-compose logs: `docker-compose logs`
2. Check specific service: `docker-compose logs <service-name>`
3. SSH into container: `docker exec -it <container-name> bash`
4. Check README.md troubleshooting section

---

## 📝 Notes

- All services use Docker bridge network
- Data persists in `volumes/` directory
- SSH passwordless login between nodes
- Health checks ensure service readiness
- Services start in correct order via `depends_on`
- All UIs accessible from localhost

---

**Project Status**: ✅ COMPLETE & READY TO USE

Created: 2026-04-01
Version: 1.0
License: MIT
