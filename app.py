import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(layout="wide")

df = pd.read_csv("data.csv")

st.title("Food Fortification Dashboard")

# Sidebar filter
region = st.sidebar.selectbox("Select Region", df["Region"].unique())
filtered_df = df[df["Region"] == region]

# KPI
col1, col2, col3 = st.columns(3)
col1.metric("Avg Compliance", round(filtered_df["Compliance"].mean(),1))
col2.metric("Avg Reduction", round(filtered_df["Reduction"].mean(),1))
col3.metric("Total Mills", int(filtered_df["Mills"].sum()))

# Charts
st.subheader("Regional Comparison")
bar = px.bar(df, x="Region", y="Compliance", color="Region")
st.plotly_chart(bar)

st.subheader("Trend Over Time")
line = px.line(filtered_df, x="Month", y="Compliance", markers=True)
st.plotly_chart(line)

st.subheader("Impact Analysis")
scatter = px.scatter(df, x="Compliance", y="Reduction", color="Region", size="Mills")
st.plotly_chart(scatter)

# Insight
st.markdown("### Insights")
st.write("Regions with higher compliance show better anaemia reduction.")
