import json
import os

notebook = {
    "cells": [
        {
            "cell_type": "markdown",
            "metadata": {},
            "source": ["# LAB 5 - CÂU 2: Hive Analysis\n", "Phân tích doanh thu theo productType"]
        },
        {
            "cell_type": "code",
            "execution_count": None,
            "metadata": {},
            "outputs": [],
            "source": [
                "from pyspark.sql import SparkSession\n",
                "\n",
                "spark = SparkSession.builder.appName('LAB5-CAU2').master('spark://spark-master:7077').config('spark.hadoop.fs.defaultFS', 'hdfs://hadoop-master:9000').getOrCreate()\n",
                "print('Spark Session created!')"
            ]
        },
        {
            "cell_type": "code",
            "execution_count": None,
            "metadata": {},
            "outputs": [],
            "source": [
                "df = spark.read.csv('/home/jovyan/work/shop_transactions.csv', header=True, inferSchema=True)\n",
                "print(f'Data loaded: {df.count():,} rows')\n",
                "df.show(3)"
            ]
        },
        {
            "cell_type": "code",
            "execution_count": None,
            "metadata": {},
            "outputs": [],
            "source": [
                "from pyspark.sql.functions import col\n",
                "\n",
                "df = df.withColumn('revenue', col('price') * col('quantity'))\n",
                "df.createOrReplaceTempView('shop_transactions')\n",
                "print('Temp view created')"
            ]
        },
        {
            "cell_type": "code",
            "execution_count": None,
            "metadata": {},
            "outputs": [],
            "source": [
                "result = spark.sql('''SELECT productType, COUNT(*) as cnt, ROUND(AVG(price), 2) as avg_price, ROUND(SUM(price * quantity), 2) as total_revenue FROM shop_transactions GROUP BY productType ORDER BY total_revenue DESC''')\n",
                "result.show()"
            ]
        },
        {
            "cell_type": "code",
            "execution_count": None,
            "metadata": {},
            "outputs": [],
            "source": [
                "spark.sql('SELECT productType, ROUND(SUM(price * quantity), 2) as revenue, COUNT(*) as cnt FROM shop_transactions GROUP BY productType ORDER BY revenue DESC LIMIT 5').show()"
            ]
        }
    ],
    "metadata": {
        "kernelspec": {"display_name": "Python 3", "language": "python", "name": "python3"},
        "language_info": {"name": "python", "version": "3.8.0"}
    },
    "nbformat": 4,
    "nbformat_minor": 4
}

# Lưu lên Windows
windows_path = r'd:\BIGDATA\Hoang\hadoop-hoang\notebooks\LAB5_CAU2_Simple.ipynb'
with open(windows_path, 'w', encoding='utf-8') as f:
    json.dump(notebook, f, indent=1, ensure_ascii=False)

print(f'Created: {windows_path}')
print(f'Size: {os.path.getsize(windows_path)} bytes')
