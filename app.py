import streamlit as st
import pandas as pd
import plotly.express as px

# Page settings
st.set_page_config(page_title="Dashboard", layout="wide")

# Title
st.title("📊 Food Fortification Dashboard")

# Sample data
data = {
    "Month": ["Jan", "Feb", "Mar", "Apr", "May", "Jun"],
    "Region": ["North", "South", "East", "West", "North", "South"],
    "Production": [120, 150, 100, 180, 200, 170],
    "Compliance": [85, 90, 78, 88, 92, 87]
}

df = pd.DataFrame(data)

# Sidebar filter
st.sidebar.header("Filters")
region = st.sidebar.multiselect(
    "Select Region",
    df["Region"].unique(),
    default=df["Region"].unique()
)

filtered_df = df[df["Region"].isin(region)]

# KPIs
col1, col2, col3 = st.columns(3)
col1.metric("Total Production", filtered_df["Production"].sum())
col2.metric("Avg Compliance", round(filtered_df["Compliance"].mean(), 2))
col3.metric("Total Records", len(filtered_df))

# Charts
st.subheader("Production Trend")
fig1 = px.line(filtered_df, x="Month", y="Production", color="Region", markers=True)
st.plotly_chart(fig1, use_container_width=True)

st.subheader("Compliance by Region")
fig2 = px.bar(filtered_df, x="Region", y="Compliance", color="Region")
st.plotly_chart(fig2, use_container_width=True)

# Table
st.subheader("Data Table")
st.dataframe(filtered_df)

# Success message
st.success("✅ Dashboard is live!")
