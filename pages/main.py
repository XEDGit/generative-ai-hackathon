import streamlit as st
import os
import whisper
from utils.nav_page import nav_page

st.set_page_config(initial_sidebar_state="collapsed")
ts_model = whisper.load_model("base")
col1, col2 = st.columns(2)
with col1:
    st.title("MeetMate")
with col2:
    if st.button("List meetings"):
        nav_page("list")

audio_file = st.file_uploader("Upload your recording", type=['mp3', 'wav'])
if audio_file:
    with open("audio.mp3", "wb") as f:
        f.write(audio_file.getbuffer())
    transcription = ts_model.transcribe("audio.mp3")["text"]
    os.remove("audio.mp3")
    with open("new_transcript.txt", "wb") as f:
        f.write(bytes(transcription, encoding="utf8"))
        f.close()
    i = -1
    if "index" in st.session_state:
        i = st.session_state["index"]
    st.session_state.clear()
    if i != -1:
        st.session_state["index"] = i
    nav_page("summary")
