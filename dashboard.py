import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np

# Load new data
data = pd.read_csv('large_product_sales_500k.csv')
data.columns = data.columns.str.strip()
data['Date'] = pd.to_datetime(data['Date'])

# Set the page config
st.set_page_config(
    page_title="AI Solutions Product Sales Dashboard", 
    page_icon="📊", 
    layout="wide"
)

# Title and description with reduced font
st.markdown("""
<h5 style='text-align: center; font-size:16px;'>📊 AI Solutions Product Sales Dashboard</h5>
<p style='text-align: center;'>Explore interactive insights on sales, strategies, and conversions.</p>
""", unsafe_allow_html=True)

# Filter section in sidebar
with st.sidebar:
    st.markdown("<h6 style='margin-bottom: 10px;'>Filters</h6>", unsafe_allow_html=True)
    start_date = st.date_input('Start Date', data['Date'].min())
    end_date = st.date_input('End Date', data['Date'].max())
    product_options = ['All'] + sorted(data['ProductType'].unique())
    selected_product = st.selectbox('Product Type', product_options)
    strategy_options = ['All'] + sorted(data['MarketingStrategy'].unique())
    selected_strategy = st.selectbox('Marketing Strategy', strategy_options)
    team_options = ['All'] + sorted(data['SalesTeamName'].dropna().unique())
    selected_team = st.selectbox('Sales Team', team_options)

# Apply filters
data_filtered = data[(data['Date'] >= pd.to_datetime(start_date)) & (data['Date'] <= pd.to_datetime(end_date))]
if selected_product != 'All':
    data_filtered = data_filtered[data_filtered['ProductType'] == selected_product]
if selected_strategy != 'All':
    data_filtered = data_filtered[data_filtered['MarketingStrategy'] == selected_strategy]
if selected_team != 'All':
    data_filtered = data_filtered[data_filtered['SalesTeamName'] == selected_team]

scaling_factor = 100

# Tabs to organize layout - Added Data Tables tab
tab1, tab2, tab3, tab4 = st.tabs(["Overview", "Sales Analysis", "Forecast & Teams", "Data Tables"])

# Enhanced chart settings with better spacing
def styled_fig(fig, height=350):
    fig.update_layout(
        template='plotly_white',
        height=height,
        font=dict(size=10),
        margin=dict(l=50, r=50, t=50, b=50),  # Increased margins
        legend=dict(orientation='h', y=-0.2),
        xaxis=dict(tickangle=-45 if len(fig.data[0].x) > 5 else 0)  # Rotate labels if many categories
    )
    return fig

# --- Tab 1: Overview --- #
with tab1:
    # Top row - Metrics
    st.subheader("Key Metrics")
    metric1, metric2, metric3 = st.columns(3)
    with metric1:
        st.metric("Total Quantity Sold", f"{int(data_filtered['QuantitySold'].sum() * scaling_factor):,}")
    with metric2:
        st.metric("Total Interactions", f"{len(data_filtered):,}")
    with metric3:
        st.metric("Average Conversion", f"{(data_filtered['Converted'].mean() * 100):.1f}%")
    
    st.markdown("---")
    
    # First chart row
    col1, col2 = st.columns(2)
    with col1:
        # Team Performance Comparison
        team_performance = data_filtered.groupby('SalesTeamName').agg({
            'QuantitySold': 'sum',
            'Converted': 'mean'
        }).reset_index()
        team_performance['QuantitySold'] = team_performance['QuantitySold'] * scaling_factor
        team_performance['Converted'] = (team_performance['Converted'] * 100).round(1)
        fig_team = px.bar(team_performance, 
                         x='SalesTeamName', 
                         y='QuantitySold',
                         color='Converted',
                         title='Team Performance (Size=Sales, Color=Conversion %)',
                         labels={'QuantitySold': 'Total Sales', 'Converted': 'Conversion %'})
        st.plotly_chart(styled_fig(fig_team, height=400), use_container_width=True)
        
    with col2:
        # Sales by Region
        region = data_filtered.groupby('Region')['QuantitySold'].sum().reset_index()
        region['QuantitySold'] *= scaling_factor
        fig2 = px.bar(region, x='Region', y='QuantitySold', color='Region',
                      title="Sales by Region")
        st.plotly_chart(styled_fig(fig2, height=400), use_container_width=True)
    
    st.markdown("---")
    
    # Second chart row
    col3, col4 = st.columns(2)
    with col3:
        # Conversion Rates
        conv = data_filtered.groupby('InteractionType')['Converted'].mean().reset_index()
        conv['Converted'] = (conv['Converted'] * 100).round(2)
        fig1 = px.bar(conv, x='InteractionType', y='Converted', color='InteractionType',
                      title="Conversion Rates (%)", labels={'Converted': 'Conversion %'})
        st.plotly_chart(styled_fig(fig1, height=400), use_container_width=True)
    
    with col4:
        # Sales by Team (horizontal)
        team_sales = data_filtered.groupby('SalesTeamName')['QuantitySold'].sum().reset_index()
        team_sales = team_sales.sort_values(by='QuantitySold', ascending=False)
        fig3 = px.bar(team_sales, x='QuantitySold', y='SalesTeamName', orientation='h',
                      color='SalesTeamName', title='Sales by Team')
        st.plotly_chart(styled_fig(fig3, height=400), use_container_width=True)

