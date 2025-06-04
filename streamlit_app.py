import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Set page config
st.set_page_config(page_title="Retail Sales Dashboard", layout="wide")
sns.set_style("whitegrid")

# Load dataset
@st.cache_data
def load_data():
    df = pd.read_csv("Dataset.csv")
    df.columns = df.columns.str.strip().str.lower()
    df['date'] = pd.to_datetime(df['date'], errors='coerce')
    df['month'] = df['date'].dt.month_name()
    df['day'] = df['date'].dt.day_name()
    return df

df = load_data()

# Sidebar filters
st.sidebar.title("Filter Data")
selected_month = st.sidebar.multiselect(
    "Select Month(s):", options=df['month'].dropna().unique(), default=df['month'].dropna().unique()
)

filtered_df = df[df['month'].isin(selected_month)]

# Title
st.title("📊 Retail Sales Dashboard")
st.markdown("Analyze sales data to uncover insights and trends.")

# KPI section
total_sales = filtered_df['total'].sum()
total_orders = filtered_df['orderid'].nunique()
unique_customers = filtered_df['customerid'].nunique()

col1, col2, col3 = st.columns(3)
col1.metric("Total Sales ($)", f"{total_sales:,.2f}")
col2.metric("Total Orders", total_orders)
col3.metric("Unique Customers", unique_customers)

st.markdown("---")

# Sales Over Time
st.subheader("📈 Daily Sales Over Time")
daily_sales = filtered_df.groupby('date')['total'].sum().reset_index()

fig1, ax1 = plt.subplots(figsize=(10, 4))
sns.lineplot(data=daily_sales, x='date', y='total', ax=ax1, marker="o")
ax1.set_title("Daily Sales")
ax1.set_xlabel("Date")
ax1.set_ylabel("Total ($)")
st.pyplot(fig1)

# Top Products
st.subheader("🏆 Top 10 Products by Quantity Sold")
top_products = (
    filtered_df.groupby('product')['quantity'].sum()
    .sort_values(ascending=False).head(10)
)

fig2, ax2 = plt.subplots(figsize=(8, 4))
sns.barplot(x=top_products.values, y=top_products.index, palette="viridis", ax=ax2)
ax2.set_xlabel("Quantity Sold")
ax2.set_ylabel("Product")
st.pyplot(fig2)

# Monthly Sales
st.subheader("📅 Monthly Sales Distribution")
month_order = [
    'January', 'February', 'March', 'April', 'May', 'June', 'July',
    'August', 'September', 'October', 'November', 'December'
]
monthly_sales = (
    filtered_df.groupby('month')['total'].sum()
    .reindex(month_order).dropna()
)

fig3, ax3 = plt.subplots(figsize=(8, 4))
sns.barplot(x=monthly_sales.index, y=monthly_sales.values, palette="coolwarm", ax=ax3)
ax3.set_ylabel("Total Sales ($)")
ax3.set_xlabel("Month")
ax3.set_title("Monthly Sales")
plt.xticks(rotation=45)
st.pyplot(fig3)

# Customer Frequency
st.subheader("👤 Top 10 Customers by Number of Orders")
top_customers = filtered_df['customerid'].value_counts().head(10)

fig4, ax4 = plt.subplots(figsize=(8, 4))
sns.barplot(x=top_customers.values, y=top_customers.index, palette="Set3", ax=ax4)
ax4.set_xlabel("Number of Orders")
ax4.set_ylabel("Customer ID")
st.pyplot(fig4)

# Raw Data (Optional)
with st.expander("📄 View Raw Data"):
    st.dataframe(filtered_df)
