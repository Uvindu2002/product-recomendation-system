import streamlit as st
from show_product_page import show_product_page
from product_details_page import product_details_page
from profile_page import profile_page  # Import the profile management page
from auth import signup, login, logout

# Initialize session state for navigation and user authentication
if 'page' not in st.session_state:
    st.session_state.page = 'show_products'

if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False

# State to track whether the user is in "Login" or "Sign Up" mode
if 'auth_mode' not in st.session_state:
    st.session_state.auth_mode = 'none'  # Can be 'login', 'signup', or 'none'

# Initialize user email and input fields if not already set
if 'user_email' not in st.session_state:
    st.session_state.user_email = None

# Sidebar for navigation and authentication
st.sidebar.title("Navigation")

if st.session_state.logged_in:
    # Display a welcome message with the username
    if 'username' in st.session_state:
        st.sidebar.write(f"Welcome, {st.session_state['username']}!")

    # Show Profile and Logout options when logged in
    if st.sidebar.button("Profile", key="profile_button"):
        st.session_state.page = 'profile'  # Navigate to the profile page
    if st.sidebar.button("Log Out", key="logout_button"):
        logout()
        st.session_state.page = 'show_products'  # Redirect to product page after logout
else:
    st.sidebar.subheader("User Authentication")

    # Show only the buttons initially if no login/signup form is shown
    if st.session_state.auth_mode == 'none':
        if st.sidebar.button("Log In", key="show_login_button"):
            st.session_state.auth_mode = 'login'  # Show login fields
            st.experimental_rerun()  # Rerun to show the login form

        if st.sidebar.button("Sign Up", key="show_signup_button"):
            st.session_state.auth_mode = 'signup'  # Show signup fields
            st.experimental_rerun()  # Rerun to show the signup form

    # If the user clicks "Login", show login fields
    if st.session_state.auth_mode == 'login':
        email = st.sidebar.text_input(
            "Email", 
            key="email_input", 
            placeholder="Enter your email"
        )
        password = st.sidebar.text_input(
            "Password", 
            type="password", 
            key="password_input", 
            placeholder="Enter your password"
        )

        if st.sidebar.button("Log In", key="login_button"):
            user_data = login(email, password)  # Assuming login returns user data
            if user_data:  # Check if user_data is valid
                st.session_state.auth_mode = 'none'  # Hide login fields after success
                st.experimental_rerun()  # Refresh the app to show the updated state

    # If the user clicks "Sign Up", show signup fields (with Username)
    if st.session_state.auth_mode == 'signup':
        username = st.sidebar.text_input(
            "Username", 
            key="signup_username_input", 
            placeholder="Enter your username"
        )
        email = st.sidebar.text_input(
            "Email", 
            key="signup_email_input", 
            placeholder="Enter your email"
        )
        password = st.sidebar.text_input(
            "Password", 
            type="password", 
            key="signup_password_input", 
            placeholder="Enter your password"
        )

        if st.sidebar.button("Sign Up", key="signup_button"):
            if signup(username, email, password):  # Passing username as well
                st.session_state.auth_mode = 'login'  # Switch to login form after successful signup
                st.success("Sign up successful! Please log in.")
                
                # Force an immediate rerun after successful sign-up
                st.experimental_rerun()

# Main content area
st.title("Welcome to the E-Commerce Platform")
st.write("Discover your favorite products and manage your profile.")

# Add a button for navigating to the show_products page
if st.button("View Products", key="view_products_main"):
    st.session_state.page = 'show_products'  # Navigate to the product page

# Add some styling to separate sections visually
st.markdown("---")

# Routing logic
if st.session_state.page == 'show_products':
    show_product_page()  # Display the product page for all users
elif st.session_state.page == 'product_details':
    product_details_page()  # Product details page
elif st.session_state.logged_in and st.session_state.page == 'profile':
    profile_page()  # Navigate to the profile management page
else:
    st.warning("Please log in to view profile and manage preferences.")

# Display seasonal recommendations if available
if st.session_state.get('seasonal_recommendations', []):
    st.subheader("Seasonal Recommendations")
    for recommendation in st.session_state.seasonal_recommendations:
        st.write(recommendation)  # Display seasonal recommendations

# Additional styling for better aesthetics
st.markdown("""
<style>
    .stTitle {
        font-size: 2.5em;
        color: #3572EF;
        text-align: center;
    }
</style>
""", unsafe_allow_html=True)