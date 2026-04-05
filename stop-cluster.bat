@echo off
REM Stop script for Hadoop-Spark cluster

setlocal enabledelayedexpansion

set SCRIPT_DIR=%~dp0
cd /d "%SCRIPT_DIR%"

echo.
echo ============================================
echo Stopping Hadoop-Spark Cluster
echo ============================================
echo.

docker-compose down

echo.
echo Cluster stopped successfully
echo.
echo To start again, run: start-cluster.bat
echo.
pause
