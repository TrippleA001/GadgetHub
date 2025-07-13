# Import dependencies
import streamlit as st
import pandas as pd
from streamlit_gsheets import GSheetsConnection

# Create a connection object
conn = st.connection("gsheets", type=GSheetsConnection)

# --- Read Data from Multiple Sheets ---
# Read Sheet 1 (Products)
# This sheet contains details about the products GadgetHub sells.
products_data = conn.read(worksheet="Products")
df_products = pd.DataFrame(products_data)

# Read Sheet 2 (Sales Reps)
# This sheet holds information about the sales representatives.
sales_reps_data = conn.read(worksheet="Sales Reps")
df_sales_reps = pd.DataFrame(sales_reps_data)

# Read Sheet 3 (Real-time Sales Record from Google Form)
# This sheet is fed by a Google Form for new sales entries.
sales_data = conn.read(worksheet="Sales Record")
df_sales = pd.DataFrame(sales_data)

# Read Sheet 4 (Historical Sales Records)
# This sheet contains older sales data.
historical_sales_data = conn.read(worksheet="Sales Records")
df_historical_sales = pd.DataFrame(historical_sales_data)

# Read Sheet 5 (Individual KPIs)
# This sheet stores data related to Key Performance Indicators for individuals.
kpi_data = conn.read(worksheet="KPI Settings")
df_kpi = pd.DataFrame(kpi_data)

# Read Sheet 6 (Processed Sales Records)
# This sheet contains data that has undergone calculations.
processed_sales_data = conn.read(worksheet="Calculations")
df_processed_sales = pd.DataFrame(processed_sales_data)

# --- Streamlit App Layout ---

st.title("GadgetHub Datasets Dashboard")

st.markdown("""
Welcome to the GadgetHub Data Dashboard! This application allows you to explore various datasets
related to our products, sales operations, and performance metrics, all sourced directly from
Google Sheets. Use the tabs below to navigate through different data views.
""")

# Define tabs for each sheet
tab_products, tab_sales_reps, tab_realtime_sales, tab_historical_sales, tab_kpi, tab_processed_sales = \
    st.tabs([
        "Products",
        "Sales Reps",
        "Real-time Sales",
        "Historical Sales",
        "KPI Settings",
        "Calculations"
    ])

# Content for each tab
with tab_products:
    st.header("Product Catalog")
    st.write("Details about all products offered by GadgetHub.")
    st.dataframe(df_products)


with tab_sales_reps:
    st.header("Sales Representatives Information")
    st.write("Information about our sales team members.")
    st.dataframe(df_sales_reps)


with tab_realtime_sales:
    st.header("Real-time Sales Records (Google Form Input)")
    st.write("Latest sales entries, potentially from a Google Form.")
    st.dataframe(df_sales)


with tab_historical_sales:
    st.header("Historical Sales Records")
    st.write("Comprehensive historical sales data for in-depth analysis.")
    st.dataframe(df_historical_sales)


with tab_kpi:
    st.header("KPI Settings and Individual Performance")
    st.write("Key Performance Indicators data, likely for monitoring individual or team goals.")
    st.dataframe(df_kpi)

with tab_processed_sales:
    st.header("Processed Sales Data & Calculations")
    st.write("This tab contains data that has already undergone various calculations or transformations.")
    st.dataframe(df_processed_sales)
   

st.markdown("---") # A horizontal rule for separation
st.markdown("""
You can read the [LinkedIn post here](https://www.linkedin.com/posts/abdul-samad-abdul-jaleel_grassrootsdatascience-dashboardthinking-buildwhatmatters-activity-7347403678149967872-Dnv3 '🟢 No Data? No Problem: What I Built, What I Found')
""")
st.markdown("""
For more detailed analysis or specific reports, send a DM.
""")
