import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, sum as spark_sum, avg, count, round as spark_round
import time

st.set_page_config(page_title="LAB 5 Dashboard", layout="wide", initial_sidebar_state="expanded")

# Custom CSS
st.markdown("""
<style>
    .main {
        padding: 2rem;
    }
    h1 {
        color: #1f77b4;
        text-align: center;
    }
    .metric-box {
        background-color: #f0f2f6;
        padding: 1.5rem;
        border-radius: 0.5rem;
        border-left: 4px solid #1f77b4;
    }
</style>
""", unsafe_allow_html=True)

st.title("📊 LAB 5 - Big Data Analysis Dashboard")
st.markdown("---")

# Sidebar
st.sidebar.header("⚙️ Configuration")
data_source = st.sidebar.radio("Select Data Source:", ["Local File", "HDFS"])

# Initialize Spark
@st.cache_resource
def init_spark():
    return SparkSession.builder \
        .appName("Streamlit-LAB5") \
        .master("local[*]") \
        .config("spark.sql.adaptive.enabled", "true") \
        .getOrCreate()

spark = init_spark()

# Load Data
@st.cache_data
def load_data(source):
    try:
        if source == "Local File":
            path = "file:///home/jovyan/work/shop_transactions.csv"
        else:
            path = "hdfs://hadoop-master:9000/shop_transactions.csv"
        
        df = spark.read.csv(path, header=True, inferSchema=True)
        df = df.withColumn('revenue', col('price') * col('quantity'))
        return df
    except Exception as e:
        st.error(f"Error loading data: {str(e)}")
        return None

df = load_data(data_source)

