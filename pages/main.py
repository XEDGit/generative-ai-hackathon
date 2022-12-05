import streamlit as st
import os
import whisper
from utils.nav_page import nav_page
import uuid

@st.cache
def load_model():
    return whisper.load_model("base")

st.set_page_config(initial_sidebar_state="collapsed")
if "uuid" not in st.session_state:
    st.session_state["uuid"] = str(uuid.uuid1())
ts_model = load_model()
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
    st.session_state["new_transcript_{}.txt".format(st.session_state["uuid"])] = transcription
    nav_page("summary")
st.write("Find our example recording at this link: https://drive.google.com/file/d/1jwggCXLTlBAS31wC6E6T4Iti7MO4Uwwn/view?usp=sharing")