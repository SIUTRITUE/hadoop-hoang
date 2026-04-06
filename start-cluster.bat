@echo off
REM Startup script for Hadoop-Spark cluster on Windows
REM Run this script to start the entire cluster

setlocal enabledelayedexpansion

set SCRIPT_DIR=%~dp0
cd /d "%SCRIPT_DIR%"

echo.
echo ============================================
echo Hadoop-Spark Cluster Startup Script
echo ============================================
echo.

REM Check if Docker is running
echo Checking Docker daemon...
docker info >nul 2>&1
if errorlevel 1 (
    echo ERROR: Docker daemon is not running
    echo Please start Docker Desktop and try again
    pause
    exit /b 1
)

echo Docker is running. Proceeding...
echo.

REM Pull required images
echo Pulling base images...
docker pull ubuntu:22.04
docker pull jupyter/pyspark-notebook:latest

echo.
echo Building Docker images...
docker-compose build --no-cache

echo.
echo.
echo ============================================
echo Starting Hadoop-Spark Cluster
echo ============================================
echo.

REM Start services
docker-compose up -d

echo.
echo Services are starting. Waiting for them to be ready...
echo.

REM Wait for services to be healthy
echo Waiting for Hadoop Master...
timeout /t 10 /nobreak

for /L %%i in (1,1,30) do (
    docker exec hadoop-master curl -s http://localhost:9870 >nul 2>&1
    if !errorlevel! equ 0 (
        echo Hadoop Master is ready!
        goto hadoop_ready
    )
    echo Attempt %%i/30: Waiting for Hadoop Master...
    timeout /t 2 /nobreak
)

:hadoop_ready
echo Waiting for Spark Master...
timeout /t 5 /nobreak

for /L %%i in (1,1,30) do (
    docker exec spark-master curl -s http://localhost:8080 >nul 2>&1
    if !errorlevel! equ 0 (
        echo Spark Master is ready!
        goto spark_ready
    )
    echo Attempt %%i/30: Waiting for Spark Master...
    timeout /t 2 /nobreak
)

:spark_ready
echo Waiting for Jupyter...
timeout /t 5 /nobreak

for /L %%i in (1,1,30) do (
    docker exec jupyter-notebook curl -s http://localhost:8888/lab >nul 2>&1
    if !errorlevel! equ 0 (
        echo Jupyter is ready!
        goto jupyter_ready
    )
    echo Attempt %%i/30: Waiting for Jupyter...
    timeout /t 2 /nobreak
)

:jupyter_ready
echo Waiting for Streamlit...
timeout /t 5 /nobreak

for /L %%i in (1,1,30) do (
    docker exec streamlit-app curl -s http://localhost:8501 >nul 2>&1
    if !errorlevel! equ 0 (
        echo Streamlit is ready!
        goto streamlit_ready
    )
    echo Attempt %%i/30: Waiting for Streamlit...
    timeout /t 2 /nobreak
)

:streamlit_ready
echo.
echo ============================================
echo Cluster Startup Completed!
echo ============================================
echo.
echo Web UIs:
echo  - Hadoop NameNode: http://localhost:9870
echo  - YARN ResourceManager: http://localhost:8088
echo  - Spark Master: http://localhost:8080
echo  - Spark Worker 1: http://localhost:8081
echo  - Spark Worker 2: http://localhost:8082
echo  - Jupyter Notebook: http://localhost:8888
echo  - Streamlit Dashboard: http://localhost:8501
echo.
echo Useful Commands:
echo  - View logs: docker-compose logs -f
echo  - Stop cluster: docker-compose down
echo  - Bash into Hadoop Master: docker exec -it hadoop-master bash
echo  - Bash into Jupyter: docker exec -it jupyter-notebook bash
echo  - List HDFS files: docker exec hadoop-master hdfs dfs -ls /
echo.
pause
