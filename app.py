import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from sklearn.linear_model import LinearRegression
from datetime import datetime, timedelta
import time

# ================= PAGE CONFIG =================
st.set_page_config(
    page_title="Enterprise Inventory Intelligence",
    page_icon="💠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ================= STATE MANAGEMENT =================
if "auth" not in st.session_state:
    st.session_state.auth = False
if "chat_history" not in st.session_state:
    st.session_state.chat_history = [
        {"role": "assistant", "content": "System initialized. Neural pathways active. How can I assist your executive decisions today?"}
    ]

# ================= FINAL BOSS STYLING =================
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }
    
    /* Animated Deep Space Background */
    .stApp {
        background: linear-gradient(-45deg, #020617, #0f172a, #020617, #1e1b4b);
        background-size: 400% 400%;
        animation: gradientBG 15s ease infinite;
        color: #f8fafc;
    }
    
    @keyframes gradientBG {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }
    
    /* Ultra-Premium Glassmorphism with Hover Glow */
    .glass-card {
        background: linear-gradient(145deg, rgba(15, 23, 42, 0.4) 0%, rgba(2, 6, 23, 0.7) 100%);
        backdrop-filter: blur(24px);
        -webkit-backdrop-filter: blur(24px);
        border: 1px solid rgba(255, 255, 255, 0.05);
        border-top: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 24px;
        padding: 32px;
        box-shadow: 0 25px 50px -12px rgba(0,0,0,0.5);
        transition: all 0.5s cubic-bezier(0.175, 0.885, 0.32, 1.275);
        position: relative;
        overflow: hidden;
    }
    
    .glass-card::before {
        content: "";
        position: absolute;
        top: 0; left: -100%; width: 50%; height: 100%;
        background: linear-gradient(to right, transparent, rgba(255,255,255,0.05), transparent);
        transform: skewX(-20deg);
        transition: 0.5s;
    }
    
    .glass-card:hover::before {
        left: 150%;
    }
    
    .glass-card:hover {
        transform: translateY(-8px) scale(1.01);
        box-shadow: 0 30px 60px -15px rgba(56, 189, 248, 0.2), 0 0 20px rgba(99, 102, 241, 0.1);
        border: 1px solid rgba(56, 189, 248, 0.3);
    }
    
    /* KPI Typography */
    .metric-label {
        color: #94a3b8;
        font-size: 0.75rem;
        font-weight: 800;
        text-transform: uppercase;
        letter-spacing: 0.2em;
        margin-bottom: 8px;
    }
    
    .metric-value {
        font-size: 3rem;
        font-weight: 900;
        background: linear-gradient(180deg, #ffffff 0%, #cbd5e1 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        line-height: 1.1;
        letter-spacing: -0.03em;
        text-shadow: 0 10px 20px rgba(0,0,0,0.5);
    }
    
    /* Hero Title Animation */
    .hero-container {
        animation: float 6s ease-in-out infinite;
    }
    
    @keyframes float {
        0% { transform: translateY(0px); }
        50% { transform: translateY(-10px); }
        100% { transform: translateY(0px); }
    }
    
    .gradient-text {
        background: linear-gradient(270deg, #38bdf8, #818cf8, #c084fc, #38bdf8);
        background-size: 200% 200%;
        animation: gradientShift 6s ease infinite;
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 900;
        font-size: clamp(2.5rem, 5vw, 4.5rem); 
        line-height: 1.2;
        padding-bottom: 0.2rem;
    }

    @keyframes gradientShift {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }

    /* Streamlit Input Overhauls */
    div[data-baseweb="input"] > div {
        background-color: rgba(15, 23, 42, 0.6) !important;
        backdrop-filter: blur(10px) !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        border-radius: 12px !important;
        transition: all 0.4s ease !important;
    }
    
    div[data-baseweb="input"] > div:focus-within {
        border-color: #38bdf8 !important;
        box-shadow: 0 0 25px rgba(56, 189, 248, 0.2), inset 0 0 10px rgba(56, 189, 248, 0.1) !important;
        background-color: rgba(15, 23, 42, 0.9) !important;
        transform: scale(1.02);
    }

    /* Button Physics */
    button[kind="primary"] {
        background: linear-gradient(135deg, #0ea5e9 0%, #4f46e5 100%) !important;
        border: none !important;
        border-radius: 12px !important;
        padding: 0.75rem 1.5rem !important;
        font-weight: 800 !important;
        letter-spacing: 1px !important;
        text-transform: uppercase !important;
        font-size: 0.9rem !important;
        box-shadow: 0 0 20px rgba(79, 70, 229, 0.4) !important;
        transition: all 0.3s cubic-bezier(0.175, 0.885, 0.32, 1.275) !important;
    }
    
    button[kind="primary"]:hover {
        transform: translateY(-3px) scale(1.02) !important;
        box-shadow: 0 15px 30px rgba(56, 189, 248, 0.6) !important;
        letter-spacing: 2px !important;
    }
    
    /* Sidebar Blur */
    [data-testid="stSidebar"] {
        background-color: rgba(2, 6, 23, 0.7) !important;
        backdrop-filter: blur(30px) !important;
        border-right: 1px solid rgba(255,255,255,0.05);
    }
    
    hr { border-color: rgba(255,255,255,0.05); }
    
    /* Cascading Staggered Animations */
    .stagger-1 { animation: fadeInUp 0.8s cubic-bezier(0.165, 0.84, 0.44, 1) 0.1s forwards; opacity: 0; }
    .stagger-2 { animation: fadeInUp 0.8s cubic-bezier(0.165, 0.84, 0.44, 1) 0.2s forwards; opacity: 0; }
    .stagger-3 { animation: fadeInUp 0.8s cubic-bezier(0.165, 0.84, 0.44, 1) 0.3s forwards; opacity: 0; }
    .stagger-4 { animation: fadeInUp 0.8s cubic-bezier(0.165, 0.84, 0.44, 1) 0.4s forwards; opacity: 0; }
    
    @keyframes fadeInUp {
        from { opacity: 0; transform: translateY(30px); }
        to { opacity: 1; transform: translateY(0); }
    }
</style>
""", unsafe_allow_html=True)

# ================= DATA LOADER (CACHED) =================
@st.cache_data
def load_data():
    try:
        df = pd.read_csv("Superstore.csv", encoding="latin1")
        df["Order Date"] = pd.to_datetime(df["Order Date"], errors="coerce")
        df = df.dropna(subset=["Order Date"])
    except FileNotFoundError:
        np.random.seed(42)
        dates = pd.date_range(start="2024-01-01", end="2025-12-31", freq="D")
        categories = ["Technology", "Furniture", "Office Supplies"]
        products = ["Enterprise Server", "Ergonomic Chair", "Optical Cable", "Cloud Storage Unit", "Executive Desk"]
        
        data = {
            "Order Date": np.random.choice(dates, 2000),
            "Category": np.random.choice(categories, 2000, p=[0.4, 0.3, 0.3]),
            "Product Name": np.random.choice(products, 2000),
            "Sales": np.random.uniform(50, 5000, 2000),
            "Profit": np.random.uniform(-50, 1500, 2000),
            "Quantity": np.random.randint(1, 10, 2000)
        }
        df = pd.DataFrame(data)
        df["Order Date"] = pd.to_datetime(df["Order Date"])
    return df

# ================= AUTHENTICATION PORTAL =================
if not st.session_state.auth:
    st.markdown("<br><br><br><br>", unsafe_allow_html=True)
    
    _, center_stage, _ = st.columns([0.5, 9, 0.5])
    
    with center_stage:
        st.markdown(
            """
            <div class='hero-container' style='text-align: center; margin-bottom: 2.5rem;'>
                <div class='stagger-1' style='display: inline-block; padding: 8px 20px; background: rgba(56, 189, 248, 0.05); border-radius: 50px; border: 1px solid rgba(56, 189, 248, 0.3); color: #38bdf8; font-size: 0.8rem; font-weight: 800; letter-spacing: 3px; text-transform: uppercase; margin-bottom: 1.5rem; box-shadow: 0 0 20px rgba(56, 189, 248, 0.2);'>
                    Secure Gateway
                </div>
                <div class='stagger-2 gradient-text'>Enterprise Inventory Intelligence</div>
                <p class='stagger-3' style='color: #64748b; font-size: 1.2rem; font-weight: 400; margin-top: 0.5rem; letter-spacing: 1px;'>Advanced Forecasting & Neural Analytics</p>
            </div>
            """, 
            unsafe_allow_html=True
        )
        
        _, form_col, _ = st.columns([1, 1.2, 1])
        
        with form_col:
            st.markdown("<div class='stagger-4'>", unsafe_allow_html=True)
            with st.form("login_form"):
                st.markdown("<div style='padding: 5px 0;'>", unsafe_allow_html=True)
                user = st.text_input("Access ID", placeholder="Enter authorization code")
                pwd = st.text_input("Security Token", type="password", placeholder="Enter biometric token")
                st.markdown("</div>", unsafe_allow_html=True)
                
                submit = st.form_submit_button("Initialize Systems ⚡", use_container_width=True)
                
                if submit:
                    if user == "admin" and pwd == "admin123":
                        st.session_state.auth = True
                        st.rerun()
                    else:
                        st.error("Authentication Failed. Breach detected.")
            
            st.markdown("<div style='text-align: center; margin-top: 1.5rem; color: #334155; font-size: 0.8rem; letter-spacing: 2px; text-transform: uppercase;'>Demo: admin / admin123</div>", unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)

# ================= MAIN APPLICATION =================
else:
    df = load_data()
    
    # --- SIDEBAR ---
    with st.sidebar:
        st.markdown("<h2 class='gradient-text' style='font-size: 1.5rem;'>Command Center</h2>", unsafe_allow_html=True)
        st.markdown("---")
        
        min_date = df["Order Date"].min().date()
        max_date = df["Order Date"].max().date()
        date_range = st.date_input("📅 Temporal Window", [min_date, max_date], min_value=min_date, max_value=max_date)
        
        if len(date_range) == 2:
            start_date, end_date = date_range
        else:
            start_date, end_date = min_date, max_date
            
        data = df[
            (df["Order Date"] >= pd.to_datetime(start_date)) & 
            (df["Order Date"] <= pd.to_datetime(end_date))
        ]
        
        st.markdown("---")
        page = st.radio(
            "🧭 Primary Modules",
            [
                "Executive Overview", 
                "Sales Intelligence", 
                "Demand Forecasting", 
                "Risk Monitoring", 
                "Neural Agent"
            ],
            label_visibility="collapsed"
        )
        
        st.markdown("---")
        if st.button("Sever Connection 🛑", use_container_width=True):
            st.session_state.auth = False
            st.rerun()

    if data.empty:
        st.warning("⚠️ No data available in this temporal sector.")
        st.stop()

    # --- ROUTING ---
    if page == "Executive Overview":
        st.markdown("<h2 class='stagger-1'>📊 Executive Overview</h2>", unsafe_allow_html=True)
        
        c1, c2, c3, c4 = st.columns(4)
        kpis = [
            ("Gross Revenue", f"${data['Sales'].sum():,.0f}"),
            ("Net Profit", f"${data['Profit'].sum():,.0f}"),
            ("Total Volume", f"{len(data):,}"),
            ("AOV", f"${data['Sales'].mean():,.0f}")
        ]
        
        # Apply staggering to cards
        staggers = ['stagger-1', 'stagger-2', 'stagger-3', 'stagger-4']
        for col, (label, value), stag in zip([c1, c2, c3, c4], kpis, staggers):
            col.markdown(f"""
                <div class='glass-card {stag}'>
                    <div class='metric-label'>{label}</div>
                    <div class='metric-value'>{value}</div>
                </div>
            """, unsafe_allow_html=True)
            
        st.markdown("<br>", unsafe_allow_html=True)
        
        col_chart1, col_chart2 = st.columns([2, 1])
        
        with col_chart1:
            st.markdown("<div class='glass-card stagger-3'>", unsafe_allow_html=True)
            st.markdown("<h4 style='margin-bottom: 1rem; color: #f8fafc;'>Revenue Trajectory</h4>", unsafe_allow_html=True)
            monthly = data.set_index("Order Date").resample("MS")["Sales"].sum().reset_index()
            fig = px.area(monthly, x="Order Date", y="Sales", template="plotly_dark", 
                          color_discrete_sequence=["#38bdf8"])
            fig.update_layout(plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)", margin=dict(l=0, r=0, t=0, b=0))
            st.plotly_chart(fig, use_container_width=True)
            st.markdown("</div>", unsafe_allow_html=True)
            
        with col_chart2:
            st.markdown("<div class='glass-card stagger-4'>", unsafe_allow_html=True)
            st.markdown("<h4 style='margin-bottom: 1rem; color: #f8fafc;'>Category Spread</h4>", unsafe_allow_html=True)
            cat_sales = data.groupby("Category")["Sales"].sum().reset_index()
            fig = px.pie(cat_sales, values='Sales', names='Category', hole=0.75, 
                         template="plotly_dark", color_discrete_sequence=["#38bdf8", "#818cf8", "#c084fc"])
            fig.update_layout(plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)", margin=dict(l=0, r=0, t=0, b=0), showlegend=False)
            # Add center text to donut
            fig.update_traces(textinfo='percent')
            st.plotly_chart(fig, use_container_width=True)
            st.markdown("</div>", unsafe_allow_html=True)

    elif page == "Sales Intelligence":
        st.markdown("<h2 class='stagger-1'>🎯 Sales Intelligence</h2>", unsafe_allow_html=True)
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("<div class='glass-card stagger-2'>", unsafe_allow_html=True)
            st.markdown("#### Top Performing Categories")
            cat_sales = data.groupby("Category")["Sales"].sum().reset_index().sort_values(by="Sales", ascending=True)
            fig = px.bar(cat_sales, x="Sales", y="Category", orientation='h', template="plotly_dark", color_discrete_sequence=["#818cf8"])
            fig.update_layout(plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)")
            st.plotly_chart(fig, use_container_width=True)
            st.markdown("</div>", unsafe_allow_html=True)
        with col2:
            st.markdown("<div class='glass-card stagger-3'>", unsafe_allow_html=True)
            st.markdown("#### Elite Product Registry")
            top_products = data.groupby("Product Name")["Sales"].sum().nlargest(10).reset_index()
            top_products["Sales"] = top_products["Sales"].apply(lambda x: f"${x:,.2f}")
            st.dataframe(top_products, use_container_width=True, hide_index=True)
            st.markdown("</div>", unsafe_allow_html=True)

    elif page == "Demand Forecasting":
        st.markdown("<h2 class='stagger-1'>📈 Predictive Forecasting</h2>", unsafe_allow_html=True)
        st.markdown("<div class='glass-card stagger-2'>", unsafe_allow_html=True)
        cat = st.selectbox("Select Target Category", data["Category"].unique())
        subset = data[data["Category"] == cat].copy()
        ts = subset.groupby("Order Date")["Sales"].sum().reset_index()
        ts = ts.sort_values("Order Date")
        ts["t"] = range(len(ts))
        
        if len(ts) > 2:
            model = LinearRegression()
            model.fit(ts[["t"]], ts["Sales"])
            days = st.slider("Forecast Horizon (Days)", 7, 120, 30)
            future_t = np.arange(len(ts), len(ts) + days).reshape(-1, 1)
            forecast = model.predict(future_t)
            last_date = ts["Order Date"].iloc[-1]
            future_dates = [last_date + timedelta(days=int(i)) for i in range(1, days + 1)]
            
            fig = go.Figure()
            fig.add_trace(go.Scatter(x=ts["Order Date"], y=ts["Sales"], mode='lines', name='Historical', line=dict(color='#64748b', width=2)))
            fig.add_trace(go.Scatter(x=future_dates, y=forecast, mode='lines', name='Projection', line=dict(color='#38bdf8', dash='dot', width=3)))
            fig.update_layout(template="plotly_dark", plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)", hovermode="x unified", title=f"{cat} Trajectory Matrix")
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.warning("Insufficient data vectors.")
        st.markdown("</div>", unsafe_allow_html=True)

    elif page == "Risk Monitoring":
        st.markdown("<h2 class='stagger-1'>⚠️ Risk Monitoring</h2>", unsafe_allow_html=True)
        st.markdown("<div class='glass-card stagger-2'>", unsafe_allow_html=True)
        col1, col2 = st.columns([1, 2])
        with col1:
            stock = st.number_input("Warehouse Capacity ($)", value=100000, step=10000)
            demand = data["Sales"].sum()
            risk_ratio = min(100, (demand / stock) * 100) if stock > 0 else 100
            status_color = "#10b981" if risk_ratio < 50 else "#f59e0b" if risk_ratio < 85 else "#ef4444"
            status_text = "Stable" if risk_ratio < 50 else "Warning" if risk_ratio < 85 else "Critical"
            st.markdown(f"### Status Matrix: <br><span style='color:{status_color}; font-size: 2.5rem; font-weight: 900; text-shadow: 0 0 20px {status_color}80;'>{status_text}</span>", unsafe_allow_html=True)
        with col2:
            fig = go.Figure(go.Indicator(
                mode = "gauge+number",
                value = risk_ratio,
                title = {'text': "Supply Strain", 'font': {'color': '#94a3b8'}},
                domain = {'x': [0, 1], 'y': [0, 1]},
                gauge = {
                    'axis': {'range': [None, 100], 'tickwidth': 1, 'tickcolor': "#475569"},
                    'bar': {'color': status_color},
                    'bgcolor': "rgba(255,255,255,0.02)",
                    'steps': [
                        {'range': [0, 50], 'color': "rgba(16, 185, 129, 0.1)"},
                        {'range': [50, 85], 'color': "rgba(245, 158, 11, 0.1)"},
                        {'range': [85, 100], 'color': "rgba(239, 68, 68, 0.1)"}],
                }
            ))
            fig.update_layout(template="plotly_dark", plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)", height=300)
            st.plotly_chart(fig, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

    elif page == "Neural Agent":
        st.markdown("<h2 class='stagger-1'>🤖 Neural Agent</h2>", unsafe_allow_html=True)
        st.markdown("<div class='glass-card stagger-2' style='min-height: 500px;'>", unsafe_allow_html=True)
        for message in st.session_state.chat_history:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

        if prompt := st.chat_input("Query the mainframe..."):
            st.session_state.chat_history.append({"role": "user", "content": prompt})
            with st.chat_message("user"):
                st.markdown(prompt)

            with st.chat_message("assistant"):
                with st.spinner("Processing neural pathways..."):
                    time.sleep(0.8)
                    q = prompt.lower()
                    if "sales" in q: response = f"Based on the current window, gross sales volume is **${data['Sales'].sum():,.2f}**."
                    elif "profit" in q: response = f"Current net profit margins stand at **${data['Profit'].sum():,.2f}**."
                    elif "category" in q: 
                        best = data.groupby("Category")["Sales"].sum().idxmax()
                        response = f"The leading product vertical is currently **{best}**."
                    else: response = "I am optimized to analyze metrics regarding **sales**, **profit**, and **category performance**. Please specify your query parameters."
                    st.markdown(response)
                    st.session_state.chat_history.append({"role": "assistant", "content": response})
        st.markdown("</div>", unsafe_allow_html=True)
