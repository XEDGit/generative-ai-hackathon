import streamlit as st
from utils.nav_page import nav_page
from utils.retrieve_db import retrieve_db

st.set_page_config(initial_sidebar_state="collapsed")
st.title("Previous meetings:")
if "index" in st.session_state:
	num = st.session_state["index"]
	for i in range(num + 1):
		arr = retrieve_db(i)
		st.header(f"Meeting {arr[0]}")
		st.write(arr[2][:1000])
		if st.button("Show more", key=f"button{str(i)}"):
			st.session_state["show"] = i
			nav_page("display")
		st.write("__________________________________")
else:
	st.write("Nothing to show")
if st.button("Create new"):
	nav_page("main")