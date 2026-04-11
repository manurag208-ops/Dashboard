import streamlit as st
import pandas as pd
import plotly.express as px
from openai import OpenAI
# ✅ ADD THIS EXACTLY HERE
st.markdown("""
<style>

/* Bigger multiselect bubbles */
.stMultiSelect [data-baseweb="tag"] {
    font-size: 16px !important;
    padding: 8px 12px !important;
    border-radius: 20px !important;
}

/* Gradient premium color */
.stMultiSelect [data-baseweb="tag"] {
    background: linear-gradient(45deg, #6f42c1, #9b59b6) !important;
    color: white !important;
}

/* Hover effect */
.stMultiSelect [data-baseweb="tag"]:hover {
    background: linear-gradient(45deg, #5a32a3, #8e44ad) !important;
}

</style>
""", unsafe_allow_html=True)
# -----------------------------
# Page Config
# -----------------------------
st.set_page_config(page_title="Policy Intelligence System", layout="wide")

# -----------------------------
# Title
# -----------------------------
st.title("📊 Food Fortification Intelligence Dashboard")
st.markdown("### 🤖 AI-Powered Policy Analysis & Decision System")

# -----------------------------
# Load Data (Upload option)
# -----------------------------
uploaded_file = st.sidebar.file_uploader("📁 Upload CSV", type=["csv"])

if uploaded_file:
    df = pd.read_csv(uploaded_file)
else:
    df = pd.read_csv("data.csv")

df.columns = df.columns.str.strip()

# -----------------------------
# Sidebar Filters
# -----------------------------
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

mode = st.sidebar.radio("Mode", ["Dashboard", "Story", "Simulator"])

filtered_df = df[
    (df["Region"].isin(region)) &
    (df["Month"].isin(month))
]

# -----------------------------
# KPI Section
# -----------------------------
st.subheader("📌 Key Metrics")

col1, col2, col3, col4 = st.columns(4)

col1.metric("🏭 Mills", int(filtered_df["Mills"].sum()))
col2.metric("📊 Compliance", round(filtered_df["Compliance"].mean(), 1))
col3.metric("🧪 Iron", round(filtered_df["Iron"].mean(), 1))
col4.metric("❤️ Anaemia", round(filtered_df["Anaemia"].mean(), 1))

# -----------------------------
# Charts
# -----------------------------
st.subheader("📈 Trends")

fig1 = px.line(filtered_df, x="Month", y="Compliance", color="Region", markers=True)
st.plotly_chart(fig1, use_container_width=True)

fig2 = px.scatter(
    filtered_df,
    x="Iron",
    y="Anaemia",
    size="Mills",
    color="Region"
)
st.plotly_chart(fig2, use_container_width=True)

# -----------------------------
# Map Visualization
# -----------------------------
st.subheader("📍 Region Map")

region_map = {
    "North": (28.6, 77.2),
    "South": (13.0, 80.2),
    "East": (22.6, 88.4),
    "West": (19.0, 72.8),
    "Central": (23.2, 77.4)
}

filtered_df["lat"] = filtered_df["Region"].map(lambda x: region_map.get(x, (0,0))[0])
filtered_df["lon"] = filtered_df["Region"].map(lambda x: region_map.get(x, (0,0))[1])

st.map(filtered_df)

# -----------------------------
# Simulator
# -----------------------------
if mode == "Simulator":
    st.subheader("🎯 Policy Simulator")

    increase = st.slider("Increase Compliance (%)", 0, 20, 5)

    sim_df = filtered_df.copy()
    sim_df["Compliance"] += increase
    sim_df["Anaemia"] += increase * 0.5

    st.write("### Simulated Outcome")
    st.dataframe(sim_df)

# -----------------------------
# Story Mode
# -----------------------------
if mode == "Story":
    st.subheader("📖 Policy Story")

    st.write("📊 Compliance directly impacts anaemia reduction outcomes.")
    st.write("⚠️ Regional disparities highlight implementation gaps.")
    st.write("💡 Strengthening monitoring can improve health outcomes.")

# -----------------------------
# 🤖 ADVANCED AI POLICY ANALYST
# -----------------------------
st.subheader("🤖 AI Policy Advisor")

question = st.text_input("Ask something about your data")

if question:

    # Data context for AI
    data_summary = filtered_df.describe().to_string()
    sample_data = filtered_df.head(20).to_string()

    prompt = f"""
    You are a senior public policy analyst.

    Use the dataset below to answer in DETAIL.

    DATA SUMMARY:
    {data_summary}

    SAMPLE DATA:
    {sample_data}

    QUESTION:
    {question}

    Give answer in this format:

    1. Key Insight (data-based)
    2. Trend Analysis
    3. Policy Interpretation
    4. Recommendations

    Make answer detailed, analytical, and professional.
    """

    client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}]
    )

    st.write(response.choices[0].message.content)

# -----------------------------
# Download Report
# -----------------------------
st.subheader("📥 Download Data")

csv = filtered_df.to_csv(index=False).encode('utf-8')

st.download_button(
    "Download Filtered Data",
    csv,
    "data.csv",
    "text/csv"
)

# -----------------------------
# Footer
# -----------------------------

