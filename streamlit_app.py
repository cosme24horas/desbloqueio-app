import streamlit as st
import hmac

st.session_state.status = st.session_state.get("status", "unverified")
st.title("My login page")


def check_password():
    if hmac.compare_digest(st.session_state.password, st.secrets.password):
        st.session_state.status = "verified"
    else:
        st.session_state.status = "incorrect"
    st.session_state.password = ""

def login_prompt():
    st.text_input("Enter password:", key="password", on_change=check_password)
    if st.session_state.status == "incorrect":
        st.warning("Incorrect password. Please try again.")

def logout():
    st.session_state.status = "unverified"

def welcome():
    st.success("Login successful.")
    st.button("Log out", on_click=logout)


if st.session_state.status != "verified":
    login_prompt()
    st.stop()
welcome()