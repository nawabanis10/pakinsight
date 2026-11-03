
import streamlit as st
import pandas as pd
from pathlib import Path
import plotly.express as px
from home_ui import inject_css, render_sidebar, render_home
import os
from dotenv import load_dotenv
from pathlib import Path

from sqlalchemy import create_engine
from sqlalchemy.engine import URL

@st.cache_resource
def get_engine():
    config = st.secrets["mysql"]

    connection_url = URL.create(
        "mysql+pymysql",
        username=config["username"],
        password=config["password"],
        host=config["host"],
        port=int(config["port"]),
        database=config["database"]
    )

    return create_engine(
        connection_url,
        connect_args={"ssl": {"check_hostname": False}}
    )

engine = get_engine()

# Page configuration
st.set_page_config(
    page_title="PakInsight",
    page_icon="🇵🇰",
    layout="wide"
)
inject_css()
# Project paths
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data" / "processed"

# Load datasets
weather_df = pd.read_sql("SELECT * FROM weather_data", engine)
cost_df = pd.read_sql("SELECT * FROM cost_of_living", engine)
economic_df = pd.read_sql("SELECT * FROM economic_summary", engine)


# Sidebar Navigation
page = render_sidebar()


# Page Content
if page == "Home":
    render_home(weather_df, cost_df, economic_df)


elif page == "Weather Analysis":

    st.subheader("🌤️ Weather Insights")
    st.caption("Understand temperature and rainfall patterns across Pakistani cities.")

    st.divider()

    # 1. City Selection
    cities = sorted(weather_df["city"].unique())

    selected_city = st.selectbox(
        "📍 Choose a City",
        cities
    )

    # 2. Filter Selected City
    city_weather = weather_df[
        weather_df["city"] == selected_city
    ].copy()

    # 3. Calculate Weather Statistics
    avg_max_temp = city_weather["temp_max"].mean()
    avg_min_temp = city_weather["temp_min"].mean()
    total_rainfall = city_weather["precipitation"].sum()

    # 4. Weather Overview
    st.markdown(f"### 📊 Weather Overview — {selected_city}")
    st.caption("Annual weather statistics for 2025")

    col1, col2, col3 = st.columns(3)

    with col1:
        with st.container(border=True):
            st.metric("🌡️ Average High", f"{avg_max_temp:.2f} °C")

    with col2:
        with st.container(border=True):
            st.metric("❄️ Average Low", f"{avg_min_temp:.2f} °C")

    with col3:
        with st.container(border=True):
            st.metric("🌧️ Total Rainfall", f"{total_rainfall:,.2f} mm")

    st.caption(
        f"Based on {len(city_weather):,} daily weather records for {selected_city}."
    )

    st.divider()

    # 5. Monthly Temperature Trend
    st.subheader("📈 Monthly Temperature Trend")

    monthly_weather = city_weather.copy()

    monthly_weather["date"] = pd.to_datetime(monthly_weather["date"])
    monthly_weather["month"] = monthly_weather["date"].dt.month

    monthly_summary = (
        monthly_weather.groupby("month")["temp_max"]
        .mean()
        .reset_index()
        .sort_values("month")
    )

    monthly_summary["Month"] = monthly_summary["month"].apply(
        lambda x: pd.Timestamp(month=x, day=1, year=2025).strftime("%b")
    )

    fig = px.line(
        monthly_summary,
        x="Month",
        y="temp_max",
        markers=True,
        title=f"Monthly Average Maximum Temperature — {selected_city}",
        labels={
            "Month": "Month",
            "temp_max": "Temperature (°C)"
        },
        template="plotly_dark"
    )

    fig.update_traces(
        line=dict(width=3),
        marker=dict(size=9)
    )

    fig.update_layout(
        hovermode="x unified",
        height=450
    )

    st.plotly_chart(fig, use_container_width=True)



    # 6. Monthly Rainfall Analysis
    st.divider()

    st.subheader("🌧️ Monthly Rainfall Analysis")

    # Create month column
    rainfall_data = city_weather.copy()

    rainfall_data["date"] = pd.to_datetime(rainfall_data["date"])
    rainfall_data["month"] = rainfall_data["date"].dt.month

    # Calculate monthly rainfall
    rainfall_summary = (
        rainfall_data.groupby("month")["precipitation"]
        .sum()
        .reset_index()
        .sort_values("month")
    )

    rainfall_summary["Month"] = rainfall_summary["month"].apply(
        lambda x: pd.Timestamp(month=x, day=1, year=2025).strftime("%b")
    )

    fig_rain = px.bar(
        rainfall_summary,
        x="Month",
        y="precipitation",
        title=f"Monthly Rainfall — {selected_city}",
        labels={
            "Month": "Month",
            "precipitation": "Rainfall (mm)"
        },
        template="plotly_dark",
        color="precipitation",
        color_continuous_scale="Blues"
    )

    fig_rain.update_layout(
        height=450,
        showlegend=False
    )

    st.plotly_chart(fig_rain, use_container_width=True)


    # 7. Weather Highlights
    st.divider()

    st.subheader("🔍 Weather Highlights")

    hottest_month = monthly_summary.loc[
        monthly_summary["temp_max"].idxmax()
    ]

    coldest_month = monthly_summary.loc[
        monthly_summary["temp_max"].idxmin()
    ]

    rainiest_month = rainfall_summary.loc[
        rainfall_summary["precipitation"].idxmax()
    ]

    col1, col2, col3 = st.columns(3)

    with col1:
        st.info(
            f"🔥 **Hottest Month**\n\n"
            f"{hottest_month['Month']} — "
            f"{hottest_month['temp_max']:.2f} °C"
        )

    with col2:
        st.info(
            f"❄️ **Coldest Month**\n\n"
            f"{coldest_month['Month']} — "
            f"{coldest_month['temp_max']:.2f} °C"
        )

    with col3:
        st.info(
            f"🌧️ **Rainiest Month**\n\n"
            f"{rainiest_month['Month']} — "
            f"{rainiest_month['precipitation']:.2f} mm"
        )



