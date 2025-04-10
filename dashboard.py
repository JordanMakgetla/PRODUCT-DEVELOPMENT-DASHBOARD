import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

# Load new data
data = pd.read_csv('large_product_sales_500k.csv')
data['Date'] = pd.to_datetime(data['Date'])

# Set the page configuration
st.set_page_config(
    page_title="AI Solutions Product Sales Dashboard", 
    page_icon="📊", 
    layout="wide"
)

# Add some title and description
st.title("📊 AI Solutions Product Sales Dashboard")
st.markdown("""
This dashboard provides insights into AI-Solutions' product sales, customer interactions, and the effectiveness of marketing strategies. 
Use the interactive filters below to explore the data in various ways.
""")

# Sidebar filters for user interactivity
st.sidebar.header("Filter Data")

# Start Date and End Date filters
start_date = st.sidebar.date_input('Start Date', data['Date'].min())
end_date = st.sidebar.date_input('End Date', data['Date'].max())

# Product Type filter (Including "All" option)
product_options = ['All'] + list(data['ProductType'].unique())  # Adding "All" as an option
selected_product = st.sidebar.selectbox('Select Product Type', product_options)

# Marketing Strategy filter (Including "All" option)
strategy_options = ['All'] + list(data['MarketingStrategy'].unique())  # Adding "All" as an option
selected_strategy = st.sidebar.selectbox('Select Marketing Strategy', strategy_options)

# Region filter (Including "All" option)
region_options = ['All'] + list(data['Region'].unique())  # Adding "All" as an option
selected_region = st.sidebar.selectbox('Select Region', region_options)

# Filter data based on user input
filtered_data = data[(data['Date'] >= pd.to_datetime(start_date)) & (data['Date'] <= pd.to_datetime(end_date))]

# Apply filters based on the selected product type, marketing strategy, and region
if selected_product != 'All':
    filtered_data = filtered_data[filtered_data['ProductType'] == selected_product]

if selected_strategy != 'All':
    filtered_data = filtered_data[filtered_data['MarketingStrategy'] == selected_strategy]

if selected_region != 'All':
    filtered_data = filtered_data[filtered_data['Region'] == selected_region]

# Show summary statistics
st.subheader("Summary Statistics")
st.write(filtered_data.describe())

# Sales over time chart
st.subheader("Product Sales Over Time")
fig, ax = plt.subplots(figsize=(10, 6))
sns.lineplot(x='Date', y='QuantitySold', data=filtered_data, ax=ax, marker='o', color='teal')
ax.set_title(f"Sales of {selected_product if selected_product != 'All' else 'All Products'} Over Time (in Pounds)")
ax.set_xlabel('Date')
ax.set_ylabel('Quantity Sold (in Pounds)')
plt.xticks(rotation=45)
st.pyplot(fig)

# Sales over time report
st.markdown("""
**Report:**
- This line chart shows the sales of the selected product (or all products) over time.
- The x-axis represents the dates, and the y-axis shows the total quantity sold in pounds.
- The trend of sales over time can be observed. If there are any upward or downward movements, those are significant periods to analyze for marketing strategies or sales events.
- Based on this chart, you can determine periods of peak performance and identify potential seasonal trends or anomalies.
""")

# Sales distribution by marketing strategy
st.subheader("Sales Distribution by Marketing Strategy")
fig, ax = plt.subplots(figsize=(10, 6))
sns.barplot(x='MarketingStrategy', y='QuantitySold', data=filtered_data, ax=ax, palette="viridis")
ax.set_title(f"Sales Distribution for {selected_product if selected_product != 'All' else 'All Products'} (in Pounds)")
ax.set_xlabel('Marketing Strategy')
ax.set_ylabel('Total Sales (in Pounds)')
st.pyplot(fig)

# Sales distribution by marketing strategy report
st.markdown("""
**Report:**
- This bar chart compares the total sales in pounds for different marketing strategies.
- It provides insights into which strategies have generated the highest sales and which have not performed as well.
- The marketing strategy with the highest bar has had the most success in driving sales for the selected product (or all products).
- This data can help identify which marketing efforts are most effective for driving revenue, and where further investment or changes may be needed.
""")

# Conversion rates visualization
st.subheader("Conversion Rates")
conversion_data = filtered_data.groupby('InteractionType').agg({'Converted': 'mean'}).reset_index()
fig, ax = plt.subplots(figsize=(10, 6))
sns.barplot(x='InteractionType', y='Converted', data=conversion_data, ax=ax, palette="magma")
ax.set_title("Conversion Rates by Interaction Type")
ax.set_xlabel('Interaction Type')
ax.set_ylabel('Conversion Rate')
st.pyplot(fig)

