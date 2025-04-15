import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

st.set_page_config(page_title="Retail Sales Dashboard", layout="wide")

# Load dataset
@st.cache_data
def load_data():
    df = pd.read_csv("Dataset.csv")

    # Clean and standardize column names
    df.columns = df.columns.str.strip().str.lower()

    # Show column names to help with debugging
    st.write("📋 Available Columns:", df.columns.tolist())

    # Convert dates and times safely
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

# Filters
st.sidebar.header("Filters")

branch_col = "branch"
product_line_col = "product line"

selected_branch = st.sidebar.multiselect(
    "Select Branch:",
    options=df[branch_col].unique() if branch_col in df.columns else [],
    default=df[branch_col].unique() if branch_col in df.columns else []
)

selected_product = st.sidebar.multiselect(
    "Select Product Line:",
    options=df[product_line_col].unique() if product_line_col in df.columns else [],
    default=df[product_line_col].unique() if product_line_col in df.columns else []
)

if selected_branch and selected_product:
    filtered_df = df[(df[branch_col].isin(selected_branch)) & (df[product_line_col].isin(selected_product))]
else:
    filtered_df = df.copy()

# KPIs
if not filtered_df.empty:
    total_sales = filtered_df["total"].sum() if "total" in filtered_df.columns else 0
    gross_income = filtered_df["gross income"].sum() if "gross income" in filtered_df.columns else 0
    avg_rating = filtered_df["rating"].mean() if "rating" in filtered_df.columns else 0

    col1, col2, col3 = st.columns(3)
    col1.metric("Total Sales", f"${total_sales:,.2f}")
    col2.metric("Gross Income", f"${gross_income:,.2f}")
    col3.metric("Average Rating", f"{avg_rating:.2f} ⭐")

    # Charts
    if "product" in filtered_df.columns:
        st.subheader("📊 Quantity Distribution")
        fig1, ax1 = plt.subplots()
        sns.countplot(data=filtered_df, x='Product', ax=ax1, palette='Set2')
        st.pyplot(fig1)

    if "date" in filtered_df.columns and "total" in filtered_df.columns:
        st.subheader("📈 Daily Sales Trend")
        daily_sales = filtered_df.groupby('date').agg({'total': 'sum'}).reset_index()
        fig2, ax2 = plt.subplots()
        sns.lineplot(data=daily_sales, x='date', y='total', ax=ax2)
        ax2.set_title("Total Sales Over Time")
        st.pyplot(fig2)

    if "product" in filtered_df.columns and "total" in filtered_df.columns:
        st.subheader("🏷️ Sales by Product Line")
        product_sales = filtered_df.groupby(product_line_col)['total'].sum().sort_values()
        fig3, ax3 = plt.subplots()
        product_sales.plot(kind='barh', ax=ax3, color='skyblue')
        ax3.set_xlabel("Total Sales")
        st.pyplot(fig3)

    if "price" in filtered_df.columns and "rating" in filtered_df.columns:
        st.subheader("💳 Ratings by Payment")
        fig4, ax4 = plt.subplots()
        sns.boxplot(data=filtered_df, x='Price', y='rating', palette='pastel', ax=ax4)
        st.pyplot(fig4)
else:
    st.warning("No data to display. Please check your filters or dataset.")
