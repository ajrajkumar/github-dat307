import streamlit as st
from page.login_page import login_page
from page.signup_page import signup_page
from page.app import app_page
from utils.init_session import init_session, reset_session

init_session()

if st.session_state['authenticated']:
    app_page()
else:
    print(st.session_state['page'])
    if st.session_state['page'] == 'login':
        reset_session()
        print("calling the login page")
        login_page()
    elif st.session_state['page'] == 'signup':
        print("calling the signup page")
        signup_page()
