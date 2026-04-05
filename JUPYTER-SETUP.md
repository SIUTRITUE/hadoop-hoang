# 🚀 Hướng Dẫn Chạy Notebook Qua Docker Jupyter

## ⚠️ Vấn đề Hiện Tại
Bạn đang chạy notebook từ **VS Code Local Kernel** (Windows), nhưng nó cần chạy từ **Jupyter Container** (trong Docker).

**Lý do:**
- ❌ Windows không có Java/Spark/Hadoop
- ❌ Không thể kết nối tới containers qua hostname
- ❌ Thiếu configuration files
- ✅ Docker Jupyter container có đủ tất cả

---

## 🌐 Cách Truy Cập Jupyter Web

### **Bước 1: Kiểm tra Jupyter đã chạy**
```bash
docker ps | findstr jupyter
```
Kết quả phải có: `jupyter-notebook ... Up ... 0.0.0.0:8888->8888/tcp`

### **Bước 2: Mở Trình Duyệt**
Nhập URL này vào thanh địa chỉ:
```
http://127.0.0.1:8888
```

### **Bước 3: Nhập Token (nếu cần)**
Nếu yêu cầu token, lấy từ logs:
```bash
docker logs jupyter-notebook 2>&1 | findstr "token=" | head -1
```

---

## 📂 Mở Notebook

1. **Trang chủ Jupyter** → Thư mục `work/` (hoặc `notebooks/`)
2. Click vào file: **`01-Test-Connection.ipynb`**
3. Notebook sẽ mở trong tab mới

---

## ▶️ Chạy Cells

Mỗi cell cần được chạy **tuần tự từ trên xuống**:

**Cell 1️⃣ - Environment Setup** (chạy đầu tiên)
```python
import os
import sys
os.environ['JAVA_HOME'] = '/usr/lib/jvm/java-17-openjdk-amd64'
...
```
→ Nhấn `Shift + Enter` hoặc nút ▶️

**Cell 2️⃣ - Import PySpark**
```python
from pyspark.sql import SparkSession
```
→ Nhấn `Shift + Enter`

**Cell 3️⃣ - Create SparkSession** ⭐ **CẤP QUAN TRỌNG**
```python
spark = SparkSession.builder.master("local[2]")...
```
→ Nhấn `Shift + Enter` → **Chờ 30-60 giây**

**Nếu thành công** → Sẽ thấy:
```
✓ SparkSession created successfully in LOCAL mode!

Session Details:
  Spark version: 3.5.0
  Master: local[2]
  App Name: Hadoop-Spark-Test
  Default Parallelism: 2
```

**Các cells tiếp theo:**
- Cell 4-14: Kiểm tra HDFS, DataFrame, RDD, SQL operations

---

## 🔗 Shortcuts Jupyter

| Phím | Ý Nghĩa |
|------|---------|
| `Shift + Enter` | Chạy cell hiện tại |
| `Ctrl + Enter` | Chạy cell không move |
| `Alt + Enter` | Chạy + tạo cell mới |
| `Ctrl + L` | Clear output |
| `Ctrl + Shift + C` | Bản sao cell |

---

## ❌ Nếu Gặp Lỗi

### "Connection refused" / "Java gateway"
**Giải pháp:**
1. Kiểm tra Spark Master healthy: `docker ps | findstr spark-master`
2. Restart Jupyter: `docker-compose restart jupyter`
3. Chờ 30 giây rồi thử lại

### "JAVA_HOME not found"
**Giải pháp:** Chạy Cell 1 trước (environment setup)

### Notebook load chậm
**Giải pháp:** 
1. Chờ 10-20 giây
2. F5 refresh page
3. Check: `docker logs jupyter-notebook`

---

## 📊 Kiểm Tra Cluster Status

**Từ Web Browser:**

| Service | URL | Mục Đích |
|---------|-----|---------|
| **Hadoop NameNode** | http://127.0.0.1:9870 | Xem HDFS status |
| **YARN ResourceManager** | http://127.0.0.1:8088 | Xem jobs |
| **Spark Master UI** | http://127.0.0.1:8080 | Xem Spark apps |
| **Jupyter Notebook** | http://127.0.0.1:8888 | Chạy notebooks |

---

## ✅ Xác Nhận Thành Công

Khi Cell 3 chạy xong, bạn sẽ thấy:
```
✓ SparkSession created successfully in LOCAL mode!

Session Details:
  Spark version: 3.5.0
  Master: local[2]
  App Name: Hadoop-Spark-Test
  Default Parallelism: 2
```

→ Lúc đó có thể chạy các cells tiếp theo để test HDFS, DataFrame, SQL, v.v.

---

## 💡 Ghi Chú Quan Trọng

1. **Local Mode vs Cluster Mode**
   - Cell 3 sử dụng `local[2]` (chạy trên Jupyter container)
   - Có thể thay bằng `yarn` sau để submit tới Spark cluster
   - Cả hai modes đều có thể access HDFS

2. **Data Persistence**
   - Notebooks được lưu trong Docker volume
   - Thay đổi sẽ được giữ lại

3. **Performance**
   - Local mode: nhanh, dùng cho testing
   - YARN mode: dùng cho production, submit tới cluster

---

## 🆘 Cần Trợ Giúp?

Nếu vẫn gặp vấn đề, chạy lệnh này để debug:
```bash
docker exec jupyter-notebook python -c "
import os, sys
sys.path.insert(0, '/opt/spark/python')
from pyspark.sql import SparkSession
spark = SparkSession.builder.master('local[2]').getOrCreate()
print('SUCCESS')
"
```

Nếu output là `SUCCESS` → Jupyter container OK
Nếu error → Check Docker logs: `docker logs jupyter-notebook`
