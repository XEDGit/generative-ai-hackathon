import openai
import requests
import streamlit as st
import utils.text_elaboration as te
from utils.nav_page import nav_page
import time
import datetime
import os

st.set_page_config(initial_sidebar_state="collapsed")
def write_edit():
	del st.session_state["edit"]
	st.session_state["edit_transcript_{}.txt".format(st.session_state["uuid"])] = st.session_state["edit_text"]

if "uuid" not in st.session_state:
	nav_page("main")
og_path = "new_transcript_{}.txt".format(st.session_state["uuid"])
edit_path = "edit_transcript_{}.txt".format(st.session_state["uuid"])
if edit_path in st.session_state:
	og_path = edit_path
transcription = st.session_state[og_path]
if not transcription:
	raise Exception("No data found")
st.title("Edit report")
st.header("Transcription:")
if "edit" not in st.session_state:
	with st.expander("{}...".format(".".join(transcription.split(".")[:2]))):
		st.write(transcription)
else:
	st.text_area("Input:", value=transcription, on_change=write_edit, key="edit_text")
tr1, tr2 = st.columns(2, gap="small")
with tr1:
	if st.button("Back to original"):
		try:
			os.remove(edit_path)
			time.sleep(1)
		except:
			pass
with tr2:
	if "edit" not in st.session_state:
		if st.button("Edit text"):
			st.session_state["edit"] = True
tab1, tab2, tab3 = st.tabs(["Summary", "Tasks", "Q&A"])
with tab1:
	sum1, sum2 = st.columns(2)
	with sum1:
		st.header("Summary:")
	with sum2:
		if st.button("Generate new", key="gen1"):
			del st.session_state["summary"]
	if "summary" not in st.session_state:
		with st.spinner("Loading"):
			summary = te.summarize(transcription)
		st.session_state["summary"] = summary
	else:
		summary = st.session_state["summary"]
	st.write(summary)

with tab2:
	tsk1, tsk2 = st.columns(2)
	with tsk1:
		st.header("Tasks:")
	with tsk2:
		if st.button("Generate new", key="gen2"):
			del st.session_state["tasks"]
	if "tasks" not in st.session_state:
		with st.spinner("Loading"):
			tasks = te.extract_tasks(transcription)
		st.session_state["tasks"] = tasks
	else:
		tasks = st.session_state["tasks"]
	st.write(tasks)

with tab3:
	st.header("Q&A:")
	questions, answers = te.q_a(transcription)
	qa = ""
	for n, arr in enumerate(questions):
		qs = "?".join(arr)
		qs += "?"
		st.write(qs)
		st.write(answers[n][0])
		qa += f"{qs}\n{answers[n][0]}\n"
	st.session_state["qa"] = qa

dis_save = True
if all(name in st.session_state for name in ["summary", "tasks", "qa"]):
	dis_save = False
if st.button("Save", disabled=dis_save):
	with st.spinner("Saving"):
		if "index" in st.session_state:
			st.session_state["index"] = st.session_state.get("index") + 1
		else:
			st.session_state["index"] = 0
		i = st.session_state["index"]
		openai.api_key = st.secrets["openai"]
		img = openai.Image.create(
			prompt=summary,
			n=1,
			size="1024x1024"
			)
		response = requests.get(img['data'][0]['url'])
		if response.status_code == 200:
			st.session_state["{}{}.png".format(str(i), st.session_state["uuid"])] = response.content
			now = datetime.datetime.now()
			date = now.strftime("%d/%m/%y")
			st.session_state["db{}{}.txt".format(str(i), st.session_state["uuid"])] = f"{date}\n-\n{transcription}\n-\n{summary}\n-\n{tasks}\n-\n{qa}"
		try:
			del st.session_state["summary"]
		except:
			pass
		try:
			del st.session_state["tasks"]
		except:
			pass
		try:
			del st.session_state["qa"]
		except:
			pass
		try:
			del st.session_state["edit"]
		except:
			pass
		try:
			del st.session_state["new_transcript_{}.txt".format(st.session_state["uuid"])]
		except:
			pass
		nav_page("list")