# Conversion rates report
st.markdown("""
**Report:**
- This bar chart shows the average conversion rate by interaction type.
- The conversion rate represents the percentage of users who converted after interacting with the system.
- High conversion rates in certain interaction types may indicate that these methods are more effective at prompting action from users.
- Comparing the conversion rates across interaction types allows you to assess the success of different engagement strategies.
""")

# Anomaly detection plot
st.subheader("Anomaly Detection")
anomalies = filtered_data[filtered_data['Anomaly'] == 1]
st.write(f"Anomalies detected: {len(anomalies)}")

# Show a list of anomalies (if any)
if len(anomalies) > 0:
    st.write(anomalies[['Date', 'ProductType', 'QuantitySold', 'Anomaly']])

# Anomaly detection report
st.markdown("""
**Report:**
- The anomalies detected represent irregularities or outliers in the data, where the quantity sold or other variables deviate from expected patterns.
- Identifying and investigating anomalies can help understand why certain sales data doesn't align with typical behavior, allowing you to take corrective actions.
- Anomalies can be due to data entry errors, product issues, or unexpected marketing events.
""")

# Sales by Region
st.subheader("Sales by Region")
region_sales = filtered_data.groupby('Region').agg({'QuantitySold': 'sum'}).reset_index()
fig, ax = plt.subplots(figsize=(10, 6))
sns.barplot(x='Region', y='QuantitySold', data=region_sales, ax=ax, palette="coolwarm")
ax.set_title(f"Sales by Region (in Pounds)")
ax.set_xlabel('Region')
ax.set_ylabel('Total Sales (in Pounds)')
st.pyplot(fig)

# Sales by Region report
st.markdown("""
**Report:**
- This bar chart compares total sales across different regions.
- It shows which regions have the highest sales and which are underperforming.
- Identifying top-performing regions helps direct marketing resources and plan regional promotions.
- If there are discrepancies between regions, it may be worth investigating local factors that could impact sales (e.g., regional marketing campaigns, product availability).
""")

# Forecasting (Dummy example: simple moving average for the next 7 days)
st.subheader("Sales Forecast (Next 7 Days)")
forecast_data = filtered_data.groupby('Date').agg({'QuantitySold': 'sum'}).reset_index()
forecast_data.set_index('Date', inplace=True)
forecast_data = forecast_data.rolling(window=7).mean()

fig, ax = plt.subplots(figsize=(10, 6))
sns.lineplot(x=forecast_data.index, y=forecast_data['QuantitySold'], ax=ax, color='orange', label='Moving Average (7 days)', marker='o')
ax.set_title("7-Day Sales Forecast")
ax.set_xlabel('Date')
ax.set_ylabel('Quantity Sold (in Pounds)')
plt.xticks(rotation=45)
st.pyplot(fig)

# Sales forecasting report
st.markdown("""
**Report:**
- This line chart shows the 7-day moving average of sales, providing a forecast of the expected sales trend.
- The moving average smooths out short-term fluctuations and highlights longer-term trends.
- This forecast can help anticipate demand and plan future marketing strategies, stock levels, or promotional campaigns.
""")

# Marketing Strategy Performance Report
st.subheader("Marketing Strategy Performance Report")

# Compare the effectiveness of each marketing strategy
strategy_performance = filtered_data.groupby('MarketingStrategy').agg({
    'QuantitySold': 'sum', 
    'Converted': 'mean'
}).reset_index()

# Visualize total sales by marketing strategy
fig, ax = plt.subplots(figsize=(10, 6))
sns.barplot(x='MarketingStrategy', y='QuantitySold', data=strategy_performance, ax=ax, palette="Set2")
ax.set_title("Total Sales by Marketing Strategy (in Pounds)")
ax.set_xlabel('Marketing Strategy')
ax.set_ylabel('Total Sales (in Pounds)')
st.pyplot(fig)

# Marketing strategy performance report
st.markdown("""
**Report:**
- This bar chart shows the total sales generated by each marketing strategy.
- The marketing strategy with the highest total sales has been the most successful at generating revenue.
- It’s important to note the conversion rates for each strategy (shown earlier) to understand the relative effectiveness of each marketing approach.
- These findings can inform future marketing decisions, allowing AI-Solutions to optimize their approach for maximum impact.
""")

# Footer section
st.markdown("---")
st.markdown("By **Jordan Makgetla**")











