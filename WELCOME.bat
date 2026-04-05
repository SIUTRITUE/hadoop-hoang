@echo off
REM Welcome screen for Hadoop-Spark Cluster

setlocal enabledelayedexpansion

cls
echo.
echo ============================================================
echo    HADOOP-SPARK CLUSTER ON DOCKER COMPOSE (WINDOWS)
echo ============================================================
echo.
echo Welcome to the Hadoop-Spark Big Data Platform!
echo.
echo This system includes:
echo   - Hadoop 3.3.6 with 1 Master + 2 Workers
echo   - Spark 3.5.0 with 1 Master + 2 Workers
echo   - Jupyter Notebook with PySpark
echo   - HDFS, YARN, and complete Big Data stack
echo.
echo ============================================================
echo.

REM Check Docker
echo Checking Docker installation...
docker --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Docker is not installed or not in PATH
    echo Please install Docker Desktop from https://www.docker.com/products/docker-desktop
    pause
    exit /b 1
)

echo Docker found: OK
echo.

REM Check Docker Compose
echo Checking Docker Compose...
docker-compose --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Docker Compose not found
    pause
    exit /b 1
)

echo Docker Compose found: OK
echo.

REM Check Docker daemon
echo Checking Docker daemon...
docker info >nul 2>&1
if errorlevel 1 (
    echo WARNING: Docker daemon is not running
    echo Please start Docker Desktop and try again
    pause
    exit /b 1
)

echo Docker daemon running: OK
echo.

REM Show next steps
echo ============================================================
echo NEXT STEPS:
echo ============================================================
echo.
echo 1. START CLUSTER:
echo    Double-click: start-cluster.bat
echo    Or run: docker-compose up -d
echo.
echo 2. WAIT FOR SERVICES (5-10 minutes first time):
echo    - Hadoop NameNode
echo    - YARN ResourceManager
echo    - Spark Master
echo    - Jupyter Notebook
echo.
echo 3. OPEN WEB UIs IN BROWSER:
echo    - Hadoop NameNode: http://localhost:9870
echo    - YARN ResourceManager: http://localhost:8088
echo    - Spark Master: http://localhost:8080
echo    - Spark Worker 1: http://localhost:8081
echo    - Spark Worker 2: http://localhost:8082
echo    - Jupyter Notebook: http://localhost:8888
echo.
echo 4. JUPYTER PASSWORD:
echo    Copy token from: docker logs jupyter-notebook
echo    Or access without password (auto-login when opened)
echo.
echo 5. RUN EXAMPLES:
echo    - See notebooks/ folder
echo    - 01-Test-Connection.ipynb: Basic connectivity test
echo    - 02-WordCount-Example.ipynb: MapReduce example
echo    - 03-Data-Processing-Pipeline.ipynb: Complex pipeline
echo.
echo 6. STOP CLUSTER:
echo    Double-click: stop-cluster.bat
echo    Or run: docker-compose down
echo.
echo ============================================================
echo.
echo QUICK COMMANDS:
echo   docker-compose ps              - Show container status
echo   docker-compose logs             - View logs
echo   docker exec -it hadoop-master bash  - SSH into Hadoop Master
echo   docker exec -it spark-master bash   - SSH into Spark Master
echo   docker exec -it jupyter-notebook bash - SSH into Jupyter
echo.
echo FULL DOCUMENTATION:
echo   - README.md: Complete documentation
echo   - QUICKSTART.md: Quick reference guide
echo.
echo ============================================================
echo.
echo Press any key to continue...
pause

cls
