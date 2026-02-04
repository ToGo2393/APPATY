import streamlit as st
import hashlib
from utils import db

def init_session():
    """Initialize session state variables (Required by app.py)."""
    if 'user' not in st.session_state:
        st.session_state.user = None
    if 'history' not in st.session_state:
        st.session_state.history = []

def make_hashes(password):
    return hashlib.sha256(str.encode(password)).hexdigest()

def check_hashes(password, hashed_text):
    return make_hashes(password) == hashed_text

def render_auth_sidebar():
    db.init_db()
    if 'user' not in st.session_state:
        st.session_state.user = None

    if st.session_state.user is None:
        menu = ["Login", "Sign Up"]
        choice = st.sidebar.selectbox("Account Access", menu)

        if choice == "Login":
            # Retrieve saved user
            saved_user = st.query_params.get("remembered_user", "")
            
            username = st.sidebar.text_input("Username", value=saved_user).lower().strip()
            password = st.sidebar.text_input("Password", type='password')
            
            remember_me = st.sidebar.checkbox("Remember Me")
            
            if st.sidebar.button("Login"):
                user_data = db.get_user(username)
                if not user_data.empty:
                    stored_pw = user_data.iloc[0]['password']
                    if check_hashes(password, stored_pw):
                        # Handle Remember Me Logic
                        if remember_me:
                            st.query_params["remembered_user"] = username
                        else:
                            st.query_params.clear()
                            
                        # Convert DataFrame row to dict for session state
                        st.session_state.user = user_data.iloc[0].to_dict()
                        st.sidebar.success(f"Welcome {username}")
                        st.rerun()
                    else:
                        st.sidebar.error("Invalid password")
                else:
                    st.sidebar.error("User not found")

        else: # Sign Up
            new_user = st.sidebar.text_input("Username").lower().strip()
            new_pw = st.sidebar.text_input("Password", type='password')
            confirm_pw = st.sidebar.text_input("Confirm Password", type='password')
            
            if st.sidebar.button("Register"):
                if new_user and new_pw:
                    if new_pw != confirm_pw:
                        st.sidebar.error("Passwords do not match!")
                    else:
                        hashed_pw = make_hashes(new_pw)
                        success, msg = db.add_user(new_user, hashed_pw)
                        if success:
                            st.sidebar.success(msg)
                            st.sidebar.info("Success! Please switch to the 'Login' tab to enter.")
                        else:
                            st.sidebar.error(msg)
                else:
                   st.sidebar.warning("Please fill all fields.")

        # --- Visual Divider & Social Login ---
        st.sidebar.markdown("---")
        st.sidebar.markdown("<div style='text-align: center; color: #666; font-size: 0.8em; margin-bottom: 10px;'>OR CONTINUE WITH</div>", unsafe_allow_html=True)
        
        if st.sidebar.button("🔵 Continue with Google", use_container_width=True):
             st.sidebar.info("Social Login integration is coming soon in the production version!")
             
        if st.sidebar.button("🍏 Continue with Apple", use_container_width=True):
             st.sidebar.info("Social Login integration is coming soon in the production version!")
             
        if st.sidebar.button("🤖 Continue with Android Account", use_container_width=True):
             st.sidebar.info("Social Login integration is coming soon in the production version!")

    else:
        st.sidebar.write(f"Logged in as: **{st.session_state.user['username']}**")
        
        # Premium Badge
        if st.session_state.user.get('is_premium'):
             st.sidebar.success("🌟 Premium Logic Active")
        
        if st.sidebar.button("Logout"):
            st.session_state.user = None
            st.rerun()
