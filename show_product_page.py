import streamlit as st
import pandas as pd
from datetime import datetime
from db import get_user_preferences  # Import the MongoDB connection from db.py
from product_details_page import product_details_page
from profile_page import profile_page
from auth import signup, login, logout

# Load dataset (assuming the file is in the same directory)
@st.cache_data
def load_data():
    return pd.read_csv('product_data_new.csv')

# Function to filter high-rated products
def get_high_rated_products(data, rating_threshold=4.0):
    return data[data['Rating'] >= rating_threshold]

# Function to get seasonal products
def get_seasonal_products(data):
    current_month = datetime.now().month
    season = 'Winter' if current_month in [12, 1, 2] else \
             'Spring' if current_month in [3, 4, 5] else \
             'Summer' if current_month in [6, 7, 8] else \
             'Autumn'
    return data[data['Season'] == season], season

def show_product_page():
    # Load the product data
    data = load_data()

    

    # Initialize search history in session state
    if 'search_history' not in st.session_state:
        st.session_state.search_history = []

    # Search bar for filtering by product name
    search_query = st.text_input("Search for products", value="")

    # Add search query to history if it is not empty
    if search_query and search_query not in st.session_state.search_history:
        st.session_state.search_history.append(search_query)

    # Display previous searches
    if st.session_state.search_history:
        st.write("Previous Searches:")
        for query in st.session_state.search_history:
            st.write(f"- {query}")

    # Category selection dropdown
    available_categories = data['Category'].unique()  # Assuming 'Category' column exists
    selected_categories = st.multiselect("Filter by categories", options=available_categories)

    # Check if the user is logged in and retrieve their preferences
    user_preferences = {}
    is_logged_in = st.session_state.get('logged_in', False)
    if is_logged_in:
        email = st.session_state.get('user_email')
        user_preferences = get_user_preferences(email)

    # Initial filtered data based on user preferences and inputs
    filtered_data = data.copy()

    # Filter products based on the search query
    if search_query:
        filtered_data = filtered_data[filtered_data['Name'].str.contains(search_query, case=False, na=False)]

    # Filter products based on selected categories
    if selected_categories:
        filtered_data = filtered_data[filtered_data['Category'].isin(selected_categories)]

    # Apply favorite brands filter if the user is logged in and no filters are used
    if is_logged_in and not (search_query or selected_categories):
        if user_preferences.get('preferred_brands'):
            filtered_data = filtered_data[filtered_data['Brand'].isin(user_preferences['preferred_brands'])]

    # Display seasonal products only if no filters are applied
    if not search_query and not selected_categories:
        # Get seasonal high-rated products
        seasonal_products, season_name = get_seasonal_products(data)
        high_rated_seasonal_products = get_high_rated_products(seasonal_products)

        # Show high-rated seasonal products
        st.subheader(f"🌟 High-Rated Products for {season_name} season 🌟")
        high_rated_seasonal_products = high_rated_seasonal_products[:9]

        # Create a grid layout to show high-rated seasonal products as cards
        cols = st.columns(3)  # Create 3 columns for card layout
        for index, product in high_rated_seasonal_products.iterrows():
            with cols[index % 3]:  # Cycle through the columns
                st.markdown(
                    f"""
                    <div style="width: 250px hidght: 250px; border: none; border-radius: 10px; padding: 10px; margin: 10px; background-color: #262730;">
                        <img src="{product['ImageURL']}" style="width: 300px; height: 250px; border-radius: 10px;" />
                        <h4 style="text-align: center;">{product['Name']}</h4>
                        <p style="font-weight: bold; text-align: center; color: #4CAF50;">Rating: {product['Rating']}</p>
                        <p style="text-align: center;">Brand: {product['Brand']}</p>
                    </div>
                    """,
                    unsafe_allow_html=True
                )

                product_id = product['product_id']
                if st.button("View Details", key=f"view_button_{product_id}_{index}"):
                    st.session_state.selected_product_id = product_id
                    st.session_state.page = 'product_details'
                    st.experimental_rerun()

    # General high-rated products section (not seasonal)
    st.subheader("🌟 Other High-Rated Products 🌟")
    high_rated_products = get_high_rated_products(filtered_data)

    # Limit to 9 products for display
    high_rated_products = high_rated_products[:9]

    # Create a grid layout to show high-rated products as cards
    cols = st.columns(3)  # Create 3 columns for card layout
    for index, product in high_rated_products.iterrows():
        with cols[index % 3]:  # Cycle through the columns
            st.markdown(
                f"""
                <div style="width: 250px hidght: 250px; border: none; border-radius: 10px; padding: 10px; margin: 10px; background-color: #262730;">
                    <img src="{product['ImageURL']}" style="width: 300px; height: 250px; border-radius: 10px;" />
                    <h4 style="text-align: center;">{product['Name']}</h4>                    
                    <p style="font-weight: bold; text-align: center; color: #4CAF50;">Rating: {product['Rating']}</p>
                    <p style="text-align: center;">Brand: {product['Brand']}</p>
                </div>
                """,
                unsafe_allow_html=True
            )

            product_id = product['product_id']
            if st.button("View Details", key=f"view_button_{product_id}_{index + 100}"):
                st.session_state.selected_product_id = product_id
                st.session_state.page = 'product_details'
                st.experimental_rerun()

# Initialize session state for navigation and user authentication
if 'page' not in st.session_state:
    st.session_state.page = 'show_products'
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'user_email' not in st.session_state:
    st.session_state.user_email = None

# Set the page background color
st.markdown(
    """
    <style>
    .reportview-container {
        background-color: #F0F8FF; /* Light background color */
    }
    </style>
    """,
    unsafe_allow_html=True
)

