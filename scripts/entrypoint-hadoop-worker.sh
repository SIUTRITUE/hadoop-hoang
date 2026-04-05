#!/bin/bash

# Entrypoint script for Hadoop Worker container

HADOOP_HOME=/opt/hadoop
JAVA_HOME=/usr/lib/jvm/java-11-openjdk-amd64

# Export environment variables
export HADOOP_HOME JAVA_HOME
export PATH=$JAVA_HOME/bin:$HADOOP_HOME/bin:$HADOOP_HOME/sbin:$PATH

# Create necessary directories
mkdir -p /data/namenode /data/datanode /data/tmp
mkdir -p /data/tmp/nm-local-dir /data/tmp/nm-logs

# Create necessary directories with proper permissions
echo "Creating HDFS directories..."
mkdir -p /data/namenode /data/datanode /data/tmp
mkdir -p /data/tmp/nm-local-dir /data/tmp/nm-logs
chmod -R 777 /data 2>/dev/null || true
chown -R hadoop:hadoop /data 2>/dev/null || true

# Copy configuration files
echo "Copying Hadoop configuration files..."
cp /config/core-site.xml $HADOOP_HOME/etc/hadoop/
cp /config/hdfs-site.xml $HADOOP_HOME/etc/hadoop/
cp /config/yarn-site.xml $HADOOP_HOME/etc/hadoop/
cp /config/hdfs-site.xml $HADOOP_HOME/etc/hadoop/
cp /config/yarn-site.xml $HADOOP_HOME/etc/hadoop/

# Add mapred-site.xml if not exists
if [ ! -f "$HADOOP_HOME/etc/hadoop/mapred-site.xml" ]; then
    echo "Creating mapred-site.xml..."
    cp $HADOOP_HOME/etc/hadoop/mapred-site.xml.template $HADOOP_HOME/etc/hadoop/mapred-site.xml 2>/dev/null || cat > $HADOOP_HOME/etc/hadoop/mapred-site.xml <<EOF
<?xml version="1.0" encoding="UTF-8"?>
<?xml-stylesheet type="text/xsl" href="configuration.xsl"?>
<configuration>
    <property>
        <name>mapreduce.framework.name</name>
        <value>yarn</value>
    </property>
    <property>
        <name>mapreduce.map.memory.mb</name>
        <value>512</value>
    </property>
    <property>
        <name>mapreduce.reduce.memory.mb</name>
        <value>512</value>
    </property>
</configuration>
EOF
fi

# Generate SSH key if not exists
if [ ! -f /home/hadoop/.ssh/id_rsa ]; then
    echo "Generating SSH key..."
    ssh-keygen -t rsa -f /home/hadoop/.ssh/id_rsa -N "" -C "hadoop@worker"
    cat /home/hadoop/.ssh/id_rsa.pub >> /home/hadoop/.ssh/authorized_keys
    chmod 600 /home/hadoop/.ssh/authorized_keys
fi

# Start SSH service
echo "Starting SSH service..."
service ssh start || true

# Wait for Hadoop cluster to initialize...
echo "Waiting for Hadoop cluster to initialize..."
sleep 25

# Ensure datanode directory has proper permissions for Docker volumes
echo "Preparing datanode directory..."
mkdir -p /data/datanode /data/tmp/nm-local-dir /data/tmp/nm-logs

# Start HDFS DataNode in background with retry logic
echo "Starting HDFS DataNode..."
for attempt in 1 2 3; do
    echo "DataNode startup attempt $attempt/3..."
    hdfs datanode &
    DATANODE_PID=$!
    
    # Wait a bit to see if it stays running
    sleep 3
    if ! kill -0 $DATANODE_PID 2>/dev/null; then
        echo "DataNode exited unexpectedly on attempt $attempt"
        wait $DATANODE_PID || true
    else
        echo "DataNode successfully started"
        break
    fi
done

# Start YARN NodeManager in background
echo "Starting YARN NodeManager..."
yarn nodemanager &
NODEMANAGER_PID=$!

# Keep container running and wait for services
echo "Services started, keeping container alive..."
wait $DATANODE_PID $NODEMANAGER_PID || true