# --- Tab 2: Sales Analysis --- #
with tab2:
    col1, col2 = st.columns(2)
    with col1:
        # Sales Over Time
        daily_sales = data_filtered.groupby('Date')['QuantitySold'].sum().reset_index()
        daily_sales['QuantitySold'] *= scaling_factor
        fig4 = px.line(daily_sales, x='Date', y='QuantitySold', markers=True, 
                       title='Sales Over Time')
        st.plotly_chart(styled_fig(fig4, height=450), use_container_width=True)
    
    with col2:
        # Sales by Strategy
        strat = data_filtered.groupby('MarketingStrategy')['QuantitySold'].sum().reset_index()
        strat['QuantitySold'] *= scaling_factor
        fig5 = px.bar(strat, x='MarketingStrategy', y='QuantitySold', color='MarketingStrategy',
                      title='Sales by Strategy')
        st.plotly_chart(styled_fig(fig5, height=450), use_container_width=True)
    
    # Anomalies section with more space
    st.markdown("---")
    st.subheader("Anomaly Detection")
    anomalies = data_filtered[data_filtered['Anomaly'] == 1]
    col_anom1, col_anom2 = st.columns([1, 3])
    with col_anom1:
        st.metric("Anomalies Detected", len(anomalies))
    with col_anom2:
        if not anomalies.empty:
            st.dataframe(anomalies[['Date', 'ProductType', 'QuantitySold', 'SalesTeamName', 'Anomaly']].head(10))

# --- Tab 3: Forecast & Teams --- #
with tab3:
    col1, col2 = st.columns(2)
    with col1:
        # 7-Day Moving Average
        forecast = data_filtered.groupby('Date')['QuantitySold'].sum().reset_index()
        forecast['RollingAvg'] = forecast['QuantitySold'].rolling(7).mean() * scaling_factor
        fig6 = px.line(forecast, x='Date', y='RollingAvg', 
                       title='7-Day Moving Average', markers=True)
        st.plotly_chart(styled_fig(fig6, height=450), use_container_width=True)
    
    with col2:
        # Strategy Effectiveness
        strat_perf = data_filtered.groupby('MarketingStrategy').agg({
            'QuantitySold': 'sum', 'Converted': 'mean'
        }).reset_index()
        strat_perf['Converted'] = (strat_perf['Converted'] * 100).round(2)
        strat_perf['QuantitySold'] *= scaling_factor
        fig7 = px.scatter(strat_perf, x='Converted', y='QuantitySold', 
                          color='MarketingStrategy', size='QuantitySold', 
                          title='Strategy Effectiveness')
        st.plotly_chart(styled_fig(fig7, height=450), use_container_width=True)

# --- New Tab 4: Data Tables --- #
with tab4:
    st.subheader("Detailed Data")
    st.write("Filtered dataset with all records")
    st.dataframe(data_filtered)
    
    st.markdown("---")
    st.subheader("Summary Statistics")
    st.dataframe(data_filtered.describe())

# Footer
st.markdown("---")
st.markdown("By *Jordan Makgetla*")

