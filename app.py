import streamlit as st
import pandas as pd
import plotly.express as px

# Page config
st.set_page_config(page_title="Dashboard", layout="wide")

# Title
st.title("📊 Food Fortification Dashboard")

# Load data
df = pd.read_csv("data.csv")

# Sidebar filters
st.sidebar.header("🔍 Filters")

region = st.sidebar.multiselect(
    "Select Region",
    df["Region"].unique(),
    default=df["Region"].unique()
)

month = st.sidebar.multiselect(
    "Select Month",
    df["Month"].unique(),
    default=df["Month"].unique()
)

# Filter data
filtered_df = df[
    (df["Region"].isin(region)) &
    (df["Month"].isin(month))
]

# KPIs
col1, col2, col3 = st.columns(3)

col1.metric("Total Mills", filtered_df["Mills"].sum())
col2.metric("Avg Compliance", round(filtered_df["Compliance"].mean(), 2))
col3.metric("Total Reduction", filtered_df["Reduction"].sum())

# Charts
st.subheader("📈 Compliance Trend")
fig1 = px.line(filtered_df, x="Month", y="Compliance", color="Region", markers=True)
st.plotly_chart(fig1, use_container_width=True)

st.subheader("📊 Mills by Region")
fig2 = px.bar(filtered_df, x="Region", y="Mills", color="Region")
st.plotly_chart(fig2, use_container_width=True)

# Table
st.subheader("📋 Data Table")
st.dataframe(filtered_df)

st.success("✅ Dashboard Ready for Presentation!")
