import streamlit as st
import pandas as pd
from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt

st.set_page_config(
    page_title="Inventory Forecasting System",
    layout="wide"
)

data = pd.read_csv("Superstore.csv", encoding="latin1")
data["Order Date"] = pd.to_datetime(data["Order Date"])

st.sidebar.title("📦 Inventory Forecasting System")

st.sidebar.markdown("### Date Filter")
start_date = st.sidebar.date_input(
    "From",
    data["Order Date"].min()
)
end_date = st.sidebar.date_input(
    "To",
    data["Order Date"].max()
)

filtered_data = data[
    (data["Order Date"] >= pd.to_datetime(start_date)) &
    (data["Order Date"] <= pd.to_datetime(end_date))
]

page = st.sidebar.selectbox(
    "Navigation",
    ["Dashboard", "Forecasting", "Stock Alerts"]
)

if page == "Dashboard":
    st.markdown("## 📊 Sales & Inventory Overview")
    st.markdown(
        "This dashboard provides a high-level summary of sales performance "
        "and inventory-related insights based on the selected date range."
    )

    col1, col2, col3 = st.columns(3)
    col1.metric(
        "💰 Total Sales",
        f"{round(filtered_data['Sales'].sum(), 2)}"
    )
    col2.metric(
        "📈 Total Profit",
        f"{round(filtered_data['Profit'].sum(), 2)}"
    )
    col3.metric(
        "🧾 Total Orders",
        len(filtered_data)
    )

    st.markdown("### 🗂️ Sales by Product Category")
    category_sales = (
        filtered_data.groupby("Category")["Sales"].sum()
    )
    st.bar_chart(category_sales)

    st.markdown("### 🏆 Top 5 Best-Selling Products")
    top_products = (
        filtered_data
        .groupby("Product Name")["Sales"]
        .sum()
        .sort_values(ascending=False)
        .head(5)
    )
    st.table(top_products)

    st.markdown("### 📅 Monthly Sales Trend")
    monthly_sales = (
        filtered_data
        .set_index("Order Date")
        .resample("M")["Sales"]
        .sum()
    )
    st.line_chart(monthly_sales)

    st.download_button(
        "⬇️ Download Filtered Report",
        filtered_data.to_csv(index=False),
        "inventory_report.csv",
        "text/csv"
    )

elif page == "Forecasting":
    st.markdown("## 🤖 Demand Forecasting")
    st.markdown(
        "This section uses a simple machine learning model to predict "
        "future sales demand based on historical trends."
    )

    sales = (
        filtered_data
        .groupby("Order Date")["Sales"]
        .sum()
        .reset_index()
    )

    sales["day"] = range(len(sales))
    X = sales[["day"]]
    y = sales["Sales"]

    model = LinearRegression()
    model.fit(X, y)

    days = st.slider(
        "Select number of days to forecast",
        5,
        60,
        10
    )

    future_days = [
        [i] for i in range(len(sales), len(sales) + days)
    ]
    forecast = model.predict(future_days)

    st.markdown("### 📈 Forecast Visualization")
    plt.figure()
    plt.plot(
        sales["Sales"],
        label="Historical Sales"
    )
    plt.plot(
        range(len(sales), len(sales) + days),
        forecast,
        label="Forecasted Sales"
    )
    plt.legend()
    st.pyplot(plt)

    st.markdown("### 📊 Forecasted Values")
    st.write(forecast)

elif page == "Stock Alerts":
    st.markdown("## 🚨 Inventory Stock Monitoring")
    st.markdown(
        "This module checks whether current inventory levels are sufficient "
        "based on total sales within the selected period."
    )

    current_stock = st.number_input(
        "Enter current stock level",
        value=100000
    )

    total_sales = filtered_data["Sales"].sum()

    st.write("📦 Current Stock:", current_stock)
    st.write("📊 Total Sales:", total_sales)

    if total_sales > current_stock:
        st.error(
            "⚠️ Stock level is insufficient. Immediate replenishment is recommended."
        )
    else:
        st.success(
            "✅ Stock level is sufficient. No immediate action required."
        )