elif page == "Cost of Living":

    st.subheader("🛒 Cost of Living Analysis")
    st.caption("Compare essential item prices across Pakistani cities.")

    st.divider()

    # City selection
    cities = ["Islamabad", "Lahore", "Karachi", "Peshawar", "Quetta"]

    selected_city = st.selectbox(
        "📍 Select a City",
        cities,
        key="cost_city"
    )

    # Calculate price statistics
    city_prices = cost_df[selected_city].dropna()

    avg_price = city_prices.mean()
    highest_price = city_prices.max()
    lowest_price = city_prices.min()

    # Display metrics
    st.markdown(f"### 📊 Price Overview — {selected_city}")

    col1, col2, col3 = st.columns(3)

    with col1:
        with st.container(border=True):
            st.metric("Average Listed Price", f"Rs. {avg_price:,.2f}")

    with col2:
        with st.container(border=True):
            st.metric("Highest Item Price", f"Rs. {highest_price:,.2f}")

    with col3:
        with st.container(border=True):
            st.metric("Lowest Item Price", f"Rs. {lowest_price:,.2f}")

    st.caption(
        f"Based on {len(city_prices)} available item prices."
    )

    st.info(
        "Note: Average listed item price is a simple average across different "
        "items and units, not an official cost-of-living index."
    )


    # Item-wise Price Analysis
    st.divider()

    st.subheader("📊 Essential Items Price Comparison")

    sort_order = st.selectbox(
        "Sort prices",
        ["Highest to Lowest", "Lowest to Highest"],
        key="price_sort"
    )

    price_data = cost_df[["Item", selected_city]].dropna()

    price_data = price_data.sort_values(
        by=selected_city,
        ascending=(sort_order == "Lowest to Highest")
    )

    fig_cost = px.bar(
        price_data,
        x=selected_city,
        y="Item",
        orientation="h",
        title=f"Essential Item Prices — {selected_city}",
        labels={
            selected_city: "Price (Rs.)",
            "Item": "Essential Item"
        },
        template="plotly_dark"
    )

    fig_cost.update_layout(
    height=750,
    yaxis={"autorange": "reversed"},
    showlegend=False
)

    st.plotly_chart(fig_cost, use_container_width=True)

    # City-wise Item Price Comparison
    st.divider()

    st.subheader("🏙️ Compare an Item Across Cities")

    selected_item = st.selectbox(
        "Select an Essential Item",
        cost_df["Item"].dropna().unique(),
        key="compare_item"
    )

    item_data = cost_df[cost_df["Item"] == selected_item]

    comparison_data = item_data[
        ["Islamabad", "Lahore", "Karachi", "Peshawar", "Quetta"]
    ].melt(
        var_name="City",
        value_name="Price"
    ).dropna()

    fig_compare = px.bar(
        comparison_data,
        x="City",
        y="Price",
        color="City",
        title=f"{selected_item} — Price Comparison Across Cities",
        labels={"Price": "Price (Rs.)"},
        template="plotly_dark"
    )

    st.plotly_chart(fig_compare, use_container_width=True)

    # Essential Items Price Table
    st.divider()

    st.subheader("📋 Essential Items Price List")

    display_data = cost_df[["Item", "Unit", selected_city]].copy()

    display_data = display_data.rename(
        columns={selected_city: "Price (Rs.)"}
    )

    display_data = display_data.sort_values(
        by="Price (Rs.)",
        ascending=False,
        na_position="last"
    )

    st.dataframe(
        display_data,
        use_container_width=True,
        hide_index=True
    )


