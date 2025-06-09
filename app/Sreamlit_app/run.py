import streamlit as st
import requests

st.set_page_config(page_title="ChatGPT Clone", layout="centered")
st.title("ChatGPT Clone")

# --- Session State Initialization ---
if 'token' not in st.session_state:
    st.session_state.token = ""
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'show_signup' not in st.session_state:
    st.session_state.show_signup = False

# --- switches between login and signup view ---
def toggle_signup():
    st.session_state.show_signup = not st.session_state.show_signup

# --- Logout Function ---
def logout():
    st.session_state.token = ""
    st.session_state.logged_in = False
    st.experimental_rerun() if hasattr(st, "experimental_rerun") else st.rerun()

# --- SIGNUP ---
if st.session_state.show_signup:
    st.subheader("Sign Up")
    new_username = st.text_input("Choose a Username")
    new_password = st.text_input("Choose a Password", type="password")

    if st.button("Sign Up"):
        res = requests.post("http://localhost:8000/auth/signup", json={
            "username": new_username, "password": new_password
        })
        if res.ok:
            st.success("Account created! Please log in.")
            st.session_state.show_signup = False
        else:
            st.error(res.json().get("detail", "Signup failed."))

    st.button("Back to Login", on_click=toggle_signup)

# --- LOGIN ---
elif not st.session_state.logged_in:
    st.subheader("Login")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        res = requests.post("http://localhost:8000/auth/login", json={
            "username": username, "password": password
        })
        if res.ok:
            st.session_state.token = res.json()['access_token']
            st.session_state.logged_in = True
            st.success("Logged in successfully!")
            st.experimental_rerun() if hasattr(st, "experimental_rerun") else st.rerun()
        else:
            st.error(res.json().get("detail", "Login failed."))

    st.button("Create an Account", on_click=toggle_signup)

# --- CHATBOT UI ---
else:
    st.subheader("Chat with the Bot")

    if st.button("Logout"):
        logout()

    topic = st.selectbox("Choose a topic", ["Sport", "Science", "History", "Weather"])
    message = st.text_input("Your Message")

    if st.button("Send"):
        if not message.strip():
            st.warning("Please enter a message.")
        else:
            res = requests.post(
                "http://localhost:8000/chat",
                headers={"Authorization": f"Bearer {st.session_state.token}"},
                json={"message": message, "topic": topic}
            )
            if res.ok:
                st.write(res.json()["response"])
            else:
                st.error("Failed to get a response from the chatbot.")
