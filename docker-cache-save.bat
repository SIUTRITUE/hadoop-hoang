@echo off
REM Save Docker images to tar files for caching
REM This way we don't need to rebuild/retag every time

echo.
echo ========================================
echo SAVING DOCKER IMAGES TO CACHE
echo ========================================
echo.

REM Create cache directory
if not exist "docker-cache" mkdir docker-cache

echo [1/7] Saving Hadoop Master image...
docker save hadoop-hoang-hadoop-master > docker-cache\hadoop-master.tar
if %errorlevel% equ 0 (echo ✓ Saved hadoop-master.tar) else (echo ✗ Failed to save hadoop-master)

echo [2/7] Saving Hadoop Worker image...
docker save 74c5c3e261ae > docker-cache\hadoop-worker.tar
if %errorlevel% equ 0 (echo ✓ Saved hadoop-worker.tar) else (echo ✗ Failed to save hadoop-worker)

echo [3/7] Saving Spark Master image...
docker save hadoop-hoang-spark-master > docker-cache\spark-master.tar
if %errorlevel% equ 0 (echo ✓ Saved spark-master.tar) else (echo ✗ Failed to save spark-master)

echo [4/7] Saving Spark Worker image...
docker save hadoop-hoang-spark-worker-1 > docker-cache\spark-worker-1.tar
if %errorlevel% equ 0 (echo ✓ Saved spark-worker-1.tar) else (echo ✗ Failed to save spark-worker-1)

echo [5/7] Saving Jupyter image (Python 3.10)...
docker save hadoop-hoang-jupyter > docker-cache\jupyter-python310.tar
if %errorlevel% equ 0 (echo ✓ Saved jupyter-python310.tar) else (echo ✗ Failed to save jupyter)

echo.
echo ========================================
echo CACHE SAVED TO: docker-cache\
echo ========================================
echo.
echo Next time, use: docker-cache-load.bat
echo.
