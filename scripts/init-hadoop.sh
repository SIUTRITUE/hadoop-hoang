#!/bin/bash

# Script to format namenode and start Hadoop cluster
# Should be run once before starting the cluster

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${YELLOW}Hadoop Cluster Initialization Script${NC}"
echo "========================================="

# Check if HADOOP_HOME is set
if [ -z "$HADOOP_HOME" ]; then
    echo -e "${RED}Error: HADOOP_HOME is not set${NC}"
    exit 1
fi

# Check if we need to format namenode
if [ "$1" == "format" ]; then
    echo -e "${YELLOW}Formatting namenode...${NC}"
    $HADOOP_HOME/bin/hdfs namenode -format -force
    echo -e "${GREEN}Namenode formatted successfully${NC}"
fi

# Wait for Hadoop master to be ready
echo -e "${YELLOW}Waiting for Hadoop master to be ready...${NC}"
for i in {1..30}; do
    if $HADOOP_HOME/bin/hdfs dfs -ls / >/dev/null 2>&1; then
        echo -e "${GREEN}Hadoop master is ready${NC}"
        break
    fi
    echo "Attempt $i/30: Waiting for HDFS..."
    sleep 2
done

# Create necessary directories in HDFS
echo -e "${YELLOW}Creating HDFS directories...${NC}"

$HADOOP_HOME/bin/hdfs dfs -mkdir -p /user/hadoop/input 2>/dev/null || true
$HADOOP_HOME/bin/hdfs dfs -mkdir -p /user/hadoop/output 2>/dev/null || true
$HADOOP_HOME/bin/hdfs dfs -mkdir -p /spark-logs 2>/dev/null || true
$HADOOP_HOME/bin/hdfs dfs -mkdir -p /tmp 2>/dev/null || true
$HADOOP_HOME/bin/hdfs dfs -mkdir -p /user/jupyter 2>/dev/null || true

echo -e "${GREEN}HDFS directories created${NC}"

# Set permissions
$HADOOP_HOME/bin/hdfs dfs -chmod -R 777 / 2>/dev/null || true

echo -e "${GREEN}Hadoop cluster initialization completed successfully${NC}"
