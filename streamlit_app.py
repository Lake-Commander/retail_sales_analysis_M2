import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

st.set_page_config(page_title="Retail Sales Dashboard", layout="wide")

# Load dataset
@st.cache_data
def load_data():
    df = pd.read_csv("Dataset.csv")
    df.columns = df.columns.str.strip().str.lower()

    # Convert dates and times
    if "date" in df.columns:
        df['date'] = pd.to_datetime(df['date'], errors='coerce')
        df['day'] = df['date'].dt.day_name()
        df['month'] = df['date'].dt.month_name()
    if "time" in df.columns:
        df['time'] = pd.to_datetime(df['time'], errors='coerce').dt.time

    return df

df = load_data()

st.title("🛍️ Retail Sales Dashboard")
st.markdown("Explore key metrics and trends from a retail store's transaction dataset.")

# Sidebar filters
st.sidebar.header("Filters")
selected_branch = st.sidebar.multiselect("Select Branch:", df['branch'].unique(), default=df['branch'].unique())
selected_product = st.sidebar.multiselect("Select Product Line:", df['product line'].unique(), default=df['product line'].unique())

filtered_df = df[(df['branch'].isin(selected_branch)) & (df['product line'].isin(selected_product))]

# KPIs
if not filtered_df.empty:
    total_sales = filtered_df['total'].sum()
    gross_income = filtered_df['gross income'].sum()
    avg_rating = filtered_df['rating'].mean()

    col1, col2, col3 = st.columns(3)
    col1.metric("Total Sales", f"${total_sales:,.2f}")
    col2.metric("Gross Income", f"${gross_income:,.2f}")
    col3.metric("Average Rating", f"{avg_rating:.2f} ⭐")

    # Charts
    st.subheader("📊 Quantity Distribution")
    if 'product' in filtered_df.columns:
        fig1, ax1 = plt.subplots()
        sns.countplot(data=filtered_df, x='product', ax=ax1, palette='Set2')
        st.pyplot(fig1)

    st.subheader("📈 Daily Sales Trend")
    if "date" in filtered_df.columns:
        daily_sales = filtered_df.groupby('date')['total'].sum().reset_index()
        fig2, ax2 = plt.subplots()
        sns.lineplot(data=daily_sales, x='date', y='total', ax=ax2)
        ax2.set_title("Total Sales Over Time")
        st.pyplot(fig2)

    st.subheader("🏷️ Sales by Product Line")
    product_sales = filtered_df.groupby('product line')['total'].sum().sort_values()
    fig3, ax3 = plt.subplots()
    product_sales.plot(kind='barh', ax=ax3, color='skyblue')
    ax3.set_xlabel("Total Sales")
    st.pyplot(fig3)

    st.subheader("💳 Ratings by Price")
    if "price" in filtered_df.columns:
        fig4, ax4 = plt.subplots()
        sns.boxplot(data=filtered_df, x='price', y='rating', palette='pastel', ax=ax4)
        st.pyplot(fig4)
else:
    st.warning("No data to display. Please check your filters or dataset.")
