import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

# Load data
data = pd.read_csv('large_product_sales_data.csv')
data['Date'] = pd.to_datetime(data['Date'])

# Set the page configuration
st.set_page_config(
    page_title="Product Sales Dashboard", 
    page_icon="📊", 
    layout="wide"
)

# Add some title and description
st.title("📊 Product Sales Dashboard")
st.markdown("""
This dashboard provides insights into product sales, customer interactions, and the effectiveness of marketing strategies. 
Use the interactive filters below to explore the data in various ways.
""")

# Sidebar filters for user interactivity
st.sidebar.header("Filter Data")
start_date = st.sidebar.date_input('Start Date', data['Date'].min())
end_date = st.sidebar.date_input('End Date', data['Date'].max())
selected_product = st.sidebar.selectbox('Select Product Type', data['ProductType'].unique())
selected_strategies = st.sidebar.multiselect('Select Marketing Strategies', data['MarketingStrategy'].unique())
min_sales = st.sidebar.slider("Min Sales Quantity", int(data['QuantitySold'].min()), int(data['QuantitySold'].max()), 0)

# Filter data based on user input
filtered_data = data[(data['Date'] >= pd.to_datetime(start_date)) & (data['Date'] <= pd.to_datetime(end_date))]
filtered_data = filtered_data[filtered_data['ProductType'] == selected_product]

# Filter by selected strategies (Multiple strategies)
if selected_strategies:
    filtered_data = filtered_data[filtered_data['MarketingStrategy'].isin(selected_strategies)]

# Filter by minimum sales quantity
filtered_data = filtered_data[filtered_data['QuantitySold'] >= min_sales]

# Show summary statistics
st.subheader("Summary Statistics")
st.write(filtered_data.describe())

# Sales over time chart
st.subheader("Product Sales Over Time")
fig, ax = plt.subplots(figsize=(10, 6))
sns.lineplot(x='Date', y='QuantitySold', data=filtered_data, ax=ax, marker='o', color='teal')
ax.set_title(f"Sales of {selected_product} over Time")
ax.set_xlabel('Date')
ax.set_ylabel('Quantity Sold')
plt.xticks(rotation=45)
st.pyplot(fig)

# Sales distribution by marketing strategy
st.subheader("Sales Distribution by Marketing Strategy")
fig, ax = plt.subplots(figsize=(10, 6))
sns.barplot(x='MarketingStrategy', y='QuantitySold', data=filtered_data, ax=ax, palette="viridis")
ax.set_title(f"Sales Distribution for {selected_product}")
ax.set_xlabel('Marketing Strategy')
ax.set_ylabel('Total Sales')
st.pyplot(fig)

# Conversion rates visualization
st.subheader("Conversion Rates by Interaction Type")
conversion_data = filtered_data.groupby('InteractionType').agg({'Converted': 'mean'}).reset_index()
fig, ax = plt.subplots(figsize=(10, 6))
sns.barplot(x='InteractionType', y='Converted', data=conversion_data, ax=ax, palette="magma")
ax.set_title("Conversion Rates by Interaction Type")
ax.set_xlabel('Interaction Type')
ax.set_ylabel('Conversion Rate')
st.pyplot(fig)

# Anomaly detection plot
st.subheader("Anomaly Detection")
anomalies = filtered_data[filtered_data['Anomaly'] == 1]
show_anomalies = st.sidebar.checkbox("Show Anomalies", value=True)

if show_anomalies and len(anomalies) > 0:
    st.write(f"Anomalies detected: {len(anomalies)}")
    st.write(anomalies[['Date', 'ProductType', 'QuantitySold', 'Anomaly']])
elif show_anomalies:
    st.write("No anomalies detected in the selected period.")

# Sales Comparison by Product Type
st.subheader("Sales Comparison by Product Type")
product_sales = filtered_data.groupby('ProductType').agg({'QuantitySold': 'sum'}).reset_index()
fig, ax = plt.subplots(figsize=(10, 6))
sns.barplot(x='ProductType', y='QuantitySold', data=product_sales, ax=ax, palette="coolwarm")
ax.set_title("Sales Comparison Across Product Types")
ax.set_xlabel('Product Type')
ax.set_ylabel('Total Quantity Sold')
st.pyplot(fig)

# Forecasting (Dummy example: simple moving average for the next 7 days)
st.subheader("Sales Forecast (Next 7 Days)")
forecast_data = filtered_data.groupby('Date').agg({'QuantitySold': 'sum'}).reset_index()
forecast_data.set_index('Date', inplace=True)
forecast_data = forecast_data.rolling(window=7).mean()

fig, ax = plt.subplots(figsize=(10, 6))
sns.lineplot(x=forecast_data.index, y=forecast_data['QuantitySold'], ax=ax, color='orange', label='Moving Average (7 days)', marker='o')
ax.set_title("7-Day Sales Forecast")
ax.set_xlabel('Date')
ax.set_ylabel('Quantity Sold')
plt.xticks(rotation=45)
st.pyplot(fig)

# Footer section
st.markdown("---")
st.markdown("By **Jordan Makgetla**")












