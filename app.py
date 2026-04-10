import streamlit as st
import pandas as pd

# Title
st.title("📊 Dashboard Project")

# Sample Data
data = {
    "Month": ["Jan", "Feb", "Mar", "Apr"],
    "Sales": [100, 200, 150, 300]
}

df = pd.DataFrame(data)

# Show Data
st.subheader("Data Table")
st.dataframe(df)

# Show Chart
st.subheader("Sales Trend")
st.line_chart(df.set_index("Month"))

# Message
st.success("Dashboard is working 🚀")
