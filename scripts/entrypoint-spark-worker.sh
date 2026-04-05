#!/bin/bash

# Entrypoint script for Spark Worker container

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

# Wait for Spark master to be ready (simplified - just sleep)
echo "Waiting for Spark cluster to initialize..."
sleep 20

# Start Spark Worker in background
WORKER_NAME=$(hostname)
echo "Starting Spark Worker: $WORKER_NAME"
$SPARK_HOME/sbin/start-worker.sh spark://spark-master:7077 -h $WORKER_NAME -p 7078 --webui-port 8081 -m 1G -c 2 2>&1 | tee -a /var/log/spark-worker.log &

# Keep container running indefinitely
echo "Spark Worker started, keeping container alive..."
while true; do
  sleep 60
  # Check if any java process is still running
  if ! pgrep -f "spark.deploy.worker.Worker" > /dev/null 2>&1; then
    echo "Warning: Spark Worker process not found, restarting..."
    $SPARK_HOME/sbin/start-worker.sh spark://spark-master:7077 -h $WORKER_NAME -p 7078 --webui-port 8081 -m 1G -c 2 2>&1 | tee -a /var/log/spark-worker.log &
  fi
done
