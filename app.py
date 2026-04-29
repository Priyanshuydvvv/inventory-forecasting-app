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

# ================= PREMIUM STYLING =================
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }
    
    /* Sleek Dark Executive Theme */
    .stApp {
        background-color: #050505;
        color: #f8fafc;
    }
    
    /* Glassmorphism Cards */
    .glass-card {
        background: linear-gradient(145deg, rgba(30,41,59,0.4) 0%, rgba(15,23,42,0.4) 100%);
        backdrop-filter: blur(10px);
        -webkit-backdrop-filter: blur(10px);
        border: 1px solid rgba(255,255,255,0.05);
        border-radius: 16px;
        padding: 24px;
        box-shadow: 0 10px 30px -10px rgba(0,0,0,0.5);
        transition: transform 0.3s ease;
    }
    
    .glass-card:hover {
        transform: translateY(-2px);
        border: 1px solid rgba(255,255,255,0.1);
    }
    
    /* KPI Metrics */
    .metric-label {
        color: #94a3b8;
        font-size: 0.85rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        margin-bottom: 8px;
    }
    
    .metric-value {
        font-size: 2.5rem;
        font-weight: 800;
        background: linear-gradient(to right, #ffffff, #94a3b8);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        line-height: 1.2;
    }
    
    /* Gradient Text for Headers */
    .gradient-text {
        background: linear-gradient(135deg, #38bdf8 0%, #818cf8 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 800;
    }
    
    /* Customizing the Sidebar */
    [data-testid="stSidebar"] {
        background-color: #0a0a0a;
        border-right: 1px solid rgba(255,255,255,0.05);
    }
    
    hr {
        border-color: rgba(255,255,255,0.1);
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

# ================= AUTHENTICATION =================
if not st.session_state.auth:
    st.markdown("<br><br><br><br>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 1.2, 1])
    
    with col2:
        st.markdown(
            """
            <div style='text-align: center; margin-bottom: 2rem;'>
                <h1 class='gradient-text' style='font-size: 3rem;'>Sparkence Global</h1>
                <p style='color: #94a3b8; font-size: 1.1rem;'>Enterprise Inventory Intelligence</p>
            </div>
            """, 
            unsafe_allow_html=True
        )
        
        with st.form("login_form"):
            user = st.text_input("Executive ID", placeholder="Enter username")
            pwd = st.text_input("Access Token", type="password", placeholder="Enter password")
            submit = st.form_submit_button("Authenticate 🔒", use_container_width=True)
            
            if submit:
                if user == "admin" and pwd == "admin123":
                    st.session_state.auth = True
                    st.rerun()
                else:
                    st.error("Invalid credentials. Access denied.")
        
        st.caption("Demo Mode: admin / admin123")

# ================= MAIN APPLICATION =================
else:
    df = load_data()
    
    # --- SIDEBAR ---
    with st.sidebar:
        st.markdown("<h2 class='gradient-text'>System Control</h2>", unsafe_allow_html=True)
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
        if st.button("Logout 🚪", use_container_width=True):
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
            ("Total Orders", f"{len(data):,}"),
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
            st.markdown("#### Revenue Trajectory")
            monthly = data.set_index("Order Date").resample("MS")["Sales"].sum().reset_index()
            fig = px.area(monthly, x="Order Date", y="Sales", template="plotly_dark", 
                          color_discrete_sequence=["#38bdf8"])
            fig.update_layout(plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)", margin=dict(l=0, r=0, t=0, b=0))
            st.plotly_chart(fig, use_container_width=True)
            st.markdown("</div>", unsafe_allow_html=True)
            
        with col_chart2:
            st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
            st.markdown("#### Category Distribution")
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
            st.markdown("#### Top Performing Categories")
            cat_sales = data.groupby("Category")["Sales"].sum().reset_index().sort_values(by="Sales", ascending=True)
            fig = px.bar(cat_sales, x="Sales", y="Category", orientation='h', template="plotly_dark", color_discrete_sequence=["#818cf8"])
            fig.update_layout(plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)")
            st.plotly_chart(fig, use_container_width=True)
            
        with col2:
            st.markdown("#### Elite Product Registry")
            top_products = data.groupby("Product Name")["Sales"].sum().nlargest(10).reset_index()
            top_products["Sales"] = top_products["Sales"].apply(lambda x: f"${x:,.2f}")
            st.dataframe(top_products, use_container_width=True, hide_index=True)

    # 3. DEMAND FORECASTING
    elif page == "Demand Forecasting":
        st.markdown("## 📈 Predictive Demand Forecasting")
        st.markdown("Utilizing linear regression matrices to project future inventory burn rates.")
        
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
            fig.add_trace(go.Scatter(x=ts["Order Date"], y=ts["Sales"], mode='lines', name='Historical', line=dict(color='#94a3b8')))
            fig.add_trace(go.Scatter(x=future_dates, y=forecast, mode='lines', name='Projection', line=dict(color='#38bdf8', dash='dot')))
            
            fig.update_layout(template="plotly_dark", plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)",
                              hovermode="x unified", title=f"{cat} Trajectory")
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.warning("Insufficient data points in this timeframe to generate a reliable mathematical model.")

    # 4. RISK MONITORING
    elif page == "Risk Monitoring":
        st.markdown("## ⚠️ Inventory Risk Monitoring")
        
        col1, col2 = st.columns([1, 2])
        with col1:
            stock = st.number_input("Current Warehouse Capacity ($)", value=100000, step=10000)
            demand = data["Sales"].sum()
            risk_ratio = min(100, (demand / stock) * 100) if stock > 0 else 100
            
            status_color = "#10b981" if risk_ratio < 50 else "#f59e0b" if risk_ratio < 85 else "#ef4444"
            status_text = "Stable" if risk_ratio < 50 else "Warning" if risk_ratio < 85 else "Critical"
            
            st.markdown(f"### Status: <span style='color:{status_color}'>{status_text}</span>", unsafe_allow_html=True)
        
        with col2:
            fig = go.Figure(go.Indicator(
                mode = "gauge+number",
                value = risk_ratio,
                title = {'text': "Supply Chain Strain Index"},
                domain = {'x': [0, 1], 'y': [0, 1]},
                gauge = {
                    'axis': {'range': [None, 100], 'tickwidth': 1, 'tickcolor': "white"},
                    'bar': {'color': status_color},
                    'bgcolor': "rgba(255,255,255,0.1)",
                    'steps': [
                        {'range': [0, 50], 'color': "rgba(16, 185, 129, 0.2)"},
                        {'range': [50, 85], 'color': "rgba(245, 158, 11, 0.2)"},
                        {'range': [85, 100], 'color': "rgba(239, 68, 68, 0.2)"}],
                }
            ))
            fig.update_layout(template="plotly_dark", plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)", height=300)
            st.plotly_chart(fig, use_container_width=True)

    # 5. AI AGENT
    elif page == "AI Agent":
        st.markdown("## 🤖 Executive AI Agent")
        st.caption("Natural language querying for your enterprise datasets.")
        
        # Display chat messages from history
        for message in st.session_state.chat_history:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

        # Chat input
        if prompt := st.chat_input("Ask about sales, profit, or best categories..."):
            # Add user message
            st.session_state.chat_history.append({"role": "user", "content": prompt})
            with st.chat_message("user"):
                st.markdown(prompt)

            # Process AI response
            with st.chat_message("assistant"):
                with st.spinner("Analyzing matrices..."):
                    time.sleep(0.5) # Simulate processing
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
