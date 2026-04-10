import streamlit as st
import pandas as pd
import plotly.express as px

# -----------------------------
# Page Config
# -----------------------------
st.set_page_config(page_title="Ultra Dashboard", layout="wide")

# -----------------------------
# Title
# -----------------------------
st.title("📊 Food Fortification Intelligence Dashboard")
st.markdown("### 🚀 Advanced Policy Analytics & Insights")

# -----------------------------
# Load Data
# -----------------------------
df = pd.read_csv("data.csv")
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

view_mode = st.sidebar.radio(
    "📖 View Mode",
    ["Dashboard", "Story Mode"]
)

filtered_df = df[
    (df["Region"].isin(region)) &
    (df["Month"].isin(month))
]

# -----------------------------
# KPI SECTION
# -----------------------------
st.subheader("📌 Key Metrics")

col1, col2, col3, col4 = st.columns(4)

col1.metric("🏭 Mills", int(filtered_df["Mills"].sum()))
col2.metric("📊 Compliance", round(filtered_df["Compliance"].mean(), 1))
col3.metric("🧪 Iron", round(filtered_df["Iron"].mean(), 1))
col4.metric("❤️ Anaemia", round(filtered_df["Anaemia"].mean(), 1))

# -----------------------------
# CHARTS
# -----------------------------
colA, colB = st.columns(2)

with colA:
    st.subheader("📈 Compliance Trend")
    fig1 = px.line(filtered_df, x="Month", y="Compliance", color="Region", markers=True)
    st.plotly_chart(fig1, use_container_width=True)

with colB:
    st.subheader("📊 Anaemia Reduction")
    fig2 = px.bar(filtered_df, x="Region", y="Anaemia", color="Region")
    st.plotly_chart(fig2, use_container_width=True)

# -----------------------------
# MAP VISUALIZATION (🔥 NEW)
# -----------------------------
st.subheader("📍 Regional Distribution (Bubble Map)")

# Fake coordinates for demo (you can upgrade later)
region_map = {
    "North": (28.6, 77.2),
    "South": (13.0, 80.2),
    "East": (22.6, 88.4),
    "West": (19.0, 72.8),
    "Central": (23.2, 77.4)
}

filtered_df["lat"] = filtered_df["Region"].map(lambda x: region_map[x][0])
filtered_df["lon"] = filtered_df["Region"].map(lambda x: region_map[x][1])

st.map(filtered_df)

# -----------------------------
# IMPACT ANALYSIS
# -----------------------------
st.subheader("🔬 Impact: Iron vs Anaemia")

fig3 = px.scatter(
    filtered_df,
    x="Iron",
    y="Anaemia",
    color="Region",
    size="Mills",
    hover_data=["Month"]
)
st.plotly_chart(fig3, use_container_width=True)

# -----------------------------
# STORY MODE (🔥 BIG FEATURE)
# -----------------------------
if view_mode == "Story Mode":

    st.subheader("📖 Policy Storytelling")

    avg_comp = round(filtered_df["Compliance"].mean(), 1)
    avg_red = round(filtered_df["Anaemia"].mean(), 1)

    st.markdown(f"""
    ### 🎯 Situation
    Food fortification programs aim to improve nutritional outcomes.

    ### 📊 Findings
    - Average compliance: **{avg_comp}%**
    - Average anaemia reduction: **{avg_red}%**

    ### ⚠️ Problem
    Some regions show low compliance leading to weak impact.

    ### 💡 Recommendation
    - Strengthen monitoring systems
    - Focus on low-performing regions
    - Improve iron dosage consistency

    ### 🚀 Impact
    Better compliance → Higher anaemia reduction → Stronger public health outcomes
    """)

# -----------------------------
# AI-LIKE RECOMMENDATIONS (🔥 WOW)
# -----------------------------
st.subheader("🤖 Smart Recommendations")

if not filtered_df.empty:
    if filtered_df["Compliance"].mean() < 70:
        st.warning("⚠️ Compliance is low → Strengthen enforcement policies")
    else:
        st.success("✅ Good compliance → Focus on scaling impact")

    if filtered_df["Anaemia"].mean() < 30:
        st.warning("⚠️ Low health impact → Improve iron fortification quality")
    else:
        st.success("❤️ Strong health impact observed")

# -----------------------------
# DOWNLOAD
# -----------------------------
csv = filtered_df.to_csv(index=False).encode('utf-8')

st.download_button(
    "📥 Download Data",
    csv,
    "dashboard_data.csv",
    "text/csv"
)

# -----------------------------
# Footer
# -----------------------------
st.success("🚀 Ultra Premium Dashboard Ready!")