elif page == "Economic Analysis":

    st.title("📊 Economic Insights")
    st.caption(
        "Explore business activity and employment across five major cities of Pakistan."
    )

    st.divider()

    # Calculate key statistics
    total_establishments = economic_df["Establishments"].sum()
    total_workforce = economic_df["Workforce"].sum()
    total_cities = economic_df["District"].nunique()

    # Dashboard Metrics
    col1, col2, col3 = st.columns(3)

    with col1:
        with st.container(border=True):
            st.metric(
                label="🏢 Total Establishments",
                value=f"{total_establishments:,}"
            )
            st.caption("Business establishments")

    with col2:
        with st.container(border=True):
            st.metric(
                label="👥 Total Workforce",
                value=f"{total_workforce:,}"
            )
            st.caption("People employed")

    with col3:
        with st.container(border=True):
            st.metric(
                label="📍 Cities Covered",
                value=total_cities
            )
            st.caption("Major Pakistani cities")

    st.divider()

    st.info(
        "These statistics provide an overview of business activity "
        "and workforce distribution across the selected cities."
    )

    # Business Establishments Chart
    st.divider()
    st.subheader("🏙️ Business Establishments by City")

    fig_establishments = px.bar(
        economic_df.sort_values("Establishments", ascending=False),
        x="District",
        y="Establishments",
        color="Establishments",
        title="Business Establishments by City",
        labels={
            "District": "City",
            "Establishments": "Number of Establishments"
        },
        template="plotly_dark",
        text_auto=True
    )

    st.plotly_chart(fig_establishments, use_container_width=True)

    # Workforce Comparison Chart
    st.divider()
    st.subheader("👥 Workforce Distribution by City")

    fig_workforce = px.bar(
        economic_df.sort_values("Workforce", ascending=False),
        x="District",
        y="Workforce",
        color="Workforce",
        title="Total Workforce by City",
        labels={
            "District": "City",
            "Workforce": "Number of Workers"
        },
        template="plotly_dark",
        text_auto=True
    )

    st.plotly_chart(fig_workforce, use_container_width=True)

    # Interactive City Details
    st.divider()
    st.subheader("🔎 Explore a City's Economic Profile")

    selected_economic_city = st.selectbox(
        "Select a City",
        economic_df["District"].unique(),
        key="economic_city"
    )

    city_data = economic_df[
        economic_df["District"] == selected_economic_city
    ].iloc[0]

    col1, col2 = st.columns(2)

    with col1:
        st.metric(
            "🏢 Establishments",
            f"{city_data['Establishments']:,}"
        )

    with col2:
        st.metric(
            "👥 Workforce",
            f"{city_data['Workforce']:,}"
        )


