import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np

# Load and prepare data
data = pd.read_csv('large_product_sales_500k.csv')
data.columns = data.columns.str.strip()
data['Date'] = pd.to_datetime(data['Date'])
data['Converted'] = pd.to_numeric(data['Converted'], errors='coerce').fillna(0)
data['QuantitySold'] = pd.to_numeric(data['QuantitySold'], errors='coerce').fillna(0)

# Page configuration
st.set_page_config(
    page_title="AI Solutions Product Sales Dashboard",
    page_icon="📊",
    layout="wide"
)

# Actor Selection
actor = st.selectbox("Select Actor Role", ["All Users", "Sales Manager", "Marketing Analyst", "Executive"])

# Sidebar Filters
with st.sidebar:
    st.markdown("### Filters")
    start_date = st.date_input("Start Date", data["Date"].min())
    end_date = st.date_input("End Date", data["Date"].max())
    product_options = ['All'] + sorted(data['ProductType'].dropna().unique())
    selected_product = st.selectbox('Product Type', product_options)
    strategy_options = ['All'] + sorted(data['MarketingStrategy'].dropna().unique())
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

# Custom color sequences
team_colors = px.colors.qualitative.Vivid + px.colors.qualitative.Dark24
strategy_colors = px.colors.qualitative.Set3
conversion_colors = px.colors.sequential.Blues

# Optimized Style Helper with proper legend spacing
def styled_fig(fig, height=450, chart_type='bar'):
    fig.update_layout(
        template='plotly_white',
        height=height,
        font=dict(size=12),
        margin=dict(l=80, r=50, t=80, b=180),  # Increased margins
        legend=dict(
            orientation='h',
            yanchor='bottom',
            y=-0.5,
            xanchor='center',
            x=0.5,
            font=dict(size=11),
            title=None,
            tracegroupgap=15,  # Use tracegroupgap instead of itemgap
            itemsizing='constant'
        ),
        title=dict(
            x=0.5,
            xanchor='center',
            font=dict(size=14),
            y=0.95
        )
    )
    
    if chart_type == 'bar':
        fig.update_xaxes(
            title_standoff=25,
            tickfont=dict(size=11),
            title_font=dict(size=12),
            tickangle=0,
            tickmode='array',
            showgrid=False
        )
        fig.update_yaxes(
            title_standoff=25,
            tickfont=dict(size=11),
            title_font=dict(size=12),
            showgrid=True
        )
        
        if fig.data[0].orientation == 'h':
            fig.update_layout(
                margin=dict(l=200, r=50, t=80, b=100),
                yaxis=dict(
                    tickmode='array',
                    tickfont=dict(size=10),
                    automargin=True
                )
            )
    
    elif chart_type == 'line':
        fig.update_xaxes(
            rangeslider=dict(visible=False),
            tickformat='%b %d'
        )
    
    return fig

# Tabs
tab1, tab2, tab3, tab4 = st.tabs(["Visual Dashboard", "Key Metrics", "Anomalies & Forecast", "Raw Data"])

