import streamlit as st
import pandas as pd
import plotly.express as px

# -----------------------------
# Page Config
# -----------------------------
st.set_page_config(page_title="Elite Dashboard", layout="wide")

# -----------------------------
# Title
# -----------------------------
st.title("📊 Food Fortification Decision System")
st.markdown("### 🤖 AI-Powered Policy Intelligence Dashboard")

# -----------------------------
# FILE UPLOAD (🔥 BIG FEATURE)
# -----------------------------
uploaded_file = st.sidebar.file_uploader("📁 Upload your dataset (CSV)", type=["csv"])

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
# KPI
# -----------------------------
col1, col2, col3, col4 = st.columns(4)

col1.metric("🏭 Mills", int(filtered_df["Mills"].sum()))
col2.metric("📊 Compliance", round(filtered_df["Compliance"].mean(), 1))
col3.metric("🧪 Iron", round(filtered_df["Iron"].mean(), 1))
col4.metric("❤️ Anaemia", round(filtered_df["Anaemia"].mean(), 1))

# -----------------------------
# CHARTS
# -----------------------------
st.subheader("📈 Trends")

fig1 = px.line(filtered_df, x="Month", y="Compliance", color="Region", markers=True)
st.plotly_chart(fig1, use_container_width=True)

fig2 = px.scatter(filtered_df, x="Iron", y="Anaemia", size="Mills", color="Region")
st.plotly_chart(fig2, use_container_width=True)

# -----------------------------
# MAP
# -----------------------------
region_map = {
    "North": (28.6, 77.2),
    "South": (13.0, 80.2),
    "East": (22.6, 88.4),
    "West": (19.0, 72.8),
    "Central": (23.2, 77.4)
}

filtered_df["lat"] = filtered_df["Region"].map(lambda x: region_map[x][0])
filtered_df["lon"] = filtered_df["Region"].map(lambda x: region_map[x][1])

st.subheader("📍 Region Map")
st.map(filtered_df)

# -----------------------------
# STORY MODE
# -----------------------------
if mode == "Story":
    st.subheader("📖 Policy Story")

    st.write("📊 Compliance drives health outcomes.")
    st.write("⚠️ Low performing regions need targeted interventions.")
    st.write("💡 Iron levels strongly influence anaemia reduction.")

# -----------------------------
# SIMULATOR (🔥 UNIQUE)
# -----------------------------
if mode == "Simulator":
    st.subheader("🎯 Policy Simulator")

    increase = st.slider("Increase Compliance (%)", 0, 20, 5)

    simulated = filtered_df.copy()
    simulated["Compliance"] += increase
    simulated["Anaemia"] += increase * 0.5

    st.write("### 📊 Simulated Impact")
    st.dataframe(simulated)

# -----------------------------
# AI CHAT (🔥 WOW FACTOR)
# -----------------------------
st.subheader("🤖 Ask Policy AI")

question = st.text_input("Ask something about data...")

if question:
    if "compliance" in question.lower():
        st.write("👉 Higher compliance improves outcomes significantly.")
    elif "anaemia" in question.lower():
        st.write("👉 Anaemia reduction improves with better fortification.")
    else:
        st.write("👉 Data suggests focusing on regional disparities.")

# -----------------------------
# DOWNLOAD REPORT
# -----------------------------
report = filtered_df.describe().to_csv().encode('utf-8')

st.download_button("📥 Download Report", report, "report.csv", "text/csv")

# -----------------------------
# Footer
# -----------------------------
st.success("🚀 Elite Dashboard Ready!")
