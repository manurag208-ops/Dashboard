import streamlit as st
import pandas as pd
import plotly.express as px

# Page config
st.set_page_config(page_title="Dashboard", layout="wide")

# Title
st.title("📊 Food Fortification Dashboard")

# Load data
df = pd.read_csv("data.csv")

# Clean column names
df.columns = df.columns.str.strip()

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

# ---------------- KPI ----------------
st.subheader("📌 Key Metrics")

col1, col2, col3, col4 = st.columns(4)

col1.metric("Total Mills", int(filtered_df["Mills"].sum()))
col2.metric("Avg Compliance", round(filtered_df["Compliance"].mean(), 1))
col3.metric("Avg Iron", round(filtered_df["Iron"].mean(), 1))
col4.metric("Avg Anaemia", round(filtered_df["Anaemia"].mean(), 1))

# ---------------- Charts ----------------
st.subheader("📈 Compliance Trend")
fig1 = px.line(filtered_df, x="Month", y="Compliance", color="Region", markers=True)
st.plotly_chart(fig1, use_container_width=True)

st.subheader("📊 Anaemia Reduction")
fig2 = px.bar(filtered_df, x="Region", y="Anaemia", color="Region")
st.plotly_chart(fig2, use_container_width=True)

st.subheader("🔬 Iron vs Anaemia Impact")
fig3 = px.scatter(
    filtered_df,
    x="Iron",
    y="Anaemia",
    color="Region",
    size="Mills",
    hover_data=["Month"]
)
st.plotly_chart(fig3, use_container_width=True)

# ---------------- Table ----------------
st.subheader("📋 Data Table")
st.dataframe(filtered_df)

# ---------------- Insights ----------------
st.subheader("🧠 Insights")

if not filtered_df.empty:
    high = filtered_df.loc[filtered_df["Compliance"].idxmax()]
    low = filtered_df.loc[filtered_df["Compliance"].idxmin()]

    st.write(f"✅ Highest compliance: **{high['Region']} ({high['Month']})**")
    st.write(f"⚠️ Lowest compliance: **{low['Region']} ({low['Month']})**")

st.success("🚀 Dashboard Running Perfectly!")
