import streamlit as st

def retrieve_db(i):
	if "uuid" not in st.session_state:
		return ["Error: no uuid" * 6]
	content = st.session_state["db{}{}.txt".format(i, st.session_state["uuid"])]
	if not content:
		raise Exception("Data not found")
	arr = content.split('-')
	return arr