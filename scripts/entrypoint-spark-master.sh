#!/bin/bash

# Entrypoint script for Spark Master container

SPARK_HOME=/opt/spark
HADOOP_HOME=/opt/hadoop
JAVA_HOME=/usr/lib/jvm/java-11-openjdk-amd64

# Export environment variables
export SPARK_HOME HADOOP_HOME JAVA_HOME
export PATH=$JAVA_HOME/bin:$SPARK_HOME/bin:$HADOOP_HOME/bin:$PATH
export LD_LIBRARY_PATH=$HADOOP_HOME/lib/native:$LD_LIBRARY_PATH

# Copy Spark configuration
echo "Copying Spark configuration files..."
mkdir -p $SPARK_HOME/conf
cp /config/spark-defaults.conf $SPARK_HOME/conf/

# Wait for Hadoop cluster to initialize (simplified - just sleep)
echo "Waiting for Hadoop cluster to initialize..."
sleep 30

# Start Spark Master in background
echo "Starting Spark Master..."
$SPARK_HOME/sbin/start-master.sh -h spark-master -p 7077 --webui-port 8080 2>&1 | tee -a /var/log/spark-master.log &

# Keep container running indefinitely
echo "Spark Master started, keeping container alive..."
while true; do
  sleep 60
  # Check if any java process is still running
  if ! pgrep -f "spark.deploy.master.Master" > /dev/null 2>&1; then
    echo "Warning: Spark Master process not found, restarting..."
    $SPARK_HOME/sbin/start-master.sh -h spark-master -p 7077 --webui-port 8080 2>&1 | tee -a /var/log/spark-master.log &
  fi
done
