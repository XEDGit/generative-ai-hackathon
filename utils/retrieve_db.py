import streamlit as st

def retrieve_db(i):
	if "uuid" not in st.session_state:
		return ["Error: no uuid" * 6]
	with open("db/db{}{}.txt".format(i, st.session_state["uuid"]), "r") as f:
		content = f.read()
		f.close()
	if not content:
		raise Exception("File read failed")
	arr = content.split('-')
	return arr