# 💠 Enterprise Inventory Intelligence (EII)
### *Predictive DSS Architecture for Supply Chain Optimization*

<p align="left">
  <img src="https://img.shields.io/badge/Python-3.10%2B-blue?logo=python&logoColor=white" alt="Python">
  <img src="https://img.shields.io/badge/Framework-Streamlit-FF4B4B?logo=streamlit&logoColor=white" alt="Streamlit">
  <img src="https://img.shields.io/badge/ML-Scikit--Learn-F7931E?logo=scikitlearn&logoColor=white" alt="Scikit-Learn">
  <img src="https://img.shields.io/badge/Visuals-Plotly-3F4F75?logo=plotly&logoColor=white" alt="Plotly">
</p>

---

## 🏗️ System Architecture
**Enterprise Inventory Intelligence (EII)** is a sophisticated Decision Support System (DSS) engineered to transform raw transactional data into actionable executive heuristics. The system implements a reactive state-driven architecture to handle real-time data filtering, predictive modeling, and natural language querying.

### 🧩 Core Intelligence Modules
* **Predictive Engine:** Utilizes **Ordinary Least Squares (OLS) Regression** to map temporal vectors against sales velocity for multi-day demand forecasting.
* **Heuristic Risk Engine:** Implements a localized stress-test algorithm to calculate supply strain based on real-time inventory-to-demand ratios.
* **Neural Interface:** A deterministic NLP layer that parses user intent for natural language data querying (Sales, Profit, and Category metrics).
* **Glassmorphism UX:** Custom CSS-in-JS injection providing a high-fidelity, executive-grade dark interface with staggered animations.

---

## 🛠️ Technical Stack
| Layer | Technology | Implementation |
| :--- | :--- | :--- |
| **Frontend/UX** | **Streamlit** | Reactive SPA with custom CSS keyframe animations and Session State management. |
| **Data Logic** | **Pandas / NumPy** | Vectorized data processing, cleaning, and time-series resampling. |
| **ML Engine** | **Scikit-learn** | Linear Regression models for automated trend-line projection. |
| **Visual Analytics** | **Plotly Express** | Interactive SVG and WebGL-rendered financial matrices and trajectory charts. |

---

## 📂 Repository Framework
```text
.
├── .streamlit/             # Config and UI theme settings
├── app.py                  # Entry point & core business logic
├── requirements.txt        # Dependency manifest
├── Superstore.csv          # Normalized enterprise dataset
└── README.md               # Technical documentation
