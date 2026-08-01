import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np
from pathlib import Path


st.set_page_config(page_title="Automation Dashboard", layout="wide")

CSV_PATH = Path("sales_data.csv")

def generate_mock_data():
    """Generates a dummy dataset if none exists for testing."""
    if not CSV_PATH.exists():
        np.random.seed(42)
        dates = pd.date_range(start="2026-01-01", periods=100)
        data = {
            "Date": np.random.choice(dates, size=500),
            "Category": np.random.choice(["Electronics", "Software", "Cloud Services", "Hardware"], size=500),
            "Region": np.random.choice(["North", "East", "West", "South"], size=500),
            "Revenue": np.random.uniform(50, 1500, size=500).round(2),
            "Units_Sold": np.random.randint(1, 10, size=500)
        }
        df = pd.DataFrame(data)

        df.loc[df.sample(frac=0.05).index, 'Revenue'] = np.nan
        df.to_csv(CSV_PATH, index=False)

def load_and_clean_data():
    """Data Pipeline: Extraction, Transformation, Loading (ETL)"""
    df = pd.read_csv(CSV_PATH)
    
    
    median_revenue = df['Revenue'].median()
    df['Revenue'] = df['Revenue'].fillna(median_revenue)
    
    
    df['Date'] = pd.to_datetime(df['Date'])
    return df


generate_mock_data()
df_clean = load_and_clean_data()


st.title("📊Automation & Analytics Dashboard")
st.markdown("This dashboard automatically ingests raw data files, runs a cleaning pipeline, and visualizes system metrics.")


st.sidebar.header("Filter Controls")
selected_region = st.sidebar.multiselect(
    "Select Region(s):", 
    options=df_clean["Region"].unique(), 
    default=df_clean["Region"].unique()
)


filtered_df = df_clean[df_clean["Region"].isin(selected_region)]


kpi1, kpi2, kpi3 = st.columns(3)
with kpi1:
    st.metric(label="Total Revenue ($)", value=f"${filtered_df['Revenue'].sum():,.2f}")
with kpi2:
    st.metric(label="Total Units Sold", value=f"{filtered_df['Units_Sold'].sum():,}")
with kpi3:
    st.metric(label="Avg Order Value ($)", value=f"${filtered_df['Revenue'].mean():,.2f}")

st.markdown("---")


chart_col1, chart_col2 = st.columns(2)

with chart_col1:
    st.subheader("Revenue Contribution by Category")
    fig_pie = px.pie(filtered_df, values='Revenue', names='Category', hole=0.4,
                     color_discrete_sequence=px.colors.sequential.RdBu)
    st.plotly_chart(fig_pie, use_container_width=True)

with chart_col2:
    st.subheader("Daily Revenue Trends")
    trend_df = filtered_df.groupby('Date')['Revenue'].sum().reset_index()
    fig_line = px.line(trend_df, x='Date', y='Revenue', markers=True)
    st.plotly_chart(fig_line, use_container_width=True)


with st.expander("🔍 View Cleaned Backend Dataset"):
    st.dataframe(filtered_df, use_container_width=True)
