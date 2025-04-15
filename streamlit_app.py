import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

st.set_page_config(page_title="Retail Sales Dashboard", layout="wide")

# Load dataset
@st.cache_data
def load_data():
    df = pd.read_csv("Dataset.csv")

    # Clean column names
    df.columns = df.columns.str.strip()

    # Display available columns for debugging
    st.write("📋 Available Columns:", df.columns.tolist())

    # Handle date and time if they exist
    if "Date" in df.columns:
        df['Date'] = pd.to_datetime(df['Date'])
        df['Day'] = df['Date'].dt.day_name()
        df['Month'] = df['Date'].dt.month_name()
    if "Time" in df.columns:
        df['Time'] = pd.to_datetime(df['Time'], errors='coerce').dt.time

    return df

df = load_data()

st.title("🛍️ Retail Sales Dashboard")
st.markdown("Explore key metrics and trends from a retail store's transaction dataset.")

# Filters
st.sidebar.header("Filters")

if "Branch" in df.columns:
    selected_branch = st.sidebar.multiselect(
        "Select Branch:", options=df["Branch"].unique(), default=df["Branch"].unique()
    )
else:
    selected_branch = []

if "Product line" in df.columns:
    selected_product = st.sidebar.multiselect(
        "Select Product Line:", options=df["Product line"].unique(), default=df["Product line"].unique()
    )
else:
    selected_product = []

if selected_branch and selected_product:
    filtered_df = df[(df["Branch"].isin(selected_branch)) & (df["Product line"].isin(selected_product))]
else:
    filtered_df = df.copy()

# KPI row
if not filtered_df.empty:
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Sales", f"${filtered_df['Total'].sum():,.2f}")
    col2.metric("Gross Income", f"${filtered_df['gross income'].sum():,.2f}")
    col3.metric("Average Rating", f"{filtered_df['Rating'].mean():.2f} ⭐")

    # Charts
    st.subheader("📊 Gender Distribution")
    fig1, ax1 = plt.subplots()
    sns.countplot(data=filtered_df, x='Gender', ax=ax1, palette='Set2')
    st.pyplot(fig1)

    st.subheader("📈 Daily Sales Trend")
    if "Date" in filtered_df.columns:
        daily_sales = filtered_df.groupby('Date').agg({'Total':'sum'}).reset_index()
        fig2, ax2 = plt.subplots()
        sns.lineplot(data=daily_sales, x='Date', y='Total', ax=ax2)
        ax2.set_title("Total Sales Over Time")
        st.pyplot(fig2)

    st.subheader("🏷️ Sales by Product Line")
    product_sales = filtered_df.groupby('Product line')['Total'].sum().sort_values()
    fig3, ax3 = plt.subplots()
    product_sales.plot(kind='barh', ax=ax3, color='skyblue')
    ax3.set_xlabel("Total Sales")
    st.pyplot(fig3)

    st.subheader("💳 Ratings by Payment Method")
    fig4, ax4 = plt.subplots()
    sns.boxplot(data=filtered_df, x='Payment', y='Rating', palette='pastel', ax=ax4)
    st.pyplot(fig4)
else:
    st.warning("No data to display. Please check your filters or dataset.")
