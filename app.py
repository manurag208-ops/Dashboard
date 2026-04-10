import streamlit as st
import pandas as pd
import plotly.express as px

# -----------------------------
# Page Config
# -----------------------------
st.set_page_config(page_title="Food Fortification Dashboard", layout="wide")

# -----------------------------
# Title
# -----------------------------
st.title("📊 Food Fortification & Anaemia Reduction Dashboard")

# -----------------------------
# Load Data
# -----------------------------
df = pd.read_csv("data.csv")

# Clean column names (important fix)
df.columns = df.columns.str.strip()

# -----------------------------
# Sidebar Filters
# -----------------------------
st.sidebar.header("🔍 Filter Data")

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

# Apply filters
filtered_df = df[
    (df["Region"].isin(region)) &
    (df["Month"].isin(month))
]

# -----------------------------
# KPI SECTION
# -----------------------------
st.subheader("📌 Key Performance Indicators")

col1, col2, col3, col4 = st.columns(4)

col1.metric("Total Mills", int(filtered_df["Mills"].sum()))
col2.metric("Avg Compliance", round(filtered_df["Compliance"].mean(), 1))
col3.metric("Avg Iron (ppm)", round(filtered_df["Iron ppm"].mean(), 1))
col4.metric("Avg Anaemia Reduction", round(filtered_df["Anaemia Reduction"].mean(), 1))

# -----------------------------
# CHART 1: Compliance Trend
# -----------------------------
st.subheader("📈 Monthly Compliance Trend")

fig1 = px.line(
    filtered_df,
    x="Month",
    y="Compliance",
    color="Region",
    markers=True
)
st.plotly_chart(fig1, use_container_width=True)

# -----------------------------
# CHART 2: Anaemia Reduction
# -----------------------------
st.subheader("📊 Anaemia Reduction by Region")

fig2 = px.bar(
    filtered_df,
    x="Region",
    y="Anaemia Reduction",
    color="Region"
)
st.plotly_chart(fig2, use_container_width=True)

# -----------------------------
# CHART 3: Iron vs Reduction
# -----------------------------
st.subheader("🔬 Iron vs Anaemia Reduction (Impact Analysis)")

fig3 = px.scatter(
    filtered_df,
    x="Iron ppm",
    y="Anaemia Reduction",
    color="Region",
    size="Mills",
    hover_data=["Month"]
)
st.plotly_chart(fig3, use_container_width=True)

# -----------------------------
# TABLE
# -----------------------------
st.subheader("📋 Full Dataset")
st.dataframe(filtered_df)

# -----------------------------
# INSIGHTS
# -----------------------------
st.subheader("🧠 Key Insights")

highest = filtered_df.loc[filtered_df["Compliance"].idxmax()]
lowest = filtered_df.loc[filtered_df["Compliance"].idxmin()]

st.write(f"✅ Highest compliance: **{highest['Region']} ({highest['Month']})**")
st.write(f"⚠️ Lowest compliance: **{lowest['Region']} ({lowest['Month']})**")

# -----------------------------
# Footer
# -----------------------------
st.success("🚀 Dashboard Ready for Presentation!")
