# Streamlit Dashboard - LAB 5

Interactive dashboard for Big Data Analysis using Streamlit.

## Features

### 📈 CÂU 2: Hive Analysis Tab
- Top 5 Products by Revenue
- Revenue Distribution by Region
- All Products Statistics
- Interactive Plotly charts

### 🤖 CÂU 3: ML Model Tab
- Logistic Regression Performance Metrics
- Model Evaluation Results
- Feature Information

### 📊 Data Exploration Tab
- Dataset Statistics (Total Rows, Total Revenue, Avg Price, Avg Quantity)
- Price Distribution
- Quantity Distribution
- Data Preview (first 100 rows)

### ℹ️ Info Tab
- Project Information
- Dataset Details
- Technologies Used

## Usage

### Local Development
```bash
pip install streamlit pyspark pandas plotly matplotlib

streamlit run app.py
```

### Docker
```bash
docker-compose up streamlit
```

Access at: http://localhost:8501

## Data Source

- **Local File**: `/home/jovyan/work/shop_transactions.csv`
- **HDFS**: `hdfs://hadoop-master:9000/shop_transactions.csv`

Switch between them in the sidebar.

## Features Used

- **Streamlit** for interactive dashboard
- **Plotly** for interactive visualizations
- **PySpark** for data processing
- **Pandas** for data manipulation
- **Caching** for performance optimization

## File Structure

```
streamlit/
├── app.py                 # Main Streamlit application
└── README.md             # This file
```

## Performance Tips

1. Data is cached using `@st.cache_data` to avoid recomputation
2. Spark session is cached using `@st.cache_resource`
3. Charts use Plotly for interactive visualization
4. Local mode is used for Spark to avoid cluster overhead

## Troubleshooting

**Issue**: "ModuleNotFoundError: No module named 'streamlit'"
- **Solution**: Install streamlit: `pip install streamlit`

**Issue**: Cannot connect to Spark
- **Solution**: Check if Spark Master is running at `spark://spark-master:7077`

**Issue**: Cannot load data from HDFS
- **Solution**: Check if Hadoop is running and file exists: `hadoop fs -ls /shop_transactions.csv`

## Author
SIUTRITUE

## Repository
https://github.com/SIUTRITUE/Hadoop
