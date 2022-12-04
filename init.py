from utils.nav_page import nav_page
import uuid
import streamlit as st

if "uuid" not in st.session_state:
	st.session_state["uuid"] = str(uuid.uuid1())
nav_page("main")