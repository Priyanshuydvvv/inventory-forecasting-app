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

.appview-container {
    background:
        radial-gradient(900px at 10% 10%, rgba(56,189,248,0.18), transparent),
        radial-gradient(800px at 90% 20%, rgba(167,139,250,0.20), transparent),
        radial-gradient(700px at 50% 90%, rgba(236,72,153,0.14), transparent),
        linear-gradient(180deg, #020617, #020617);
}

h1 {
    font-size: 42px;
    font-weight: 900;
    letter-spacing: -0.04em;
    background: linear-gradient(90deg, #38bdf8, #818cf8, #ec4899);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

.glass {
    background: linear-gradient(
        135deg,
        rgba(255,255,255,0.14),
        rgba(255,255,255,0.04)
    );
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

.spacer {
    height: 28px;
}
</style>
""", unsafe_allow_html=True)

if not st.session_state.auth:
    st.markdown("<br><br><br>", unsafe_allow_html=True)
    _, center, _ = st.columns([1,2,1])
    with center:
        st.markdown("<div class='glass'>", unsafe_allow_html=True)
        st.markdown("# Enterprise Inventory Forecasting & Intelligence System")
        st.markdown("🔐 Secure access to enterprise analytics & forecasting")
        user = st.text_input("Username")
        pwd = st.text_input("Password", type="password")
        if st.button("🚀 Enter Platform"):
            if user == "admin" and pwd == "admin123":
                st.session_state.auth = True
                st.rerun()
            else:
                st.error("Invalid credentials")
        st.caption("Demo access → admin / admin123")
        st.markdown("</div>", unsafe_allow_html=True)

else:
    df = pd.read_csv("Superstore.csv", encoding="latin1")
    df["Order Date"] = pd.to_datetime(df["Order Date"])

    st.sidebar.markdown("📦 Enterprise Inventory System")
    start = st.sidebar.date_input("📅 Start date", df["Order Date"].min())
    end = st.sidebar.date_input("📅 End date", df["Order Date"].max())

    data = df[
        (df["Order Date"] >= pd.to_datetime(start)) &
        (df["Order Date"] <= pd.to_datetime(end))
    ]

    if st.sidebar.button("🔒 Logout"):
        st.session_state.auth = False
        st.rerun()

    page = st.sidebar.radio(
        "🧭 Navigation",
        [
            "Executive Overview",
            "Sales Intelligence",
            "Demand Forecasting",
            "Inventory Risk Monitoring",
            "AI Decision Assistant"
        ]
    )

    if data.empty:
        st.warning("⚠️ No data available for selected date range")
        st.stop()

    if page == "Executive Overview":
        st.markdown("# Executive Overview")
        st.markdown("📊 High-level KPIs and business performance")

        with st.spinner("Loading executive metrics…"):
            time.sleep(0.6)

        c1, c2, c3, c4 = st.columns(4)
        cards = [
            ("💰 Total Revenue", f"${data['Sales'].sum():,.0f}"),
            ("📈 Total Profit", f"${data['Profit'].sum():,.0f}"),
            ("🧾 Orders", len(data)),
            ("📦 Avg Order Value", f"${data['Sales'].mean():,.0f}")
        ]

        for col, (label, value) in zip([c1,c2,c3,c4], cards):
            col.markdown(
                f"<div class='glass'><div class='kpi-label'>{label}</div><div class='kpi-value'>{value}</div></div>",
                unsafe_allow_html=True
            )

        st.markdown("<div class='spacer'></div>", unsafe_allow_html=True)

        monthly = data.set_index("Order Date").resample("M")["Sales"].sum()
        st.line_chart(monthly)

        st.markdown("<div class='spacer'></div>", unsafe_allow_html=True)

        cat_sales = data.groupby("Category")["Sales"].sum()
        l, r = st.columns(2)

        with l:
            st.markdown("<div class='glass'>", unsafe_allow_html=True)
            st.bar_chart(cat_sales)
            st.markdown("📊 Category-wise revenue distribution")
            st.markdown("</div>", unsafe_allow_html=True)

        with r:
            st.markdown("<div class='glass'>", unsafe_allow_html=True)
            fig, ax = plt.subplots()
            ax.pie(cat_sales, labels=cat_sales.index, autopct="%1.1f%%", startangle=90)
            ax.axis("equal")
            st.pyplot(fig)
            st.markdown("🥧 Contribution by category")
            st.markdown("</div>", unsafe_allow_html=True)

        st.markdown("<div class='spacer'></div>", unsafe_allow_html=True)

        st.download_button(
            "⬇️ Download Executive Report",
            data.to_csv(index=False),
            "executive_report.csv",
            "text/csv",
            use_container_width=True
        )

    elif page == "Sales Intelligence":
        st.markdown("# Sales Intelligence")
        st.markdown("📉 Product & category sales insights")

        l, r = st.columns(2)
        with l:
            st.markdown("<div class='glass'>", unsafe_allow_html=True)
            st.bar_chart(data.groupby("Category")["Sales"].sum())
            st.markdown("</div>", unsafe_allow_html=True)

        with r:
            st.markdown("<div class='glass'>", unsafe_allow_html=True)
            top = (
                data.groupby("Product Name")["Sales"]
                .sum().sort_values(ascending=False).head(5)
            )
            st.dataframe(top)
            st.markdown("</div>", unsafe_allow_html=True)

        st.download_button(
            "⬇️ Download Sales Dataset",
            data.to_csv(index=False),
            "sales_data.csv",
            "text/csv",
            use_container_width=True
        )

    elif page == "Demand Forecasting":
        st.markdown("# Demand Forecasting")
        st.markdown("🤖 AI-based future demand prediction")

        cat = st.selectbox("📦 Select category", data["Category"].unique())
        subset = data[data["Category"] == cat]

        ts = subset.groupby("Order Date")["Sales"].sum().reset_index()
        ts["t"] = range(len(ts))

        model = LinearRegression()
        model.fit(ts[["t"]], ts["Sales"])

        days = st.slider("⏳ Forecast days", 7, 90, 30)
        future = np.arange(len(ts), len(ts) + days).reshape(-1,1)
        forecast = model.predict(future)

        plt.figure(figsize=(10,4))
        plt.plot(ts["Sales"], label="Historical")
        plt.plot(range(len(ts), len(ts)+days), forecast, label="Forecast")
        plt.legend()
        st.pyplot(plt)

        forecast_df = pd.DataFrame({"Forecasted Sales": forecast})

        st.download_button(
            "⬇️ Download Forecast Output",
            forecast_df.to_csv(index=False),
            "forecast_output.csv",
            "text/csv",
            use_container_width=True
        )

    elif page == "Inventory Risk Monitoring":
        st.markdown("# Inventory Risk Monitoring")
        st.markdown("🚨 Stock health & risk indicators")

        stock = st.number_input("📦 Current stock", value=100000)
        demand = data["Sales"].sum()
        risk = min(100, int((demand / stock) * 100))

        st.markdown(
            f"<div class='glass'><div class='kpi-label'>⚠️ Risk Index</div><div class='kpi-value'>{risk} / 100</div></div>",
            unsafe_allow_html=True
        )

        if risk > 75:
            st.error("🚨 High stock-out risk detected")
        elif risk > 50:
            st.warning("⚠️ Moderate inventory pressure")
        else:
            st.success("✅ Inventory levels are stable")

    elif page == "AI Decision Assistant":
        st.markdown("# AI Decision Assistant")
        st.markdown("💬 Ask business questions from the selected data")

        q = st.text_input("Type your question")

        if q:
            st.markdown("<div class='glass'>", unsafe_allow_html=True)
            ql = q.lower()
            if "sales" in ql:
                st.write(f"💰 Total sales: ${data['Sales'].sum():,.0f}")
            elif "profit" in ql:
                st.write(f"📈 Total profit: ${data['Profit'].sum():,.0f}")
            elif "risk" in ql:
                st.write("🚨 Risk increases when demand exceeds available stock")
            elif "trend" in ql:
                st.write("📊 Trends vary with time range and category")
            else:
                st.write("🧠 Focus on forecasting accuracy for better planning")
            st.markdown("</div>", unsafe_allow_html=True)