elif page == "City Comparison":

    st.title("🏙️ Pakistan City Comparison")
    st.caption(
        "Compare two Pakistani cities using weather, living costs and economic indicators."
    )

    st.divider()

    cities = ["Islamabad", "Lahore", "Karachi", "Peshawar", "Quetta"]

    col1, col2 = st.columns(2)

    with col1:
        city1 = st.selectbox(
            "Select First City",
            cities,
            index=0,
            key="compare_city1"
        )

    with col2:
        city2 = st.selectbox(
            "Select Second City",
            cities,
            index=1,
            key="compare_city2"
        )

    if city1 == city2:
        st.warning("Please select two different cities.")

    else:
        st.success(f"Comparing {city1} and {city2}")

        # Navigation
        comparison_section = st.radio(
            "Select Comparison Module",
            ["Overview", "Weather", "Cost of Living", "Economy", "Report"],
            horizontal=True,
            key="comparison_navigation"
        )

        st.divider()

        # Shared Data Calculations
        city1_weather = weather_df[weather_df["city"] == city1]
        city2_weather = weather_df[weather_df["city"] == city2]

        city1_temp = city1_weather["temp_max"].mean()
        city2_temp = city2_weather["temp_max"].mean()

        city1_rain = city1_weather["precipitation"].sum()
        city2_rain = city2_weather["precipitation"].sum()

        city1_prices = cost_df[city1].dropna()
        city2_prices = cost_df[city2].dropna()

        city1_avg = city1_prices.mean()
        city2_avg = city2_prices.mean()

        city1_highest = city1_prices.max()
        city2_highest = city2_prices.max()

        city1_lowest = city1_prices.min()
        city2_lowest = city2_prices.min()

        city1_economic = economic_df[
            economic_df["District"] == city1
        ].iloc[0]

        city2_economic = economic_df[
            economic_df["District"] == city2
        ].iloc[0]

        # =====================================
        # OVERVIEW
        # =====================================

        if comparison_section == "Overview":

            st.header("⚡ Quick Comparison Highlights")

            with st.container(border=True):

                col1, col2 = st.columns(2)

                with col1:
                    st.markdown("**🌡️ Cooler City**")

                    if city1_temp < city2_temp:
                        st.success(city1)
                    elif city2_temp < city1_temp:
                        st.success(city2)
                    else:
                        st.info("Equal")

                    st.markdown("**💰 Lower Average Listed Price**")

                    if city1_avg < city2_avg:
                        st.success(city1)
                    elif city2_avg < city1_avg:
                        st.success(city2)
                    else:
                        st.info("Equal")

                with col2:
                    st.markdown("**🌧️ Higher Annual Rainfall**")

                    if city1_rain > city2_rain:
                        st.info(city1)
                    elif city2_rain > city1_rain:
                        st.info(city2)
                    else:
                        st.info("Equal")

                    st.markdown("**🏢 More Business Establishments**")

                    if city1_economic["Establishments"] > city2_economic["Establishments"]:
                        st.info(city1)
                    elif city2_economic["Establishments"] > city1_economic["Establishments"]:
                        st.info(city2)
                    else:
                        st.info("Equal")

                st.divider()

                if city1_economic["Workforce"] > city2_economic["Workforce"]:
                    st.write(f"👥 **Larger recorded workforce:** {city1}")
                elif city2_economic["Workforce"] > city1_economic["Workforce"]:
                    st.write(f"👥 **Larger recorded workforce:** {city2}")
                else:
                    st.write("👥 **Recorded workforce:** Equal")

            st.caption(
                "Note: Average listed prices are simple averages across "
                "different items and units, not an official cost-of-living index."
            )

        # =====================================
        # WEATHER COMPARISON
        # =====================================

        elif comparison_section == "Weather":

            st.header("🌤️ Weather Comparison")

            col1, col2 = st.columns(2)

            with col1:
                with st.container(border=True):
                    st.subheader(f"📍 {city1}")
                    st.metric(
                        "Average High Temperature",
                        f"{city1_temp:.2f} °C"
                    )
                    st.metric(
                        "Annual Rainfall",
                        f"{city1_rain:,.2f} mm"
                    )

            with col2:
                with st.container(border=True):
                    st.subheader(f"📍 {city2}")
                    st.metric(
                        "Average High Temperature",
                        f"{city2_temp:.2f} °C"
                    )
                    st.metric(
                        "Annual Rainfall",
                        f"{city2_rain:,.2f} mm"
                    )

            # Differences
            st.divider()
            st.subheader("📏 Difference Between Cities")

            temp_difference = abs(city1_temp - city2_temp)
            rain_difference = abs(city1_rain - city2_rain)

            col1, col2 = st.columns(2)

            with col1:
                st.metric(
                    "Temperature Difference",
                    f"{temp_difference:.2f} °C"
                )

            with col2:
                st.metric(
                    "Rainfall Difference",
                    f"{rain_difference:,.2f} mm"
                )

            # Percentage Difference
            st.subheader("📈 Percentage Difference")

            temp_base = min(city1_temp, city2_temp)
            rain_base = min(city1_rain, city2_rain)

            temp_percentage = (
                temp_difference / temp_base * 100
                if temp_base != 0 else 0
            )

            rain_percentage = (
                rain_difference / rain_base * 100
                if rain_base != 0 else 0
            )

            col1, col2 = st.columns(2)

            with col1:
                st.metric(
                    "Temperature Difference (%)",
                    f"{temp_percentage:.2f}%"
                )

            with col2:
                st.metric(
                    "Rainfall Difference (%)",
                    f"{rain_percentage:.2f}%"
                )

            # Weather Charts
            st.divider()
            st.subheader("📊 Visual Weather Comparison")

            weather_comparison = pd.DataFrame({
                "City": [city1, city2],
                "Average Maximum Temperature": [
                    city1_temp, city2_temp
                ],
                "Annual Rainfall": [
                    city1_rain, city2_rain
                ]
            })

            col1, col2 = st.columns(2)

            with col1:
                fig_temp = px.bar(
                    weather_comparison,
                    x="City",
                    y="Average Maximum Temperature",
                    color="City",
                    title="Average Maximum Temperature (°C)",
                    text_auto=".2f"
                )
                fig_temp.update_layout(showlegend=False)
                st.plotly_chart(
                    fig_temp,
                    use_container_width=True
                )

            with col2:
                fig_rain = px.bar(
                    weather_comparison,
                    x="City",
                    y="Annual Rainfall",
                    color="City",
                    title="Annual Rainfall (mm)",
                    text_auto=".2f"
                )
                fig_rain.update_layout(showlegend=False)
                st.plotly_chart(
                    fig_rain,
                    use_container_width=True
                )

            # Weather Insights
            st.divider()
            st.subheader("💡 Smart Weather Insights")

            with st.container(border=True):

                if city1_temp < city2_temp:
                    cooler_city = city1
                    cooler_temp = city1_temp
                elif city2_temp < city1_temp:
                    cooler_city = city2
                    cooler_temp = city2_temp
                else:
                    cooler_city = None

                if city1_rain > city2_rain:
                    rainier_city = city1
                    rainier_rain = city1_rain
                elif city2_rain > city1_rain:
                    rainier_city = city2
                    rainier_rain = city2_rain
                else:
                    rainier_city = None

                if cooler_city:
                    st.success(
                        f"**{cooler_city}** has the lower average daytime "
                        f"maximum temperature: **{cooler_temp:.2f} °C**."
                    )
                else:
                    st.info("Both cities have the same average high temperature.")

                if rainier_city:
                    st.info(
                        f"**{rainier_city}** receives more annual rainfall: "
                        f"**{rainier_rain:,.2f} mm**."
                    )
                else:
                    st.info("Both cities receive the same annual rainfall.")

        # =====================================
        # COST OF LIVING
        # =====================================

        elif comparison_section == "Cost of Living":

            st.header("🛒 Cost of Living Comparison")

            col1, col2 = st.columns(2)

            with col1:
                with st.container(border=True):
                    st.subheader(f"📍 {city1}")
                    st.metric(
                        "Average Listed Item Price",
                        f"Rs. {city1_avg:,.2f}"
                    )
                    st.metric(
                        "Highest Item Price",
                        f"Rs. {city1_highest:,.2f}"
                    )
                    st.metric(
                        "Lowest Item Price",
                        f"Rs. {city1_lowest:,.2f}"
                    )

            with col2:
                with st.container(border=True):
                    st.subheader(f"📍 {city2}")
                    st.metric(
                        "Average Listed Item Price",
                        f"Rs. {city2_avg:,.2f}"
                    )
                    st.metric(
                        "Highest Item Price",
                        f"Rs. {city2_highest:,.2f}"
                    )
                    st.metric(
                        "Lowest Item Price",
                        f"Rs. {city2_lowest:,.2f}"
                    )

            # Price Difference
            st.divider()
            st.subheader("📊 Price Difference")

            avg_difference = abs(city1_avg - city2_avg)

            col1, col2 = st.columns(2)

            with col1:
                st.metric(
                    "Average Price Difference",
                    f"Rs. {avg_difference:,.2f}"
                )

            with col2:
                if city1_avg > city2_avg:
                    higher_price_city = city1
                elif city2_avg > city1_avg:
                    higher_price_city = city2
                else:
                    higher_price_city = None

                st.metric(
                    "Higher Average Listed Price",
                    higher_price_city if higher_price_city else "Equal"
                )

            # Item-wise Comparison
            st.divider()
            st.subheader("📊 Essential Item Price Comparison")

            selected_item = st.selectbox(
                "Select an Item to Compare",
                cost_df["Item"].dropna().unique(),
                key="comparison_item"
            )

            item_data = cost_df[
                cost_df["Item"] == selected_item
            ].iloc[0]

            item_comparison = pd.DataFrame({
                "City": [city1, city2],
                "Price": [
                    item_data[city1],
                    item_data[city2]
                ]
            }).dropna()

            if not item_comparison.empty:

                fig_item = px.bar(
                    item_comparison,
                    x="City",
                    y="Price",
                    color="City",
                    title=f"Price Comparison: {selected_item}",
                    text_auto=".2f"
                )

                fig_item.update_layout(
                    showlegend=False,
                    yaxis_title="Price (Rs.)",
                    xaxis_title="City"
                )

                st.plotly_chart(
                    fig_item,
                    use_container_width=True
                )

            else:
                st.warning("No price data available for this item in the selected cities.")

            st.caption(
                f"Unit: {item_data['Unit']} | "
                "Prices are based on the available PBS data."
            )

            # Cost Insight
            st.divider()
            st.subheader("💡 Cost of Living Insight")

            if higher_price_city:
                st.info(
                    f"**{higher_price_city}** has a higher average "
                    "listed item price among the selected cities."
                )
            else:
                st.success(
                    "Both cities have the same average listed item price."
                )

            st.caption(
                "Note: This is a simple average of available listed item "
                "prices across different items and units, not an official "
                "cost-of-living index."
            )

        # =====================================
        # ECONOMIC COMPARISON
        # =====================================

        elif comparison_section == "Economy":

            st.header("📊 Economic Comparison")

            col1, col2 = st.columns(2)

            with col1:
                with st.container(border=True):
                    st.subheader(f"📍 {city1}")
                    st.metric(
                        "Business Establishments",
                        f"{city1_economic['Establishments']:,}"
                    )
                    st.metric(
                        "Workforce",
                        f"{city1_economic['Workforce']:,}"
                    )

            with col2:
                with st.container(border=True):
                    st.subheader(f"📍 {city2}")
                    st.metric(
                        "Business Establishments",
                        f"{city2_economic['Establishments']:,}"
                    )
                    st.metric(
                        "Workforce",
                        f"{city2_economic['Workforce']:,}"
                    )

            # Economic Charts
            st.divider()
            st.subheader("📊 Visual Economic Comparison")

            comparison_data = pd.DataFrame({
                "City": [city1, city2],
                "Business Establishments": [
                    city1_economic["Establishments"],
                    city2_economic["Establishments"]
                ],
                "Workforce": [
                    city1_economic["Workforce"],
                    city2_economic["Workforce"]
                ]
            })

            col1, col2 = st.columns(2)

            with col1:
                fig_establishments = px.bar(
                    comparison_data,
                    x="City",
                    y="Business Establishments",
                    color="City",
                    title="Business Establishments Comparison",
                    text_auto=True
                )
                fig_establishments.update_layout(showlegend=False)
                st.plotly_chart(
                    fig_establishments,
                    use_container_width=True
                )

            with col2:
                fig_workforce = px.bar(
                    comparison_data,
                    x="City",
                    y="Workforce",
                    color="City",
                    title="Workforce Comparison",
                    text_auto=True
                )
                fig_workforce.update_layout(showlegend=False)
                st.plotly_chart(
                    fig_workforce,
                    use_container_width=True
                )

            # Economic Insights
            st.divider()
            st.subheader("💡 Economic Insights")

            if city1_economic["Establishments"] > city2_economic["Establishments"]:
                st.success(f"🏢 {city1} has more business establishments.")
            elif city2_economic["Establishments"] > city1_economic["Establishments"]:
                st.success(f"🏢 {city2} has more business establishments.")
            else:
                st.info("Both cities have equal business establishments.")

            if city1_economic["Workforce"] > city2_economic["Workforce"]:
                st.info(f"👥 {city1} has a larger recorded workforce.")
            elif city2_economic["Workforce"] > city1_economic["Workforce"]:
                st.info(f"👥 {city2} has a larger recorded workforce.")
            else:
                st.info("Both cities have equal recorded workforce.")

        # =====================================
        # DOWNLOAD REPORT
        # =====================================

        elif comparison_section == "Report":

            st.header("📥 Download Comparison Report")

            report_data = pd.DataFrame({
                "Metric": [
                    "Average Maximum Temperature (°C)",
                    "Annual Rainfall (mm)",
                    "Average Listed Item Price (Rs.)",
                    "Business Establishments",
                    "Workforce"
                ],
                city1: [
                    city1_temp,
                    city1_rain,
                    city1_avg,
                    city1_economic["Establishments"],
                    city1_economic["Workforce"]
                ],
                city2: [
                    city2_temp,
                    city2_rain,
                    city2_avg,
                    city2_economic["Establishments"],
                    city2_economic["Workforce"]
                ]
            })

            st.write(
                f"Your comparison report for **{city1}** and **{city2}** is ready."
            )

            csv_report = report_data.to_csv(
                index=False
            ).encode("utf-8")

            st.download_button(
                label="⬇️ Download City Comparison CSV",
                data=csv_report,
                file_name=f"{city1}_vs_{city2}_comparison.csv",
                mime="text/csv"
            )

            st.dataframe(
                report_data,
                use_container_width=True,
                hide_index=True
            )
