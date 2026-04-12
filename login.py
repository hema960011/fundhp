import hashlib
import streamlit as st

st.set_page_config(layout="wide")

from streamlit_app import render_data_viewer, logout

REGISTERED_USERS = {
    "alice": {
        "password_hash": hashlib.sha256("Secure@Password123".encode()).hexdigest(),
        "approved": True,
    }
}

def hash_password(raw_password: str) -> str:
    return hashlib.sha256(raw_password.encode()).hexdigest()

def verify_user(username: str, password: str) -> tuple[bool, str]:
    user = REGISTERED_USERS.get(username)
    if not user:
        return False, "User not found."
    if not user.get("approved", False):
        return False, "Your account is not approved yet."
    if user["password_hash"] != hash_password(password):
        return False, "Incorrect password."
    return True, ""

def initialize_session_state():
    if "logged_in" not in st.session_state:
        st.session_state.logged_in = False
        st.session_state.username = ""
        st.session_state.login_error = ""

def login():
    username = st.session_state.get("login_username", "").strip()
    password = st.session_state.get("login_password", "")
    valid, message = verify_user(username, password)
    if valid:
        st.session_state.logged_in = True
        st.session_state.username = username
        st.session_state.login_error = ""
    else:
        st.session_state.logged_in = False
        st.session_state.username = ""
        st.session_state.login_error = message

def rerun():
    try:
        st.experimental_rerun()
    except AttributeError:
        st.rerun()


def render_login_page():
    st.title("Login")
    st.subheader("Please sign in to access dashboard.")

    with st.form(key="login_form"):
        st.text_input("Username", key="login_username")
        st.text_input("Password", type="password", key="login_password")
        submitted = st.form_submit_button("Sign in")
        if submitted:
            login()
            if st.session_state.logged_in:
                rerun()

    if st.session_state.login_error:
        st.error(st.session_state.login_error)

    st.markdown("---")
    st.markdown(
        "Only registered and approved users may sign in and access the data. "
        "If your account is not approved, contact the app administrator."
    )


def render_app_header(username: str):
    title_col, control_col = st.columns([5, 1])
    with title_col:
        st.title("My Portfolio")
    with control_col:
        st.write("\n")
        st.write("\n")
        #st.markdown(f"**Logged in as**  \n**{username}**")
        if st.button("Logout", key="top_logout"):
            logout()


def main():
    initialize_session_state()

    if st.session_state.logged_in:
        render_app_header(st.session_state.username)
        render_data_viewer(st.session_state.username)
    else:
        render_login_page()

if __name__ == "__main__":
    main()