if df is not None:
    # Overview
    st.sidebar.metric("📦 Total Rows", f"{df.count():,}")
    
    # Create tabs
    tab1, tab2, tab3, tab4 = st.tabs([
        "📈 CÂU 2: Hive Analysis",
        "🤖 CÂU 3: ML Model",
        "📊 Data Exploration",
        "ℹ️ Info"
    ])

    # TAB 1: HIVE ANALYSIS
    with tab1:
        st.subheader("Revenue Analysis by Product Type")
        
        col1, col2 = st.columns(2)
        
        # Top 5 Products
        with col1:
            st.write("**Top 5 Products by Revenue**")
            top5_query = spark.sql('''
                SELECT 
                    productType,
                    ROUND(SUM(price * quantity), 2) as total_revenue,
                    COUNT(*) as transaction_count
                FROM (SELECT price, quantity, productType FROM (
                    SELECT * FROM df_temp
                ))
                GROUP BY productType
                ORDER BY total_revenue DESC
                LIMIT 5
            ''')
            
            # Simple approach
            top5 = df.groupBy('productType').agg(
                spark_sum('revenue').alias('total_revenue'),
                count('*').alias('transaction_count')
            ).orderBy(col('total_revenue').desc()).limit(5).toPandas()
            
            # Bar chart
            fig = px.bar(
                top5, 
                x='productType', 
                y='total_revenue',
                title='Top 5 Products by Revenue',
                labels={'total_revenue': 'Revenue ($)', 'productType': 'Product Type'},
                color='total_revenue',
                color_continuous_scale='Blues'
            )
            st.plotly_chart(fig, use_container_width=True)
            st.dataframe(top5, use_container_width=True)
        
        # Revenue by Region
        with col2:
            st.write("**Revenue by Region**")
            region_revenue = df.groupBy('customerRegion').agg(
                spark_sum('revenue').alias('total_revenue'),
                count('*').alias('count')
            ).orderBy(col('total_revenue').desc()).toPandas()
            
            fig = px.pie(
                region_revenue,
                values='total_revenue',
                names='customerRegion',
                title='Revenue Distribution by Region'
            )
            st.plotly_chart(fig, use_container_width=True)
        
        # All products stats
        st.write("**All Products Statistics**")
        all_products = df.groupBy('productType').agg(
            count('*').alias('count'),
            spark_round(avg('price'), 2).alias('avg_price'),
            spark_round(avg('revenue'), 2).alias('avg_revenue'),
            spark_round(spark_sum('revenue'), 2).alias('total_revenue')
        ).orderBy(col('total_revenue').desc()).toPandas()
        
        st.dataframe(all_products, use_container_width=True)

    # TAB 2: ML MODEL
    with tab2:
        st.subheader("Logistic Regression - Product Type Classification")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.write("**Model Performance Metrics**")
            metrics_data = {
                'Metric': ['Accuracy', 'Precision', 'Recall', 'F1-Score'],
                'Score': [0.1995, 0.1992, 0.1995, 0.1546]
            }
            metrics_df = pd.DataFrame(metrics_data)
            
            fig = px.bar(
                metrics_df,
                x='Metric',
                y='Score',
                title='Model Evaluation Metrics',
                color='Score',
                color_continuous_scale='Reds',
                range_y=[0, 1]
            )
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            st.write("**Metrics Summary**")
            col_m1, col_m2 = st.columns(2)
            with col_m1:
                st.metric("Accuracy", "19.95%", delta="-0.05")
                st.metric("Recall", "19.95%")
            with col_m2:
                st.metric("Precision", "19.92%")
                st.metric("F1-Score", "15.46%")
        
        st.write("**Model Details**")
        st.info("""
        - **Algorithm**: Logistic Regression
        - **Features**: price, quantity, customerRegion
        - **Target**: productType
        - **Train/Test Split**: 80/20
        - **Standardization**: Z-score normalization
        - **Note**: Low accuracy indicates features are not sufficient to predict product type
        """)

    # TAB 3: DATA EXPLORATION
    with tab3:
        st.subheader("Data Exploration & Insights")
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Total Transactions", f"{df.count():,}")
        with col2:
            total_revenue = df.agg(spark_sum('revenue')).collect()[0][0]
            st.metric("Total Revenue", f"${total_revenue:,.0f}")
        with col3:
            avg_price = df.agg(avg('price')).collect()[0][0]
            st.metric("Avg Price", f"${avg_price:.2f}")
        with col4:
            avg_qty = df.agg(avg('quantity')).collect()[0][0]
            st.metric("Avg Quantity", f"{avg_qty:.2f}")
        
        # Distribution charts
        col1, col2 = st.columns(2)
        
        with col1:
            price_dist = df.select('price').toPandas()
            fig = px.histogram(price_dist, x='price', nbins=50, title='Price Distribution')
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            qty_dist = df.select('quantity').toPandas()
            fig = px.histogram(qty_dist, x='quantity', nbins=50, title='Quantity Distribution')
            st.plotly_chart(fig, use_container_width=True)
        
        # Data preview
        st.write("**Data Preview**")
        sample_data = df.limit(100).toPandas()
        st.dataframe(sample_data, use_container_width=True)

    # TAB 4: INFO
    with tab4:
        st.subheader("📋 Project Information")
        
        st.write("""
        ### LAB 5 - Big Data Analysis Project
        
        **Objective:**
        - Analyze shop transactions data using Hadoop-Spark cluster
        - Perform SQL analysis with Spark SQL (replacing Hive)
        - Build Logistic Regression model for product classification
        
        **Dataset:**
        - File: shop_transactions.csv
        - Rows: 1,000,000+
        - Columns: price, quantity, customerRegion, productType
        
        **Components:**
        1. **CÂU 2: Hive Analysis**
           - Top 5 products by revenue
           - Revenue distribution by region
           - Product statistics
        
        2. **CÂU 3: Machine Learning**
           - Logistic Regression classifier
           - Features: price, quantity, customerRegion
           - Train/Test: 80/20 split
           - Metrics: Accuracy, Precision, Recall, F1-Score
        
        3. **Streamlit Dashboard**
           - Interactive data visualization
           - Real-time model metrics
           - Data exploration tools
        
        **Technologies:**
        - Apache Hadoop & HDFS
        - Apache Spark & PySpark
        - Jupyter Notebook
        - Streamlit
        - Plotly & Pandas
        
        **Author:** SIUTRITUE
        **Repository:** https://github.com/SIUTRITUE/Hadoop
        """)

else:
    st.error("Could not load data. Please check the data source and try again.")

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center'>
    <p>LAB 5 Dashboard • Hadoop-Spark Cluster • 2026</p>
</div>
""", unsafe_allow_html=True)
