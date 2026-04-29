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

# ================= STYLING =================
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

.spacer { height: 28px; }
</style>
""", unsafe_allow_html=True)

# ================= LOGIN =================
if not st.session_state.auth:
    st.markdown("<br><br><br>", unsafe_allow_html=True)
    _, center, _ = st.columns([1,2,1])
    with center:
        st.markdown("<div class='glass'>", unsafe_allow_html=True)
        st.markdown("# Enterprise Inventory System")
        user = st.text_input("Username")
        pwd = st.text_input("Password", type="password")

        if st.button("🚀 Enter Platform"):
            if user == "admin" and pwd == "admin123":
                st.session_state.auth = True
                st.rerun()
            else:
                st.error("Invalid credentials")

        st.caption("Demo → admin / admin123")
        st.markdown("</div>", unsafe_allow_html=True)

# ================= MAIN =================
else:
    df = pd.read_csv("Superstore.csv", encoding="latin1")

    # ✅ FIXED DATE ISSUE
    df["Order Date"] = pd.to_datetime(df["Order Date"], errors="coerce")
    df = df.dropna(subset=["Order Date"])

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
        st.warning("⚠️ No data available")
        st.stop()

    # ================= EXECUTIVE =================
    if page == "Executive Overview":
        st.markdown("# Executive Overview")

        c1, c2, c3, c4 = st.columns(4)

        cards = [
            ("💰 Revenue", f"${data['Sales'].sum():,.0f}"),
            ("📈 Profit", f"${data['Profit'].sum():,.0f}"),
            ("🧾 Orders", len(data)),
            ("📦 Avg Order", f"${data['Sales'].mean():,.0f}")
        ]

        for col, (label, value) in zip([c1,c2,c3,c4], cards):
            col.markdown(
                f"<div class='glass'><div class='kpi-label'>{label}</div><div class='kpi-value'>{value}</div></div>",
                unsafe_allow_html=True
            )

        st.markdown("<div class='spacer'></div>", unsafe_allow_html=True)

        # ✅ FIXED RESAMPLING
        monthly = (
            data.set_index("Order Date")
                .resample("MS")["Sales"]
                .sum()
        )

        st.line_chart(monthly)

        st.markdown("<div class='spacer'></div>", unsafe_allow_html=True)

        cat_sales = data.groupby("Category")["Sales"].sum()
        col1, col2 = st.columns(2)

        with col1:
            st.markdown("<div class='glass'>", unsafe_allow_html=True)
            st.bar_chart(cat_sales)
            st.markdown("</div>", unsafe_allow_html=True)

        with col2:
            st.markdown("<div class='glass'>", unsafe_allow_html=True)
            fig, ax = plt.subplots()
            ax.pie(cat_sales, labels=cat_sales.index, autopct="%1.1f%%")
            st.pyplot(fig)
            st.markdown("</div>", unsafe_allow_html=True)

    # ================= SALES =================
    elif page == "Sales Intelligence":
        st.markdown("# Sales Intelligence")

        col1, col2 = st.columns(2)

        with col1:
            st.bar_chart(data.groupby("Category")["Sales"].sum())

        with col2:
            top = data.groupby("Product Name")["Sales"].sum().nlargest(5)
            st.dataframe(top)

    # ================= FORECAST =================
    elif page == "Demand Forecasting":
        st.markdown("# Demand Forecasting")

        cat = st.selectbox("Select category", data["Category"].unique())
        subset = data[data["Category"] == cat]

        ts = subset.groupby("Order Date")["Sales"].sum().reset_index()
        ts["t"] = range(len(ts))

        model = LinearRegression()
        model.fit(ts[["t"]], ts["Sales"])

        days = st.slider("Forecast days", 7, 90, 30)
        future = np.arange(len(ts), len(ts) + days).reshape(-1,1)
        forecast = model.predict(future)

        plt.figure(figsize=(10,4))
        plt.plot(ts["Sales"], label="History")
        plt.plot(range(len(ts), len(ts)+days), forecast, label="Forecast")
        plt.legend()
        st.pyplot(plt)

    # ================= INVENTORY =================
    elif page == "Inventory Risk Monitoring":
        st.markdown("# Inventory Risk Monitoring")

        stock = st.number_input("Stock", value=100000)
        demand = data["Sales"].sum()

        risk = min(100, int((demand / stock) * 100))

        st.metric("Risk Index", f"{risk}/100")

        if risk > 75:
            st.error("High risk")
        elif risk > 50:
            st.warning("Medium risk")
        else:
            st.success("Low risk")

    # ================= AI =================
    elif page == "AI Decision Assistant":
        st.markdown("# AI Decision Assistant 🤖")

        q = st.text_input("Ask business question")

        if q:
            st.markdown("<div class='glass'>", unsafe_allow_html=True)

            q = q.lower()

            if "sales" in q:
                st.write(f"💰 Total sales: ${data['Sales'].sum():,.0f}")
            elif "profit" in q:
                st.write(f"📈 Profit: ${data['Profit'].sum():,.0f}")
            elif "best category" in q:
                best = data.groupby("Category")["Sales"].sum().idxmax()
                st.write(f"🏆 Best category: {best}")
            elif "trend" in q:
                st.write("📊 Sales trend depends on time range selected.")
            else:
                st.write("🤖 Try asking: sales, profit, best category, trend")

            st.markdown("</div>", unsafe_allow_html=True)
