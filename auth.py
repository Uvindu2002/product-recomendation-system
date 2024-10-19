from firebase_config import auth
import streamlit as st
from db import save_user_info, get_user_info

def signup(username, email, password):
    try:
        user = auth.create_user_with_email_and_password(email, password)
        st.success(f"User {username} created successfully!")
        
        # Store user info (username) in the database
        save_user_info(email, username)  # Assuming you're using MongoDB

        st.session_state['user_email'] = email
        st.session_state['username'] = username  # Store the username in session state
        
    except Exception as e:
        st.error(f"Error: {str(e)}")

def login(email, password):
    try:
        user = auth.sign_in_with_email_and_password(email, password)
        st.success("Logged in successfully!")
        
        # Fetch the username from the database
        user_info = get_user_info(email)
        if user_info:
            st.session_state['username'] = user_info.get('username')  # Store the username in session state
        
        st.session_state['logged_in'] = True
        st.session_state['user_email'] = email  # Store user email in session state for later use
        st.experimental_rerun()  # Refresh the app after successful login

    except Exception as e:
        st.error(f"Error: {str(e)}")

def logout():
    # Clear session state on logout
    if 'logged_in' in st.session_state:
        st.session_state['logged_in'] = False
    if 'user_email' in st.session_state:
        del st.session_state['user_email']
    if 'username' in st.session_state:
        del st.session_state['username']
    if 'user' in st.session_state:
        del st.session_state['user']
    
    # Reset auth_mode to 'none' to show Login/Sign-Up buttons again
    st.session_state.auth_mode = 'none'

    st.success("You have been logged out.")
    st.experimental_rerun()  # Refresh the app after logout