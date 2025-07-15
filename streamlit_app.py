# Import dependencies
import streamlit as st
import pandas as pd
import gspread # New import
import json # New import

# --- Configuration ---
# Define the Spreadsheet ID (NOT the full URL for gspread)
# This ID is used by gspread to open the specific Google Sheet.
GOOGLE_SHEET_ID = "1w2QpOugxd_gHw2r2nZyQo_IEGwoQPUcQIWNtdLEy0us" 

# --- Gspread Authentication and Connection ---
@st.cache_resource # Cache the connection to avoid re-authenticating on every rerun
def get_gspread_client():
    # Load the service account credentials from Streamlit secrets
    # The key 'gcp_service_account' must match what you put in secrets.toml
    service_account_info = json.loads(st.secrets["gcp_service_account"])
    
    # Authorize gspread with the service account credentials
    gc = gspread.service_account_from_dict(service_account_info)
    return gc

# Get the gspread client
gc = get_gspread_client()

# Open the Google Spreadsheet by its ID
try:
    spreadsheet = gc.open_by_key(GOOGLE_SHEET_ID)
except gspread.exceptions.SpreadsheetNotFound:
    st.error(f"Error: Google Spreadsheet with ID '{GOOGLE_SHEET_ID}' not found or accessible. "
             "Please check the ID and sharing permissions for your service account.")
    st.stop() # Stop the app if the spreadsheet isn't found
except Exception as e:
    st.error(f"Error connecting to Google Spreadsheet: {e}")
    st.stop()

# --- Read Data from Multiple Worksheets using gspread ---

# Function to read a worksheet into a DataFrame
@st.cache_data(ttl=3600) # Cache data for 1 hour
def load_worksheet_data(spreadsheet_id, worksheet_name): # Changed signature
    # Get the gspread client again (it's cached, so this is fast)
    gc_internal = get_gspread_client()
    
    # Open the spreadsheet inside the cached function
    # This ensures the spreadsheet object is created within the scope of the cached function's run
    # and not passed as an unhashable parameter.
    try:
        sheet_obj_internal = gc_internal.open_by_key(spreadsheet_id)
        worksheet = sheet_obj_internal.worksheet(worksheet_name)
        data = worksheet.get_all_records()
        df = pd.DataFrame(data)
        return df
    except gspread.exceptions.WorksheetNotFound:
        st.error(f"Error: Worksheet '{worksheet_name}' not found in the spreadsheet.")
        return pd.DataFrame()
    except Exception as e:
        st.error(f"Error reading worksheet '{worksheet_name}': {e}")
        return pd.DataFrame()

# Read Sheet 1 (Products)
df_products = load_worksheet_data(GOOGLE_SHEET_ID, "Products")

# Read Sheet 2 (Sales Reps)
df_sales_reps = load_worksheet_data(GOOGLE_SHEET_ID, "Sales Reps")

# Read Sheet 3 (Real-time Sales Record from Google Form)
df_sales = load_worksheet_data(GOOGLE_SHEET_ID, "Sales Record")

# Read Sheet 4 (Historical Sales Records)
df_historical_sales = load_worksheet_data(GOOGLE_SHEET_ID, "Sales Records")

# Read Sheet 5 (Individual KPIs)
df_kpi = load_worksheet_data(GOOGLE_SHEET_ID, "KPI Settings")

# Read Sheet 6 (Processed Sales Records)
df_processed_sales = load_worksheet_data(GOOGLE_SHEET_ID, "Calculations")


# --- Streamlit App Layout ---

st.title("GadgetHub Data")

st.markdown("""
Welcome to the GadgetHub Data! This application allows you to explore various datasets
related to our products, sales operations, and performance metrics, all sourced directly from
Google Sheets using `gspread`. Use the tabs below to navigate through different data views.
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
