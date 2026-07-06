import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Business Dashboard", layout="wide")

st.title("📊 Advanced Sales Dashboard")

# ------------------------
# 📂 LOAD DATA
# ------------------------
sales_file = "SalesDataset.xlsx"
customer_file = "CustomerDataset.xlsx"
product_file = "ProductDataset.xlsx"

sales = pd.read_excel(sales_file, sheet_name="Sheet1")
customers = pd.read_excel(customer_file, sheet_name="Sheet1")
products = pd.read_excel(product_file, sheet_name="Sheet1")

# ------------------------
# 🔗 MERGE DATA
# ------------------------
df = sales.merge(customers, on="Customer_ID").merge(products, on="Product_ID")

df["Sale_Date"] = pd.to_datetime(df["Sale_Date"])

# ------------------------
# 🎛️ SIDEBAR FILTERS
# ------------------------
st.sidebar.header("Filters")

# Date filter
start_date = st.sidebar.date_input("Start Date", df["Sale_Date"].min())
end_date = st.sidebar.date_input("End Date", df["Sale_Date"].max())

# Region filter
region = st.sidebar.multiselect("Region", df["Region"].unique(), default=df["Region"].unique())

# Segment filter
segment = st.sidebar.multiselect("Customer Segment", df["Segment"].unique(), default=df["Segment"].unique())

# Category filter
category = st.sidebar.multiselect("Product Category", df["Category"].unique(), default=df["Category"].unique())

filtered_df = df[
    (df["Sale_Date"] >= pd.to_datetime(start_date)) &
    (df["Sale_Date"] <= pd.to_datetime(end_date)) &
    (df["Region"].isin(region)) &
    (df["Segment"].isin(segment)) &
    (df["Category"].isin(category))
]

# ------------------------
# 📊 KPI SECTION
# ------------------------
total_sales = filtered_df["Sales_Amount"].sum()
total_profit = filtered_df["Profit"].sum()
orders = filtered_df["Sale_ID"].nunique()
customers_count = filtered_df["Customer_ID"].nunique()
avg_order_value = total_sales / orders if orders != 0 else 0

col1, col2, col3, col4, col5 = st.columns(5)

col1.metric("💰 Sales", f"{total_sales:,.0f}")
col2.metric("📈 Profit", f"{total_profit:,.0f}")
col3.metric("🧾 Orders", orders)
col4.metric("👥 Customers", customers_count)
col5.metric("💳 Avg Order", f"{avg_order_value:,.0f}")

# ------------------------
# 📈 SALES TREND
# ------------------------
trend = filtered_df.groupby(filtered_df["Sale_Date"].dt.to_period("M"))["Sales_Amount"].sum().reset_index()
trend["Sale_Date"] = trend["Sale_Date"].astype(str)

fig1 = px.line(trend, x="Sale_Date", y="Sales_Amount",
               title="📈 Monthly Sales Trend", markers=True)

# ------------------------
# 🏆 TOP PRODUCTS
# ------------------------
top_products = filtered_df.groupby("Product_Name")["Sales_Amount"].sum().nlargest(10).reset_index()

fig2 = px.bar(top_products, x="Sales_Amount", y="Product_Name",
              orientation="h", title="🏆 Top Products")

# ------------------------
# 🌍 REGION ANALYSIS
# ------------------------
region_sales = filtered_df.groupby("Region")["Sales_Amount"].sum().reset_index()

fig3 = px.pie(region_sales, names="Region", values="Sales_Amount",
              title="🌍 Sales by Region")

# ------------------------
# 👥 CUSTOMER SEGMENT
# ------------------------
segment_sales = filtered_df.groupby("Segment")["Sales_Amount"].sum().reset_index()

fig4 = px.bar(segment_sales, x="Segment", y="Sales_Amount",
              title="👥 Sales by Customer Segment")

# ------------------------
# 📊 CATEGORY ANALYSIS
# ------------------------
category_sales = filtered_df.groupby("Category")["Sales_Amount"].sum().reset_index()

fig5 = px.bar(category_sales, x="Category", y="Sales_Amount",
              title="📦 Sales by Category")

# ------------------------
# 📊 LAYOUT
# ------------------------
col6, col7 = st.columns(2)
col6.plotly_chart(fig1, use_container_width=True)
col7.plotly_chart(fig2, use_container_width=True)

col8, col9 = st.columns(2)
col8.plotly_chart(fig3, use_container_width=True)
col9.plotly_chart(fig4, use_container_width=True)

st.plotly_chart(fig5, use_container_width=True)

# ------------------------
# 📋 DATA TABLE
# ------------------------
st.subheader("📋 Detailed Data")
st.dataframe(filtered_df)