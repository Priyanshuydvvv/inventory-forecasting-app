import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
import time

st.set_page_config(
    page_title="Enterprise Inventory Forecasting & Intelligence System",
    layout="wide"
)

if "auth" not in st.session_state:
    st.session_state.auth = False

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
    background: #020617;
}

.glass {
    background: linear-gradient(135deg, rgba(255,255,255,0.14), rgba(255,255,255,0.04));
    backdrop-filter: blur(18px);
    border-radius: 26px;
    padding: 28px;
    border: 1px solid rgba(255,255,255,0.18);
    box-shadow: 0 40px 90px rgba(0,0,0,0.7);
}

.kpi-label {
    font-size: 12px;
    letter-spacing: 0.16em;
    color: #94a3b8;
    text-transform: uppercase;
}

.kpi-value {
    font-size: 34px;
    font-weight: 900;
    background: linear-gradient(90deg, #22d3ee, #a78bfa, #ec4899);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}
</style>
""", unsafe_allow_html=True)

if not st.session_state.auth:
    _, center, _ = st.columns([1,2,1])
    with center:
        st.markdown("<div class='glass'>", unsafe_allow_html=True)
        user = st.text_input("Username")
        pwd = st.text_input("Password", type="password")
        if st.button("Login"):
            if user == "admin" and pwd == "admin123":
                st.session_state.auth = True
                st.rerun()
            else:
                st.error("Invalid credentials")
        st.markdown("</div>", unsafe_allow_html=True)

else:
    df = pd.read_csv("Superstore.csv", encoding="latin1")
    df["Order Date"] = pd.to_datetime(df["Order Date"], errors="coerce")

    start = st.sidebar.date_input("Start", df["Order Date"].min())
    end = st.sidebar.date_input("End", df["Order Date"].max())

    data = df[
        (df["Order Date"] >= pd.to_datetime(start)) &
        (df["Order Date"] <= pd.to_datetime(end))
    ]

    page = st.sidebar.radio("Navigation", [
        "Executive Overview",
        "Sales Intelligence"
    ])

    if page == "Executive Overview":
        st.title("Executive Overview")

        c1, c2, c3, c4 = st.columns(4)
        c1.metric("Revenue", f"${data['Sales'].sum():,.0f}")
        c2.metric("Profit", f"${data['Profit'].sum():,.0f}")
        c3.metric("Orders", len(data))
        c4.metric("Avg Order", f"${data['Sales'].mean():,.0f}")

        # ✅ FIXED PART
        data["Order Date"] = pd.to_datetime(data["Order Date"], errors="coerce")

        monthly = (
            data.dropna(subset=["Order Date"])
                .set_index("Order Date")
                .resample("MS")["Sales"]
                .sum()
        )

        st.line_chart(monthly)

        cat_sales = data.groupby("Category")["Sales"].sum()
        st.bar_chart(cat_sales)

    elif page == "Sales Intelligence":
        st.title("Sales Intelligence")
        st.bar_chart(data.groupby("Category")["Sales"].sum())
