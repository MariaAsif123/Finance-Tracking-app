import streamlit as st
import sqlite3
import time
from utils.expenseTracker import ExpenseManager
from utils.expenseTracker import IncomeManager
from utils.expenseTracker import Account
from auth import AuthManager


st.title("Syntego")
st.write("An AI powered fianace tracker.")

auth = AuthManager()

#Session state for tracking login
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.user_email = ""

tab1, tab2 = st.tabs([" 🔑 Login", " Register"])

with tab1:
    st.subheader("Login")
    email = st.text_input("Email")
    password = st.text_input("Password" , type="password")
    login_btn = st.button("Login")

    if login_btn :
        if auth.login_user(email, password):
            st.session_state.logged_in = True
            st.session_state.user_email = email
            st.success("Login successful! Redirecting...")
            time.sleep(1.5)
            st.rerun()
        else:
            st.error("Invalid email or password.")
        
with tab2:
    st.subheader("Register")
    new_email = st.text_input("New Email")
    new_password = st.text_input("New Password", type="password")
    register_btn = st.button("Register")

    if register_btn:
        if auth.register_user(new_email, new_password):
            st.success("Registration succesful! Please Log in.")
        else:
            st.error("Email already exists.")

#Check if user is logged in
if st.session_state.logged_in:

    st.success("Head to side bar to use features.")


#Dynamically set the database name
db_name = "expenses.db"

#Initializing the managers with the database name
ExManager = ExpenseManager(db_name=db_name)
InManager = IncomeManager(db_name=db_name)
account =Account(db_name=db_name)

#Establisih SQLite database connection for testing
conn = sqlite3.connect(db_name)
c = conn.cursor()

if st.session_state.logged_in:

#Toast notification
    st.toast("Welocme to Syntego! ")

#Close the connection
conn.close()