# --- Tab 1: Visual Dashboard --- #
with tab1:
    if actor == "Sales Manager":
        st.subheader("Sales by Region and Team")
        col1, col2 = st.columns(2)
        with col1:
            region = data_filtered.groupby('Region')['QuantitySold'].sum().reset_index()
            fig = px.bar(region, x='Region', y='QuantitySold', color='Region',
                         title="Sales by Region", color_discrete_sequence=team_colors)
            fig.update_layout(
                xaxis=dict(
                    tickvals=region['Region'],
                    ticktext=region['Region'].apply(lambda x: x[:12]+'...' if len(x)>12 else x)
                )
            )
            st.plotly_chart(styled_fig(fig), use_container_width=True)
            
        with col2:
            team_sales = data_filtered.groupby('SalesTeamName')['QuantitySold'].sum().reset_index()
            fig = px.bar(team_sales, x='QuantitySold', y='SalesTeamName', orientation='h',
                         color='SalesTeamName', title='Sales by Team', color_discrete_sequence=team_colors)
            fig.update_layout(
                yaxis=dict(
                    tickvals=team_sales['SalesTeamName'],
                    ticktext=team_sales['SalesTeamName'].apply(lambda x: x[:18]+'...' if len(x)>18 else x)
                )
            )
            st.plotly_chart(styled_fig(fig), use_container_width=True)

    elif actor == "Marketing Analyst":
        st.subheader("Conversion and Strategy Performance")
        col1, col2 = st.columns(2)
        with col1:
            conv = data_filtered.groupby('InteractionType')['Converted'].mean().reset_index()
            conv['Converted'] *= 100
            fig = px.bar(conv, x='InteractionType', y='Converted', color='InteractionType',
                         title="Avg Conversion Rate (%)", color_discrete_sequence=conversion_colors)
            fig.update_layout(
                xaxis=dict(
                    tickvals=conv['InteractionType'],
                    ticktext=conv['InteractionType'].apply(lambda x: x[:15]+'...' if len(x)>15 else x)
                )
            )
            st.plotly_chart(styled_fig(fig), use_container_width=True)
            
        with col2:
            strat = data_filtered.groupby('MarketingStrategy')['QuantitySold'].sum().reset_index()
            fig = px.bar(strat, x='MarketingStrategy', y='QuantitySold', color='MarketingStrategy',
                         title='Sales by Strategy', color_discrete_sequence=strategy_colors)
            fig.update_layout(
                xaxis=dict(
                    tickvals=strat['MarketingStrategy'],
                    ticktext=strat['MarketingStrategy'].apply(lambda x: x[:15]+'...' if len(x)>15 else x)
                )
            )
            st.plotly_chart(styled_fig(fig), use_container_width=True)

    elif actor == "Executive" or actor == "All Users":
        st.subheader("High-Level Overview")
        col1, col2 = st.columns(2)
        with col1:
            team_perf = data_filtered.groupby('SalesTeamName').agg({'QuantitySold':'sum', 'Converted':'mean'}).reset_index()
            team_perf['Converted'] *= 100
            fig = px.bar(team_perf, x='SalesTeamName', y='QuantitySold', color='SalesTeamName',
                         title='Team Performance', color_discrete_sequence=team_colors)
            fig.update_layout(
                xaxis=dict(
                    tickvals=team_perf['SalesTeamName'],
                    ticktext=team_perf['SalesTeamName'].apply(lambda x: x[:12]+'...' if len(x)>12 else x),
                    ticklabelposition="outside",
                    ticks="outside",
                    ticklen=8
                ),
                margin=dict(b=200)
            )
            st.plotly_chart(fig, use_container_width=True)
            
        with col2:
            forecast = data_filtered.groupby('Date')['QuantitySold'].sum().rolling(7, min_periods=1).mean().reset_index(name='7-Day Avg')
            fig = px.line(forecast, x='Date', y='7-Day Avg', markers=True,
                          title='7-Day Moving Average', color_discrete_sequence=['#636EFA'])
            st.plotly_chart(styled_fig(fig, chart_type='line'), use_container_width=True)

# --- Tab 2: Key Metrics --- #
with tab2:
    st.subheader("Key Metrics Summary")
    metric1, metric2, metric3 = st.columns(3)
    metric1.metric("Total Quantity Sold", f"{int(data_filtered['QuantitySold'].sum()):,}")
    metric2.metric("Total Interactions", f"{len(data_filtered):,}")
    avg_conv = data_filtered['Converted'].mean() * 100
    metric3.metric("Avg. Conversion", f"{avg_conv:.1f}%")

# --- Tab 3: Anomalies & Forecast --- #
with tab3:
    st.subheader("Anomaly Detection and Trends")
    anomalies = data_filtered[data_filtered['Anomaly'] == 1]
    col1, col2 = st.columns([1, 2])
    with col1:
        st.metric("Anomalies Detected", len(anomalies))
    with col2:
        if not anomalies.empty:
            st.dataframe(anomalies[['Date', 'ProductType', 'QuantitySold', 'SalesTeamName', 'Anomaly']].head(10))

    st.markdown("### Strategy Effectiveness")
    strat_perf = data_filtered.groupby('MarketingStrategy').agg({'QuantitySold': 'sum', 'Converted': 'mean'}).reset_index()
    strat_perf['Converted'] *= 100
    fig = px.scatter(strat_perf, x='Converted', y='QuantitySold', size='QuantitySold',
                     color='MarketingStrategy', hover_name='MarketingStrategy',
                     title='Strategy Effectiveness (Size = Quantity Sold)',
                     color_discrete_sequence=strategy_colors)
    st.plotly_chart(styled_fig(fig, chart_type='scatter'), use_container_width=True)

# --- Tab 4: Raw Data --- #
with tab4:
    st.subheader("Filtered Dataset")
    st.dataframe(data_filtered)
    st.markdown("### Summary Statistics")
    st.dataframe(data_filtered.describe())

# Footer
st.markdown("---")
st.markdown("By Jordan Makgetla")
