import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from pyspark.sql import SparkSession
import warnings
warnings.filterwarnings('ignore')

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
st.sidebar.info("📁 Data Source: HDFS (hdfs://hadoop-master:9000/shop_transactions.csv)")

# Initialize Spark
@st.cache_resource
def init_spark():
    return SparkSession.builder \
        .appName("Streamlit-LAB5") \
        .master("local[*]") \
        .config("spark.sql.adaptive.enabled", "false") \
        .config("spark.sql.execution.arrow.enabled", "false") \
        .getOrCreate()

# Load Data with caching
@st.cache_data
def load_data_pandas(source):
    """Load data as Pandas DataFrame from HDFS"""
    try:
        from pyspark.sql.functions import col
        
        spark = init_spark()
        
        # Always load from HDFS
        path = "hdfs://hadoop-master:9000/shop_transactions.csv"
        
        # Load with Spark from HDFS
        spark_df = spark.read.csv(path, header=True, inferSchema=True)
        spark_df = spark_df.withColumn('revenue', col('price') * col('quantity'))
        
        # Convert to Pandas
        rows = spark_df.collect()
        df = pd.DataFrame([row.asDict() for row in rows])
        return df
            
    except Exception as e:
        st.error(f"Error loading data from HDFS: {str(e)}")
        return None

# Load LAB 5 results from HDFS
@st.cache_data
def load_lab5_results():
    """Load pre-computed LAB 5 results"""
    try:
        from pyspark.sql import SparkSession
        spark = init_spark()
        
        results = {}
        
        # Load CÂU 2 results (Top 5 products)
        try:
            q2_df = spark.read.csv('hdfs://hadoop-master:9000/q2_hive_top5_productType', header=True, inferSchema=True)
            rows = q2_df.collect()
            results['q2_top5'] = pd.DataFrame([row.asDict() for row in rows])
        except Exception as e:
            st.warning(f"Could not load CÂU 2 results: {str(e)}")
            results['q2_top5'] = None
        
        # Load CÂU 3 metrics
        try:
            q3_df = spark.read.csv('hdfs://hadoop-master:9000/q3_logistic_regression_metrics', header=True, inferSchema=True)
            rows = q3_df.collect()
            metrics_df = pd.DataFrame([row.asDict() for row in rows])
            results['q3_metrics'] = metrics_df
        except Exception as e:
            st.warning(f"Could not load CÂU 3 metrics: {str(e)}")
            results['q3_metrics'] = None
        
        return results
        
    except Exception as e:
        st.warning(f"Error loading LAB 5 results: {str(e)}")
        return {'q2_top5': None, 'q3_metrics': None}

# Load data
df = load_data_pandas("HDFS")

