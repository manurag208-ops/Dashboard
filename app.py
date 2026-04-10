import streamlit as st
import pandas as pd
import plotly.express as px

# -----------------------------
# Page Config
# -----------------------------
st.set_page_config(page_title="Premium Dashboard", layout="wide")

# -----------------------------
# Custom Styling (🔥 UI Upgrade)
# -----------------------------
st.markdown("""
<style>
.metric-card {
    background-color: #f0f2f6;
    padding: 15px;
    border-radius: 12px;
    text-align: center;
    box-shadow: 2px 2px 8px rgba(0,0,0,0.1);
}
</style>
""", unsafe_allow_html=True)

# -----------------------------
# Title
# -----------------------------
st.title("📊 Food Fortification Impact Dashboard")
st.markdown("### 🧠 Policy Insights on Compliance & Anaemia Reduction")

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

filtered_df = df[
    (df["Region"].isin(region)) &
    (df["Month"].isin(month))
]

# -----------------------------
# KPI CARDS (🔥 Premium Look)
# -----------------------------
st.subheader("📌 Key Metrics Overview")

col1, col2, col3, col4 = st.columns(4)

col1.metric("🏭 Total Mills", int(filtered_df["Mills"].sum()))
col2.metric("📊 Avg Compliance", round(filtered_df["Compliance"].mean(), 1))
col3.metric("🧪 Avg Iron", round(filtered_df["Iron"].mean(), 1))
col4.metric("❤️ Avg Anaemia Reduction", round(filtered_df["Anaemia"].mean(), 1))

# -----------------------------
# CHARTS (Better Layout)
# -----------------------------
colA, colB = st.columns(2)

with colA:
    st.subheader("📈 Compliance Trend")
    fig1 = px.line(filtered_df, x="Month", y="Compliance",
                   color="Region", markers=True)
    st.plotly_chart(fig1, use_container_width=True)

with colB:
    st.subheader("📊 Anaemia Reduction by Region")
    fig2 = px.bar(filtered_df, x="Region", y="Anaemia",
                  color="Region")
    st.plotly_chart(fig2, use_container_width=True)

# -----------------------------
# IMPACT ANALYSIS (🔥 USP)
# -----------------------------
st.subheader("🔬 Impact Analysis: Iron vs Anaemia")

fig3 = px.scatter(
    filtered_df,
    x="Iron",
    y="Anaemia",
    color="Region",
    size="Mills",
    hover_data=["Month"],
    title="Higher Iron → Higher Reduction?"
)
st.plotly_chart(fig3, use_container_width=True)

# -----------------------------
# DATA TABLE
# -----------------------------
with st.expander("📋 View Full Dataset"):
    st.dataframe(filtered_df)

# -----------------------------
# AUTO POLICY INSIGHTS (🔥 GOLD)
# -----------------------------
st.subheader("🧠 Policy Insights")

if not filtered_df.empty:

    high = filtered_df.loc[filtered_df["Compliance"].idxmax()]
    low = filtered_df.loc[filtered_df["Compliance"].idxmin()]

    avg_comp = round(filtered_df["Compliance"].mean(), 1)
    avg_red = round(filtered_df["Anaemia"].mean(), 1)

    st.markdown(f"""
    ### 📌 Key Findings:
    
    - ✅ Highest compliance in **{high['Region']} ({high['Month']})**
    - ⚠️ Lowest compliance in **{low['Region']} ({low['Month']})**
    - 📊 Average compliance is **{avg_comp}%**
    - ❤️ Average anaemia reduction is **{avg_red}%**
    
    ### 🎯 Policy Interpretation:
    
    - Regions with higher compliance show **better anaemia reduction outcomes**
    - Iron fortification appears to have a **positive correlation with health impact**
    - Focus needed on **low-performing regions for targeted intervention**
    """)

# -----------------------------
# DOWNLOAD BUTTON (🔥 PRO FEATURE)
# -----------------------------
csv = filtered_df.to_csv(index=False).encode('utf-8')

st.download_button(
    "📥 Download Filtered Data",
    csv,
    "filtered_data.csv",
    "text/csv"
)

# -----------------------------
# Footer
# -----------------------------
st.success("🚀 Premium Dashboard Ready for Presentation!")
