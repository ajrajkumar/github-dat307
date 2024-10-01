import streamlit as st
import re
from utils.cognito_handler import sign_up_user

def is_valid_email(email):
    """Check if the provided email is valid using regex."""
    email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(email_regex, email) is not None

def input_field(input_param, type):
    """Render an input field based on the type and store the value in session state."""
    if type == 'text':
        st.session_state[input_param] = st.text_input(input_param)
    elif type == 'number':
        st.session_state[input_param] = st.number_input(input_param, step=1)

def signup_page():
    """Render the signup page with optional extra input parameters and password confirmation."""
    if st.session_state['verifying']:
        auth,message = sign_up_user(st.session_state['email'],st.session_state['password'])
        if auth :
            with st.empty().container(border=True):
                st.title(f"User {st.session_state['email']} created successfully. Please login")
                if st.button("Back to Login"):
                    st.session_state['page'] = 'login'
                    st.rerun()
                    print("I am here")
        else:
            st.session_state["signup_error"] = message
            st.session_state['verifying'] = False
            st.rerun()
    else:
        if st.button("Back to Login"):
            st.session_state['page'] = 'login'
            st.rerun()
        
        with st.empty().container(border=True):
            st.title("Sign Up Page")
            
            # Email input with validation
            st.session_state['email'] = st.text_input("Email")
            if st.session_state['email'] and not is_valid_email(st.session_state['email']):
                st.error("Please enter a valid email address")

            # Password input
            st.session_state['password'] = st.text_input("Password", type='password')
            
            # Confirm password if required
            confirm_password = st.text_input("Confirm Password", type='password')

            if 'signup_error' in st.session_state:
                st.error(st.session_state['signup_error'])
            
          # Validate all required fields before proceeding
            if st.session_state['email'] and st.session_state['password'] and confirm_password \
               and (st.session_state['password'] == confirm_password):
                
                if st.button("Register"):
                    st.session_state['verifying'] = True
                    st.rerun()
            else:
                if st.session_state['password'] != confirm_password:
                    st.error("Passwords do not match")
                elif st.button("Register"):
                    st.error("Please fill in all required fields")
