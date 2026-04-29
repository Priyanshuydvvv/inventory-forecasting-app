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
        {"role": "assistant", "content": "Welcome to the Executive AI Assistant. How can I analyze the data for you today?"}
    ]

# ================= HYPER-ADVANCED STYLING =================
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }
    
    /* Sleek Deep Dark Theme */
    .stApp {
        background-color: #030712;
        background-image: radial-gradient(circle at 50% 0%, rgba(30, 58, 138, 0.15) 0%, transparent 50%);
        color: #f8fafc;
    }
    
    /* Premium Glassmorphism Cards */
    .glass-card {
        background: linear-gradient(145deg, rgba(17, 24, 39, 0.7) 0%, rgba(3, 7, 18, 0.9) 100%);
        backdrop-filter: blur(16px);
        -webkit-backdrop-filter: blur(16px);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-top: 1px solid rgba(255, 255, 255, 0.15);
        border-radius: 20px;
        padding: 28px;
        box-shadow: 0 20px 40px -15px rgba(0,0,0,0.7);
        transition: transform 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275), box-shadow 0.4s ease;
    }
    
    .glass-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 30px 60px -20px rgba(56, 189, 248, 0.15);
        border-top: 1px solid rgba(56, 189, 248, 0.3);
    }
    
    /* Advanced KPI Metrics */
    .metric-label {
        color: #64748b;
        font-size: 0.75rem;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.1em;
        margin-bottom: 12px;
    }
    
    .metric-value {
        font-size: 2.8rem;
        font-weight: 900;
        background: linear-gradient(180deg, #ffffff 0%, #cbd5e1 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        line-height: 1.1;
        letter-spacing: -0.02em;
    }
    
    /* Typography & Gradients */
    .gradient-text {
        background: linear-gradient(135deg, #38bdf8 0%, #6366f1 50%, #c084fc 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 900;
    }

    /* Streamlit Input Enhancements */
    div[data-baseweb="input"] > div {
        background-color: rgba(15, 23, 42, 0.6) !important;
        border: 1px solid rgba(255, 255, 255, 0.05) !important;
        border-radius: 12px !important;
        transition: all 0.3s ease !important;
    }
    
    div[data-baseweb="input"] > div:focus-within {
        border-color: #38bdf8 !important;
        box-shadow: 0 0 20px rgba(56, 189, 248, 0.15) !important;
        background-color: rgba(15, 23, 42, 0.9) !important;
    }

    /* Streamlit Primary Button Overhaul */
    button[kind="primary"] {
        background: linear-gradient(135deg, #0ea5e9 0%, #4f46e5 100%) !important;
        border: none !important;
        border-radius: 12px !important;
        padding: 0.75rem 1.5rem !important;
        font-weight: 600 !important;
        letter-spacing: 0.5px !important;
        box-shadow: 0 10px 20px -10px rgba(79, 70, 229, 0.6) !important;
        transition: all 0.3s ease !important;
    }
    
    button[kind="primary"]:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 15px 25px -10px rgba(79, 70, 229, 0.8) !important;
    }
    
    /* Sidebar Customization */
    [data-testid="stSidebar"] {
        background-color: rgba(10, 10, 10, 0.8) !important;
        backdrop-filter: blur(20px);
        border-right: 1px solid rgba(255,255,255,0.05);
    }
    
    hr {
        border-color: rgba(255,255,255,0.05);
    }
    
    /* Animations */
    @keyframes fadeInDown {
        from { opacity: 0; transform: translateY(-20px); }
        to { opacity: 1; transform: translateY(0); }
    }
    .fade-in-down {
        animation: fadeInDown 0.8s cubic-bezier(0.165, 0.84, 0.44, 1) forwards;
    }
</style>
""", unsafe_allow_html=True)

# ================= DATA LOADER (CACHED) =================
@st.cache_data
def load_data():
    try:
        # Try to load real data
        df = pd.read_csv("Superstore.csv", encoding="latin1")
        df["Order Date"] = pd.to_datetime(df["Order Date"], errors="coerce")
        df = df.dropna(subset=["Order Date"])
    except FileNotFoundError:
        # Robust Fallback: Generate synthetic enterprise data if CSV is missing on GitHub
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
    
    # Widened the center column to [1, 2.5, 1] so the text fits on one line
    col1, col2, col3 = st.columns([1, 2.5, 1])
    
    with col2:
        st.markdown(
            """
            <div class='fade-in-down' style='text-align: center; margin-bottom: 2.5rem;'>
                <div style='display: inline-block; padding: 6px 16px; background: rgba(56, 189, 248, 0.1); border-radius: 50px; border: 1px solid rgba(56, 189, 248, 0.2); color: #38bdf8; font-size: 0.75rem; font-weight: 700; letter-spacing: 2px; text-transform: uppercase; margin-bottom: 1.5rem;'>
                    System Locked
                </div>
                <h1 class='gradient-text' style='font-size: 3.5rem; line-height: 1.1; margin-bottom: 1rem; white-space: nowrap;'>Enterprise Inventory Intelligence</h1>
                <p style='color: #64748b; font-size: 1.1rem; font-weight: 400;'>Advanced Forecasting & Analytics Terminal</p>
            </div>
            """, 
            unsafe_allow_html=True
        )
        
        # Added nested columns to keep the login form a nice compact width inside the wider column
        _, form_col, _ = st.columns([1, 2, 1])
        with form_col:
            with st.form("login_form"):
                st.markdown("<div style='padding: 10px 0;'>", unsafe_allow_html=True)
                user = st.text_input("Access ID", placeholder="Enter your credentials")
                pwd = st.text_input("Security Token", type="password", placeholder="Enter your token")
                st.markdown("</div>", unsafe_allow_html=True)
                
                submit = st.form_submit_button("Initialize Session ⚡", use_container_width=True)
                
                if submit:
                    if user == "admin" and pwd == "admin123":
                        st.session_state.auth = True
                        st.rerun()
                    else:
                        st.error("Authentication Failed. Invalid credentials.")
            
            st.markdown("<div style='text-align: center; margin-top: 1rem; color: #475569; font-size: 0.85rem;'>Demo Credentials: admin / admin123</div>", unsafe_allow_html=True)

# ================= MAIN APPLICATION =================
else:
    df = load_data()
    
    # --- SIDEBAR ---
    with st.sidebar:
        st.markdown("<h2 class='gradient-text'>Control Panel</h2>", unsafe_allow_html=True)
        st.markdown("---")
        
        # Global Date Filter
        min_date = df["Order Date"].min().date()
        max_date = df["Order Date"].max().date()
        date_range = st.date_input("📅 Operations Window", [min_date, max_date], min_value=min_date, max_value=max_date)
        
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
            "🧭 Navigation Modules",
            [
                "Executive Overview", 
                "Sales Intelligence", 
                "Demand Forecasting", 
                "Risk Monitoring", 
                "AI Agent"
            ],
            label_visibility="collapsed"
        )
        
        st.markdown("---")
        if st.button("End Session 🔒", use_container_width=True):
            st.session_state.auth = False
            st.rerun()

    if data.empty:
        st.warning("⚠️ No data available for the selected timeframe.")
        st.stop()

    # --- ROUTING ---
    # 1. EXECUTIVE OVERVIEW
    if page == "Executive Overview":
        st.markdown("## 📊 Executive Overview")
        
        # Top KPI Cards
        c1, c2, c3, c4 = st.columns(4)
        kpis = [
            ("Gross Revenue", f"${data['Sales'].sum():,.0f}"),
            ("Net Profit", f"${data['Profit'].sum():,.0f}"),
            ("Total Volume", f"{len(data):,}"),
            ("AOV", f"${data['Sales'].mean():,.0f}")
        ]
        
        for col, (label, value) in zip([c1, c2, c3, c4], kpis):
            col.markdown(f"""
                <div class='glass-card'>
                    <div class='metric-label'>{label}</div>
                    <div class='metric-value'>{value}</div>
                </div>
            """, unsafe_allow_html=True)
            
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Charts Row
        col_chart1, col_chart2 = st.columns([2, 1])
        
        with col_chart1:
            st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
            st.markdown("<h4 style='margin-bottom: 1rem;'>Revenue Trajectory</h4>", unsafe_allow_html=True)
            monthly = data.set_index("Order Date").resample("MS")["Sales"].sum().reset_index()
            fig = px.area(monthly, x="Order Date", y="Sales", template="plotly_dark", 
                          color_discrete_sequence=["#38bdf8"])
            fig.update_layout(plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)", margin=dict(l=0, r=0, t=0, b=0))
            st.plotly_chart(fig, use_container_width=True)
            st.markdown("</div>", unsafe_allow_html=True)
            
        with col_chart2:
            st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
            st.markdown("<h4 style='margin-bottom: 1rem;'>Category Distribution</h4>", unsafe_allow_html=True)
            cat_sales = data.groupby("Category")["Sales"].sum().reset_index()
            fig = px.pie(cat_sales, values='Sales', names='Category', hole=0.7, 
                         template="plotly_dark", color_discrete_sequence=["#38bdf8", "#818cf8", "#c084fc"])
            fig.update_layout(plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)", margin=dict(l=0, r=0, t=0, b=0), showlegend=False)
            st.plotly_chart(fig, use_container_width=True)
            st.markdown("</div>", unsafe_allow_html=True)

    # 2. SALES INTELLIGENCE
    elif page == "Sales Intelligence":
        st.markdown("## 🎯 Sales Intelligence")
        
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
            st.markdown("#### Top Performing Categories")
            cat_sales = data.groupby("Category")["Sales"].sum().reset_index().sort_values(by="Sales", ascending=True)
            fig = px.bar(cat_sales, x="Sales", y="Category", orientation='h', template="plotly_dark", color_discrete_sequence=["#818cf8"])
            fig.update_layout(plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)")
            st.plotly_chart(fig, use_container_width=True)
            st.markdown("</div>", unsafe_allow_html=True)
            
        with col2:
            st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
            st.markdown("#### Elite Product Registry")
            top_products = data.groupby("Product Name")["Sales"].sum().nlargest(10).reset_index()
            top_products["Sales"] = top_products["Sales"].apply(lambda x: f"${x:,.2f}")
            st.dataframe(top_products, use_container_width=True, hide_index=True)
            st.markdown("</div>", unsafe_allow_html=True)

    # 3. DEMAND FORECASTING
    elif page == "Demand Forecasting":
        st.markdown("## 📈 Predictive Demand Forecasting")
        st.markdown("Utilizing linear regression matrices to project future inventory burn rates.")
        
        st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
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
            
            # Create Future Dates
            last_date = ts["Order Date"].iloc[-1]
            future_dates = [last_date + timedelta(days=int(i)) for i in range(1, days + 1)]
            
            fig = go.Figure()
            fig.add_trace(go.Scatter(x=ts["Order Date"], y=ts["Sales"], mode='lines', name='Historical', line=dict(color='#64748b', width=2)))
            fig.add_trace(go.Scatter(x=future_dates, y=forecast, mode='lines', name='Projection', line=dict(color='#38bdf8', dash='dot', width=3)))
            
            fig.update_layout(template="plotly_dark", plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)",
                              hovermode="x unified", title=f"{cat} Trajectory Matrix")
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.warning("Insufficient data points in this timeframe to generate a reliable mathematical model.")
        st.markdown("</div>", unsafe_allow_html=True)

    # 4. RISK MONITORING
    elif page == "Risk Monitoring":
        st.markdown("## ⚠️ Inventory Risk Monitoring")
        
        st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
        col1, col2 = st.columns([1, 2])
        with col1:
            stock = st.number_input("Current Warehouse Capacity ($)", value=100000, step=10000)
            demand = data["Sales"].sum()
            risk_ratio = min(100, (demand / stock) * 100) if stock > 0 else 100
            
            status_color = "#10b981" if risk_ratio < 50 else "#f59e0b" if risk_ratio < 85 else "#ef4444"
            status_text = "Stable" if risk_ratio < 50 else "Warning" if risk_ratio < 85 else "Critical"
            
            st.markdown(f"### Status Matrix: <br><span style='color:{status_color}; font-size: 2.5rem; font-weight: 800;'>{status_text}</span>", unsafe_allow_html=True)
        
        with col2:
            fig = go.Figure(go.Indicator(
                mode = "gauge+number",
                value = risk_ratio,
                title = {'text': "Supply Chain Strain Index", 'font': {'color': '#94a3b8'}},
                domain = {'x': [0, 1], 'y': [0, 1]},
                gauge = {
                    'axis': {'range': [None, 100], 'tickwidth': 1, 'tickcolor': "#475569"},
                    'bar': {'color': status_color},
                    'bgcolor': "rgba(255,255,255,0.05)",
                    'steps': [
                        {'range': [0, 50], 'color': "rgba(16, 185, 129, 0.15)"},
                        {'range': [50, 85], 'color': "rgba(245, 158, 11, 0.15)"},
                        {'range': [85, 100], 'color': "rgba(239, 68, 68, 0.15)"}],
                }
            ))
            fig.update_layout(template="plotly_dark", plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)", height=300)
            st.plotly_chart(fig, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

    # 5. AI AGENT
    elif page == "AI Agent":
        st.markdown("## 🤖 Neural Decision Agent")
        st.caption("Natural language querying for your enterprise datasets.")
        
        st.markdown("<div class='glass-card' style='min-height: 400px;'>", unsafe_allow_html=True)
        # Display chat messages from history
        for message in st.session_state.chat_history:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

        # Chat input
        if prompt := st.chat_input("Query the system (e.g., 'What is the top category?')..."):
            # Add user message
            st.session_state.chat_history.append({"role": "user", "content": prompt})
            with st.chat_message("user"):
                st.markdown(prompt)

            # Process AI response
            with st.chat_message("assistant"):
                with st.spinner("Processing data matrices..."):
                    time.sleep(0.6) # Simulate processing
                    q = prompt.lower()
                    
                    if "sales" in q:
                        response = f"Based on the current window, gross sales volume is **${data['Sales'].sum():,.2f}**."
                    elif "profit" in q:
                        response = f"Current net profit margins stand at **${data['Profit'].sum():,.2f}**."
                    elif "best category" in q or "top category" in q:
                        best = data.groupby("Category")["Sales"].sum().idxmax()
                        response = f"The leading product vertical is currently **{best}**."
                    elif "trend" in q:
                        response = "The data indicates seasonal clustering. I recommend reviewing the Demand Forecasting module for 30-day linear projections."
                    else:
                        response = "I am currently optimized to analyze metrics regarding **sales**, **profit**, **trends**, and **category performance**. Please specify your query."
                    
                    st.markdown(response)
                    st.session_state.chat_history.append({"role": "assistant", "content": response})
        st.markdown("</div>", unsafe_allow_html=True)
