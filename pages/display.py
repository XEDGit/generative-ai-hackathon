import os
import streamlit as st
from utils.nav_page import nav_page
from utils.retrieve_db import retrieve_db
from PIL import Image
import io


st.set_page_config(initial_sidebar_state="collapsed")
if "uuid" not in st.session_state:
	nav_page("main")
if "show" in st.session_state:
	arr = retrieve_db(st.session_state["show"])
	img = Image.open(io.BytesIO(st.session_state["{}{}.png".format(str(st.session_state["show"]), st.session_state["uuid"])]))
	w, h = img.size
	img = img.crop((0, h/4, w, h/4*3))
	st.image(img)
	col1, col2 = st.columns(2)
	with col1:
		st.title(f"Meeting {arr[0]}")
	with col2:
		if st.button("Back"):
			nav_page("list")
	st.header("Transcription")
	st.write(arr[1])
	st.header("Summary")
	st.write(arr[2])
	st.header("Tasks")
	st.write(arr[3])
	st.header("Q&A")
	st.write(arr[4])
	foot1, foot2 = st.columns(2)
	with foot1:
		if st.button("Email format"):
			nav_page("email")
	with foot2:
		if st.button("Delete"):
			del st.session_state["{}{}.png".format(st.session_state["show"], st.session_state["uuid"])]
			del st.session_state["db{}{}.txt".format(str(st.session_state["show"]), st.session_state["uuid"])]
			nav_page("list")
else:
	st.write("Informations to show not found")
	if st.button("Back"):
			nav_page("list")