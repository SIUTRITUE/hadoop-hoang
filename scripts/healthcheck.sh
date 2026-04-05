#!/bin/bash

# Healthcheck script for Hadoop services

# Check HDFS NameNode
if [ "$SERVICE" == "hadoop-master" ]; then
    # Check if namenode is running and responsive
    curl -f http://localhost:9870 || exit 1
    
    # Check if HDFS is accessible
    hdfs dfs -ls / >/dev/null 2>&1 || exit 1
    
    # Check YARN ResourceManager
    curl -f http://localhost:8088 || exit 1
    
    exit 0
fi

# Check HDFS DataNode
if [ "$SERVICE" == "hadoop-worker" ]; then
    # Check if datanode is running
    curl -f http://localhost:9864 || exit 1
    
    # Check if nodemanager is running
    curl -f http://localhost:8042 || exit 1
    
    exit 0
fi

# Check Spark Master
if [ "$SERVICE" == "spark-master" ]; then
    # Check if spark master is running
    curl -f http://localhost:8080 || exit 1
    
    exit 0
fi

# Check Spark Worker
if [ "$SERVICE" == "spark-worker" ]; then
    # Check if spark worker is running
    curl -f http://localhost:8081 || exit 1
    
    exit 0
fi

exit 0
