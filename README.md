# <p align="center">💠 ENTERPRISE INVENTORY INTELLIGENCE</p>

<p align="center">
  <img src="https://img.shields.io/badge/FRAMEWORK-STREAMLIT-FF4B4B?style=for-the-badge&logo=streamlit" alt="Streamlit">
  <img src="https://img.shields.io/badge/ANALYSIS-PANDAS-150458?style=for-the-badge&logo=pandas" alt="Pandas">
  <img src="https://img.shields.io/badge/ML-SKLEARN_REGRESSION-F7931E?style=for-the-badge&logo=scikitlearn" alt="Sklearn">
</p>

---

## 🏛️ ARCHITECTURAL OVERVIEW

**Enterprise Inventory Intelligence** is a decision-support system engineered to transform retail data into executive-level insights. The application utilizes a reactive state-machine architecture to process complex datasets and deliver predictive analytics through a custom-styled, high-fidelity interface.

### 🧬 INTEGRATED TECH STACK
* **Frontend Engine:** `Streamlit` with custom CSS3 glassmorphism and hardware-accelerated animations.
* **Data Processing:** `Pandas` & `NumPy` for vectorized data manipulation and resampling.
* **Predictive Modeling:** `Scikit-Learn` implementation of Linear Regression for time-series forecasting.
* **Visualization:** `Plotly Express` and `Graph Objects` for interactive WebGL-rendered telemetry.

---

## 🛠️ TECHNICAL SYSTEM MODULES

### 📊 **01 | Executive Command Center**
Aggregates macro-level KPIs including Gross Revenue, Net Profit, and Total Volume.
* **Resampling Logic:** Utilizes `.resample("MS")` for temporal revenue trajectory mapping.
* **Visuals:** Area charts and high-hole-ratio donut charts for category distribution.

### 🎯 **02 | Sales Intelligence Registry**
Deep-dives into product performance using grouped aggregations.
* **Elite Product Registry:** Dynamic extraction of the Top 10 products by sales volume using `.nlargest()`.
* **Horizontal Analytics:** Category-wise performance ranking via interactive bar visualizations.

### 📈 **03 | Predictive Forecasting Matrix**
A statistical inference module used to model future sales velocity.
* **Algorithm:** Ordinary Least Squares (OLS) Linear Regression.
* **Temporal Scaling:** Maps `Order Date` to a scalar `t` to project demand up to 120 days.
* **Equation:** $$Y = \beta_0 + \beta_1(t) + \epsilon$$

### ⚠️ **04 | Supply Risk Heuristics**
Evaluates warehouse health by calculating the **Supply Strain Ratio**.
* **Logic:** Computes `(Current Demand / User-Defined Capacity) * 100`.
* **Alert System:** Triple-tier threshold monitoring (Stable, Warning, Critical) rendered through real-time Gauge indicators.

### 🤖 **05 | Neural Decision Agent**
A state-aware interface facilitating natural language querying.
* **State Management:** Persists interaction data via `st.session_state.chat_history`.
* **Inference Gate:** Parses string inputs to return real-time aggregates for Profit, Sales, and Category leaders.

---

## 🏗️ INSTALLATION & BOOT PROTOCOL

###  Environment Synchronization
```bash
git clone [https://github.com/your-username/enterprise-inventory-intelligence.git](https://github.com/your-username/enterprise-inventory-intelligence.git)
cd enterprise-inventory-intelligence
2. Dependency Manifest
Bash
pip install streamlit pandas numpy plotly scikit-learn
3. System Initialization
Bash
streamlit run app.py
🔐 ACCESS GATEWAY
The application implements a custom authentication layer via Streamlit Session State.

Access ID: admin

Security Token: admin123
