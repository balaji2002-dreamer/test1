import streamlit as st
import sqlite3
from hashlib import sha256
from streamlit_option_menu import option_menu
from home import home_page
from identify import identify_page
from about import about

# Database connection
conn = sqlite3.connect('users.db', check_same_thread=False)
c = conn.cursor()

# Function to create a new table in the database
def create_usertable():
    c.execute('CREATE TABLE IF NOT EXISTS userstable(username TEXT, password TEXT)')
    conn.commit()

# Function to add a new user to the table
def add_userdata(username, password):
    c.execute('INSERT INTO userstable(username, password) VALUES (?,?)', (username, password))
    conn.commit()

# Function to verify user login
def login_user(username, password):
    c.execute('SELECT * FROM userstable WHERE username =? AND password = ?', (username, password))
    data = c.fetchall()
    return data

# Function to hash a password
def make_hashes(password):
    return sha256(password.encode()).hexdigest()

# Function to check if a user exists
def check_user(username, hashed_password):
    c.execute('SELECT * FROM userstable WHERE username =? AND password = ?', (username, hashed_password))
    data = c.fetchall()
    return data

# Initialize session state for user login
if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False
    st.session_state['username'] = ''

# Layout for Sign Up and Login
def login_page():
    st.title("Login")

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        create_usertable()
        hashed_password = make_hashes(password)
        result = login_user(username, hashed_password)
        if result:
            st.session_state['logged_in'] = True
            st.session_state['username'] = username
            st.success("Logged In as {}".format(username))
        else:
            st.warning("Incorrect Username/Password")

def signup_page():
    st.title("Sign Up")

    new_user = st.text_input("Username")
    new_password = st.text_input("Password", type="password")

    if st.button("Sign Up"):
        create_usertable()
        add_userdata(new_user, make_hashes(new_password))
        st.success("You have successfully created an account!")
        st.info("Go to the Login Menu to login")

# Combine the login and sign-up functionality with the main home page
def main():
    with st.sidebar:
        if st.session_state['logged_in']:
            selected = option_menu(menu_title="Main Menu", options=["Home", "Identify", "About","Logout"],
                                   icons=["house-door", "envelope", "book","box-arrow-right"],
                                   menu_icon="cast",
                                   default_index=0,)
        else:
            selected = option_menu(menu_title="Main Menu", options=["Home", "Sign Up", "Login"],
                                   icons=["house-door", "signup", "box-arrow-in-right"],
                                   menu_icon="cast",
                                   default_index=0,)

    if st.session_state['logged_in']:
        if selected == "Home":
            home_page()
        elif selected == "Identify":
            identify_page()
        elif selected == "About":
            about()
        elif selected == "Logout":
            st.session_state['logged_in'] = False
            st.session_state['username'] = ''
            st.success("You have been logged out.")
            st.experimental_rerun()

    else:
        if selected == "Home":
            home_page()
        elif selected == "Sign Up":
            signup_page()
        elif selected == "Login":
            login_page()

if __name__ == "__main__":
    main()
