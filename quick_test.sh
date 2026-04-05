#!/bin/bash
cd /tmp
python3 << 'EOF'
import os
import sys

os.environ['JAVA_HOME'] = '/usr/lib/jvm/java-17-openjdk-amd64'
os.environ['SPARK_HOME'] = '/opt/spark'
os.environ['HADOOP_HOME'] = '/opt/hadoop'
os.environ['HADOOP_CONF_DIR'] = '/opt/hadoop/etc/hadoop'
os.environ['YARN_CONF_DIR'] = '/opt/hadoop/etc/hadoop'
os.environ['LD_LIBRARY_PATH'] = '/opt/hadoop/lib/native'

sys.path.insert(0, '/opt/spark/python')
sys.path.insert(0, '/opt/spark/python/lib/py4j-0.10.9.7-src.zip')

print("Starting Spark test...")
from pyspark.sql import SparkSession

print("Creating SparkSession in LOCAL mode...")
spark = SparkSession.builder \
    .appName("Test") \
    .master("local[2]") \
    .config("spark.hadoop.fs.defaultFS", "hdfs://hadoop-master:9000") \
    .getOrCreate()

print("✓ SparkSession created!")
print(f"Master: {spark.sparkContext.master}")
spark.stop()
print("✓ Done!")
EOF
