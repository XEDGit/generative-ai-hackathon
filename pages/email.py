import streamlit as st
from utils.nav_page import nav_page
from utils.retrieve_db import retrieve_db


st.set_page_config(initial_sidebar_state="collapsed")
if "uuid" not in st.session_state:
	nav_page("main")
if "show" in st.session_state:
	arr = retrieve_db(st.session_state["show"])
	st.write("Hello, here is the summary of the last meeting:")
	st.header("Summary:")
	st.write(arr[2])
	st.header("Tasks:")
	st.write(arr[3])
	st.header("Q&A:")
	st.write(arr[4])
else:
	st.write("Error retrieving informations")
if st.button("Back"):
	nav_page("display")