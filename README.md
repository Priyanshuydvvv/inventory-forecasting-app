<div align="center">

# 💠 Enterprise Inventory Intelligence (EII)
**A Predictive Decision Support System (DSS) for Supply Chain Optimization**

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://inventory-forecasting-app-hl3nekwuk5yu7w8rzu8kvl.streamlit.app)
[![Python 3.10+](https://img.shields.io/badge/Python-3.10%2B-blue?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![Machine Learning](https://img.shields.io/badge/ML-Scikit--Learn-F7931E?style=for-the-badge&logo=scikitlearn&logoColor=white)]()
[![Code Style: Black](https://img.shields.io/badge/Code%20Style-Black-000000.svg?style=for-the-badge)](https://github.com/psf/black)

*Bridging the gap between raw logistics data and heuristic executive action.*

</div>

---

## 📌 Executive Summary
**Enterprise Inventory Intelligence (EII)** is a reactive, state-driven web application designed to transform complex supply chain datasets into actionable insights. Utilizing a high-fidelity **Glassmorphism UI**, the system integrates machine learning forecasting, real-time risk assessment, and a deterministic NLP agent to streamline enterprise resource planning.

## 🏗️ System Architecture

*Architecture mapped via predictive data pipelines and reactive UI layers.*

```mermaid
flowchart LR
    %% Data Pipeline
    A[(Raw CSV Data)] -->|ETL Engine| B[Pandas & NumPy Processing]

    %% Intelligence Routing
    B --> C{Scikit-Learn ML}
    C -.->|OLS Regression| D[Demand Trajectory Projection]
    
    B --> E[Supply Strain Matrix]
    B --> F[NLP Keyword Parser]

    %% Presentation Synthesis
    D --> G[Plotly WebGL Graphics]
    E --> G
    F --> H[Neural Agent Interface]

    %% Final Output
    G ===> I(((💠 Executive Dashboard)))
    H ===> I(((💠 Executive Dashboard)))
