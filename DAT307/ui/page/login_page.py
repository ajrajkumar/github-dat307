import streamlit as st
from utils.cognito_handler import authenticate_user

# Pages
def login_page():
    st.set_page_config(page_title="DAT307-IDR: User Login", layout="wide")
    st.image("image/aws_logo.png",width=120)
    st.header("DAT307 - Build a Generative AI incident detection and response system powered by Amazon Aurora")
    with st.empty().container(border=True):
        col1, _, col2 = st.columns([10,1,10])
        
        with col1:
            st.write("")
            st.write("")
            st.image("image/demo.png")
        
        with col2:
            st.title("Login Page")
            email = st.text_input("E-mail",value="test1@test.com")
            password = st.text_input("Password", type="password",value="Goodluck@76")

            if st.button("Login"):
                if not (email and password):
                    st.error("Please provide email and password")
                else:
                    auth, token, message = authenticate_user(email, password)
                    if auth:
                        st.session_state['authenticated'] = True
                        st.session_state['token'] = token
                        st.session_state['page'] = 'app'
                        st.rerun()
                    else:
                        st.error(message)
            if st.button("Sign Up"):
                st.session_state['page'] = 'signup'
                st.rerun()