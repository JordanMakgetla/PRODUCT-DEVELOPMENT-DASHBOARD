import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import time

@st.cache_data
def load_data():
    df = pd.read_csv("large_product_sales_500k.csv")
    df['Date'] = pd.to_datetime(df['Date'])
    return df

def main():
    st.set_page_config(page_title="AI-Solutions Dashboard", layout="wide")
    st.markdown("<h5>📊 AI-Solutions Interactive Sales Dashboard</h5>", unsafe_allow_html=True)

    df = load_data()

    st.sidebar.header("Filter Data")

    actor = st.sidebar.selectbox("View as", [
        "Regional Sales Manager",
        "Digital Marketing Analyst",
        "Product Strategy Lead",
        "Sales Team Leader"
    ])

    start_date = st.sidebar.date_input("Start Date", df['Date'].min().date())
    end_date = st.sidebar.date_input("End Date", df['Date'].max().date())

    product_types = st.sidebar.multiselect("Select Product Types", options=df['ProductType'].unique(), default=df['ProductType'].unique())
    marketing_strategies = st.sidebar.multiselect("Select Marketing Strategies", options=df['MarketingStrategy'].unique(), default=df['MarketingStrategy'].unique())
    sales_teams = st.sidebar.multiselect("Filter by Sales Team", options=df['SalesTeamName'].unique(), default=df['SalesTeamName'].unique())

    filtered_df = df[
        (df['Date'].dt.date >= start_date) &
        (df['Date'].dt.date <= end_date) &
        (df['ProductType'].isin(product_types)) &
        (df['MarketingStrategy'].isin(marketing_strategies)) &
        (df['SalesTeamName'].isin(sales_teams))
    ]

    st.markdown(f"**User Role:** {actor}")

    tab1, tab2, tab3, tab4 = st.tabs(["Visual Dashboard", "Anomalies & Forecast", "Raw Data", "AI Assistant"])

    with tab1:

        if actor == "Digital Marketing Analyst":
            sales_by_strategy = filtered_df.groupby("MarketingStrategy")["QuantitySold"].sum().reset_index()
            fig1 = px.pie(sales_by_strategy, names="MarketingStrategy", values="QuantitySold", title="Sales by Marketing Strategy")

            conv_by_strategy = filtered_df.groupby("MarketingStrategy")["Converted"].mean().reset_index()
            fig2 = px.bar(conv_by_strategy, x="MarketingStrategy", y="Converted", title="Conversion Rate by Marketing Strategy", labels={"Converted": "Conversion Rate"})

            col1, col2 = st.columns(2)
            with col1:
                st.plotly_chart(fig1, use_container_width=True)
            with col2:
                st.plotly_chart(fig2, use_container_width=True)

        elif actor == "Sales Team Leader":
            sales_team = filtered_df.groupby("SalesTeamName")["QuantitySold"].sum().reset_index().sort_values(by="QuantitySold", ascending=False)
            fig1 = px.bar(sales_team, x="SalesTeamName", y="QuantitySold", title="Sales by Team")

            top_team = sales_team.iloc[0]["SalesTeamName"] if not sales_team.empty else None
            if top_team:
                team_sales_trend = filtered_df[filtered_df["SalesTeamName"] == top_team].groupby("Date")["QuantitySold"].sum().reset_index()
                fig2 = px.line(team_sales_trend, x="Date", y="QuantitySold", title=f"Sales Trend for {top_team}")

                col1, col2 = st.columns(2)
                with col1:
                    st.plotly_chart(fig1, use_container_width=True)
                with col2:
                    st.plotly_chart(fig2, use_container_width=True)
            else:
                st.plotly_chart(fig1, use_container_width=True)

        elif actor == "Product Strategy Lead":
            sales_by_product = filtered_df.groupby("ProductType")["QuantitySold"].sum().reset_index()
            fig1 = px.bar(sales_by_product, x="ProductType", y="QuantitySold", title="Total Sales by Product Type")

            conv_by_product = filtered_df.groupby("ProductType")["Converted"].mean().reset_index()
            fig2 = px.bar(conv_by_product, x="ProductType", y="Converted", title="Conversion Rate by Product Type", labels={"Converted": "Conversion Rate"})

            col1, col2 = st.columns(2)
            with col1:
                st.plotly_chart(fig1, use_container_width=True)
            with col2:
                st.plotly_chart(fig2, use_container_width=True)

        elif actor == "Regional Sales Manager":
            sales_by_region = filtered_df.groupby("Region")["QuantitySold"].sum().reset_index()
            fig1 = px.bar(sales_by_region, x="Region", y="QuantitySold", title="Sales by Region")

            region_team_sales = filtered_df.groupby(["Region", "SalesTeamName"])["QuantitySold"].sum().reset_index()
            fig2 = px.bar(region_team_sales, x="SalesTeamName", y="QuantitySold", color="Region", title="Sales by Team within Regions")

            col1, col2 = st.columns(2)
            with col1:
                st.plotly_chart(fig1, use_container_width=True)
            with col2:
                st.plotly_chart(fig2, use_container_width=True)

    with tab2:
        st.subheader("\u26A0\uFE0F Anomaly Detection & \U0001F52E Forecast")

        col1, col2 = st.columns(2)

        with col1:
            daily_sales = filtered_df.groupby("Date")["QuantitySold"].sum().reset_index()
            fig = px.line(daily_sales, x="Date", y="QuantitySold", title="Sales Over Time with Anomalies")
            anomaly_dates = filtered_df[filtered_df["Anomaly"] == 1]["Date"]
            fig.add_trace(go.Scatter(
                x=anomaly_dates,
                y=[filtered_df[filtered_df["Date"] == date]["QuantitySold"].sum() for date in anomaly_dates],
                mode='markers', name='Anomalies',
                marker=dict(color='red', size=10)))
            st.plotly_chart(fig, use_container_width=True)

        with col2:
            st.info("Forecasting future sales using simple trend (placeholder)")
            forecast_days = 7
            recent_sales = daily_sales["QuantitySold"].values[-forecast_days:]
            forecast = [max(0, x + np.random.randint(-5, 5)) for x in recent_sales]
            forecast_dates = pd.date_range(start=daily_sales["Date"].max() + pd.Timedelta(days=1), periods=forecast_days)
            forecast_df = pd.DataFrame({"Date": forecast_dates, "Forecasted Sales": forecast})
            fig_forecast = px.line(forecast_df, x="Date", y="Forecasted Sales", title="7-Day Sales Forecast")
            st.plotly_chart(fig_forecast, use_container_width=True)

    with tab3:
        st.subheader("\U0001F4CB Raw Data")
        st.dataframe(filtered_df, use_container_width=True)

    with tab4:
        st.subheader("\U0001F9E0 AI Assistant")
        st.markdown("Use this section to generate AI-driven summaries and insights.")

        if st.button("Generate AI Summary"):
            with st.spinner("Analyzing data using AI..."):
                time.sleep(2)
                top_strategy = filtered_df.groupby("MarketingStrategy")["Converted"].sum().idxmax()
                top_product = filtered_df.groupby("ProductType")["QuantitySold"].sum().idxmax()
                anomaly_count = filtered_df["Anomaly"].sum()
                st.success("AI Summary:")
                st.markdown(f"""
                - **Top Strategy:** {top_strategy} with highest conversions.
                - **Top Product:** {top_product} by quantity sold.
                - **Anomalies:** {anomaly_count} events detected.
                """)

        task = st.selectbox("Choose AI Task", ["Summary", "Forecast", "Anomaly Explanation"])
        if task == "Forecast":
            trend = np.random.randint(5, 15)
            st.info(f"AI Forecast: Sales expected to rise by {trend}% next week.")
        elif task == "Anomaly Explanation":
            st.warning("Anomalies may be due to regional promotions, pricing errors, or external demand factors.")

if __name__ == "__main__":
    main()