if df is not None:
    # Overview metrics
    st.sidebar.metric("📦 Total Rows", f"{len(df):,}")
    st.sidebar.metric("💰 Total Revenue", f"${df['revenue'].sum():,.0f}")
    
    # Create tabs
    tab1, tab2, tab3, tab4 = st.tabs([
        "📈 CÂU 2: Hive Analysis",
        "🤖 CÂU 3: ML Model",
        "📊 Data Exploration",
        "ℹ️ Info"
    ])

    # TAB 1: HIVE ANALYSIS
    with tab1:
        st.subheader("Revenue Analysis by Product Type (CÂU 2)")
        
        # Load LAB 5 results
        lab5_results = load_lab5_results()
        
        if lab5_results['q2_top5'] is not None:
            top5 = lab5_results['q2_top5']
            
            col1, col2 = st.columns(2)
            
            # Top 5 Products from results
            with col1:
                st.write("**Top 5 Products by Revenue**")
                # Convert numeric columns
                if 'total_revenue' in top5.columns:
                    top5_display = top5.copy()
                    try:
                        top5_display['total_revenue'] = pd.to_numeric(top5_display['total_revenue'], errors='coerce')
                    except:
                        pass
                    
                    fig = px.bar(
                        top5_display, 
                        x='productType', 
                        y='total_revenue',
                        title='Top 5 Products by Revenue (from HDFS)',
                        labels={'total_revenue': 'Revenue ($)', 'productType': 'Product Type'},
                        color='total_revenue',
                        color_continuous_scale='Blues'
                    )
                    st.plotly_chart(fig, use_container_width=True)
                
                st.dataframe(top5, use_container_width=True)
            
            # All products from raw data
            with col2:
                st.write("**Revenue by Region**")
                region_revenue = df.groupby('customerRegion').agg({
                    'revenue': 'sum',
                    'price': 'count'
                }).rename(columns={'price': 'count'}).reset_index()
                region_revenue = region_revenue.sort_values('revenue', ascending=False)
                region_revenue['revenue'] = region_revenue['revenue'].round(2)
                
                fig = px.pie(
                    region_revenue,
                    values='revenue',
                    names='customerRegion',
                    title='Revenue Distribution by Region'
                )
                st.plotly_chart(fig, use_container_width=True)
            
            # All products stats
            st.write("**All Products Statistics**")
            all_products = df.groupby('productType').agg({
                'price': ['count', 'mean'],
                'revenue': 'sum'
            }).reset_index()
            all_products.columns = ['productType', 'count', 'avg_price', 'total_revenue']
            all_products = all_products.sort_values('total_revenue', ascending=False)
            all_products['avg_price'] = all_products['avg_price'].round(2)
            all_products['total_revenue'] = all_products['total_revenue'].round(2)
            
            st.dataframe(all_products, use_container_width=True)
        else:
            st.warning("⚠️ CÂU 2 results not available. Please run notebook first.")

    # TAB 2: ML MODEL
    with tab2:
        st.subheader("Logistic Regression - Product Type Classification (CÂU 3)")
        
        lab5_results = load_lab5_results()
        
        col1, col2 = st.columns(2)
        
        if lab5_results['q3_metrics'] is not None:
            metrics_df = lab5_results['q3_metrics']
            
            with col1:
                st.write("**Model Performance Metrics (from HDFS)**")
                
                # Convert to display format
                metrics_display = metrics_df.copy()
                try:
                    metrics_display['value'] = pd.to_numeric(metrics_display['value'], errors='coerce')
                    metrics_display = metrics_display.rename(columns={'metric': 'Metric', 'value': 'Score'})
                    
                    fig = px.bar(
                        metrics_display,
                        x='Metric',
                        y='Score',
                        title='Model Evaluation Metrics',
                        color='Score',
                        color_continuous_scale='Reds',
                        range_y=[0, 1]
                    )
                    st.plotly_chart(fig, use_container_width=True)
                except:
                    st.write(metrics_df)
            
            with col2:
                st.write("**Metrics Summary**")
                col_m1, col_m2 = st.columns(2)
                
                # Extract metrics
                try:
                    metrics_dict = dict(zip(metrics_df['metric'], metrics_df['value']))
                    
                    with col_m1:
                        st.metric("Accuracy", metrics_dict.get('Accuracy', 'N/A'))
                        st.metric("Recall", metrics_dict.get('Recall', 'N/A'))
                    with col_m2:
                        st.metric("Precision", metrics_dict.get('Precision', 'N/A'))
                        st.metric("F1-Score", metrics_dict.get('F1_Score', 'N/A'))
                except:
                    st.write(metrics_df)
        else:
            st.warning("⚠️ CÂU 3 metrics not available. Please run notebook first.")
            
            # Show hardcoded values as fallback
            with col1:
                st.write("**Hardcoded Model Performance Metrics**")
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
                    st.metric("Accuracy", "19.95%")
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
            st.metric("Total Transactions", f"{len(df):,}")
        with col2:
            st.metric("Total Revenue", f"${df['revenue'].sum():,.0f}")
        with col3:
            st.metric("Avg Price", f"${df['price'].mean():.2f}")
        with col4:
            st.metric("Avg Quantity", f"{df['quantity'].mean():.2f}")
        
        # Distribution charts
        col1, col2 = st.columns(2)
        
        with col1:
            fig = px.histogram(df, x='price', nbins=50, title='Price Distribution')
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            fig = px.histogram(df, x='quantity', nbins=50, title='Quantity Distribution')
            st.plotly_chart(fig, use_container_width=True)
        
        # Data preview
        st.write("**Data Preview**")
        st.dataframe(df.head(100), use_container_width=True)

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
