import streamlit as st
import pandas as pd
from db import save_user_preferences, get_user_preferences

# Load dataset (assuming the file is in the same directory)
@st.cache_data
def load_data():
    return pd.read_csv('product_data_new.csv')

# Function to display and manage the user profile
def profile_page():
    st.title("User Profile")

    # Get the current user's email from session state
    email = st.session_state.get('user_email')

    if not email:
        st.warning("Please log in to view your profile.")
        return

    # Display the current user's email
    st.write("Logged in as:", email)

    # Load user preferences from the database
    user_preferences = get_user_preferences(email)

    # Display current user preferences
    st.subheader("Current Preferences")
    
    # Use columns to create a card-like appearance
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("### Favorite Categories")
        for category in user_preferences.get("favorite_categories", []):
            st.markdown(f"🌟 {category}")

    with col2:
        st.markdown("### Preferred Brands")
        for brand in user_preferences.get("preferred_brands", []):
            st.markdown(f"🏷️ {brand}")

    # Load the product data
    data = load_data()

    # Extract unique categories and brands from the dataset
    categories = data['Category'].unique().tolist()
    brands = data['Brand'].unique().tolist()

    # Allow users to update their preferences
    st.subheader("Update Preferences")

    # Multi-select for favorite categories
    favorite_categories = st.multiselect(
        "Select your favorite categories:",
        options=categories,
        default=user_preferences.get("favorite_categories", []),
        format_func=lambda x: f"✨ {x}"  # Adding an emoji for visual appeal
    )

    # Multi-select for preferred brands
    preferred_brands = st.multiselect(
        "Select your preferred brands:",
        options=brands,
        default=user_preferences.get("preferred_brands", []),
        format_func=lambda x: f"🏷️ {x}"  # Adding an emoji for visual appeal
    )

    # Save changes button
    if st.button("Save Changes"):
        # Ensure uniqueness and filter out empty strings
        preferences = {
            "favorite_categories": list(filter(None, set(favorite_categories))),  # Ensure uniqueness and filter
            "preferred_brands": list(filter(None, set(preferred_brands))),  # Ensure uniqueness and filter
            "recent_views": user_preferences.get("recent_views", []),  # Keep existing recent views
            "purchases": user_preferences.get("purchases", [])  # Keep existing purchases
        }

        # Attempt to save preferences and check if successful
        if save_user_preferences(email, preferences):
            st.success("Preferences updated successfully!")
        else:
            st.error("Error updating preferences. Please try again.")
            st.write("Debug Info:", preferences)  # Show the preferences for debugging

# You may want to run this function directly if this script is the main module
# if __name__ == "__main__":
#     profile_page()
