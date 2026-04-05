#!/usr/bin/env python3
"""
Test script to verify Spark cluster connection from Jupyter container
This script will be executed inside the Jupyter Docker container
"""

import os
import sys

# Set environment variables
os.environ['JAVA_HOME'] = '/usr/lib/jvm/java-17-openjdk-amd64'
os.environ['SPARK_HOME'] = '/opt/spark'
os.environ['HADOOP_HOME'] = '/opt/hadoop'
os.environ['HADOOP_CONF_DIR'] = '/opt/hadoop/etc/hadoop'
os.environ['YARN_CONF_DIR'] = '/opt/hadoop/etc/hadoop'
os.environ['LD_LIBRARY_PATH'] = '/opt/hadoop/lib/native'
os.environ['PYSPARK_PYTHON'] = '/usr/bin/python3'
os.environ['PYSPARK_DRIVER_PYTHON'] = '/usr/bin/python3'

# Add Spark to Python path
sys.path.insert(0, '/opt/spark/python')
sys.path.insert(0, '/opt/spark/python/lib/py4j-0.10.9.7-src.zip')

print("=" * 80)
print("SPARK CLUSTER CONNECTION TEST")
print("=" * 80)
print()

# Step 1: Check environment
print("1. Checking environment:")
print(f"   JAVA_HOME: {os.environ.get('JAVA_HOME')}")
print(f"   SPARK_HOME: {os.environ.get('SPARK_HOME')}")
print(f"   HADOOP_HOME: {os.environ.get('HADOOP_HOME')}")
print()

# Step 2: Test Java
print("2. Testing Java availability:")
import subprocess
result = subprocess.run(['java', '-version'], capture_output=True, text=True)
java_version = result.stderr.split('\n')[0] if result.stderr else "Unknown"
print(f"   {java_version}")
print()

# Step 3: Import PySpark
print("3. Importing PySpark...")
try:
    from pyspark.sql import SparkSession
    print("   ✓ PySpark imported successfully")
except ImportError as e:
    print(f"   ✗ Failed to import PySpark: {e}")
    sys.exit(1)
print()

# Step 4: Create SparkSession with YARN
print("4. Creating SparkSession with YARN ResourceManager...")
print("   " + "=" * 70)

try:
    spark = SparkSession.builder \
        .appName("Hadoop-Spark-Cluster-Test") \
        .master("local[2]") \
        .config("spark.executor.memory", "512m") \
        .config("spark.executor.cores", "1") \
        .config("spark.driver.memory", "512m") \
        .config("spark.hadoop.fs.defaultFS", "hdfs://hadoop-master:9000") \
        .config("spark.yarn.resourcemanager.hostname", "hadoop-master") \
        .config("spark.yarn.resourcemanager.address", "hadoop-master:8032") \
        .config("spark.sql.shuffle.partitions", "4") \
        .config("spark.network.timeout", "300") \
        .getOrCreate()
    
    print("   ✓ SparkSession created successfully!")
    print()
    print("5. SparkSession Details:")
    print(f"   Spark version: {spark.version}")
    print(f"   Master: {spark.sparkContext.master}")
    print(f"   App Name: {spark.sparkContext.appName}")
    print(f"   Deploy Mode: {spark.sparkContext._conf.get('spark.submit.deployMode')}")
    print()
    
    # Step 5: Test DataFrame creation
    print("6. Testing DataFrame creation...")
    data = [("Alice", 25), ("Bob", 30), ("Charlie", 35)]
    df = spark.createDataFrame(data, ["Name", "Age"])
    print("   ✓ DataFrame created successfully")
    print()
    print("   Sample data:")
    df.show()
    print()
    
    # Step 6: Stop session
    print("7. Stopping SparkSession...")
    spark.stop()
    print("   ✓ SparkSession stopped successfully")
    print()
    print("=" * 80)
    print("✓ ALL TESTS PASSED!")
    print("=" * 80)
    
except Exception as e:
    print(f"   ✗ ERROR: {e}")
    print()
    import traceback
    traceback.print_exc()
    print()
    print("=" * 80)
    print("✗ TEST FAILED")
    print("=" * 80)
    sys.exit(1)
