import streamlit as st
from utils import show_icon
import numpy as np
import os
import cv2
import time
import threading
from utils import get_data_base, display_time
from modules.facemodel import Attendance

st.set_page_config(page_title="TMT GANG",
                   page_icon=":bridge_at_night:",
                   layout="wide")
show_icon(":foggy:")
st.markdown("# :rainbow[HUST ATTENDANCE]")
st.write("# Welcome to My Project - TMT Gang! 👋")

folder = "./face_database"
model = Attendance()
face_database = get_data_base(folder, model)
FRAME_WINDOW = st.image([])
camera = cv2.VideoCapture(0)

if 'notified_checkin' not in st.session_state:
    st.session_state.notified_checkin = set()
if 'face_database' not in st.session_state:
    st.session_state.face_database = face_database
if 'student_id' not in st.session_state:
    st.session_state.student_id = None
if 'student_name' not in st.session_state:
    st.session_state.student_name = None
if 'cap' not in st.session_state:
    st.session_state.cap = None

left_column, right_column = st.columns(2)

with left_column:
    st.header("Source Image")
    source = st.radio("Get image from", ["Camera", "Upload", "Stored"])
    if source == "Camera":
        info_displayed = False
        if st.session_state.cap:
            st.session_state.cap.release()
        st.session_state.cap = cv2.VideoCapture(0)
        while st.session_state.cap.isOpened():
            _, frame = st.session_state.cap.read()
            for face_data in st.session_state.face_database:
                frame = model.use_web_cam(frame, face_data)
                # if face_data['time_in'] is not None:
                if face_data['name'] not in st.session_state.notified_checkin:
                    info_displayed = False
                    with right_column:
                        st.empty()
                    st.session_state.student_id = face_data['student_id']
                    st.session_state.student_name = face_data['name']
                    st.session_state.notified_checkin.add(face_data['name'])
            if not info_displayed:
                with right_column:
                    st.header("Information")
                    if st.session_state.student_id is not None:
                        filename = f"{st.session_state.student_name}_{st.session_state.student_id}.png"
                        image_path = os.path.join(folder, filename)
                        st.success(f"{st.session_state.student_name} check in successfully")
                        st.write(f"Student ID: {st.session_state.student_id}")
                        st.image(image_path, caption=f'Student name: {st.session_state.student_name} (Student ID: {st.session_state.student_id})')
                info_displayed = True
            FRAME_WINDOW.image(frame)
    elif source == "Upload":
        if st.session_state.cap:
            st.session_state.cap.release()
        run = st.checkbox('Play')
        video = st.file_uploader("Upload video", type=["mp4"])
        if video is not None:
            vid = video.name
            with open(vid, mode='wb') as f:
                f.write(video.read())
            st.session_state.cap = cv2.VideoCapture(vid)
        else:
            st.warning("Vui lòng tải lên video trước.")
        info_displayed = False
        while run:
            _, frame = st.session_state.cap.read()
            for face_data in st.session_state.face_database:
                frame = model.use_video(frame, face_data)
                # if face_data['time_in'] is not None:
                if face_data['name'] not in st.session_state.notified_checkin:
                    info_displayed = False
                    st.write(f"Student ID: {st.session_state.student_id}")
                    with right_column:
                        st.empty()
                    st.session_state.student_id = face_data['student_id']
                    st.session_state.student_name = face_data['name']
                    st.session_state.notified_checkin.add(face_data['name'])
            if not info_displayed:
                with right_column:
                    st.header("Information")
                    if st.session_state.student_id is not None:
                        filename = f"{st.session_state.student_name}_{st.session_state.student_id}.png"
                        image_path = os.path.join(folder, filename)
                        st.success(f"{st.session_state.student_name} check in successfully")
                        st.write(f"Student ID: {st.session_state.student_id}")
                        st.image(image_path, caption=f'Student name: {st.session_state.student_name} (Student ID: {st.session_state.student_id})')
                info_displayed = True
            FRAME_WINDOW.image(frame)


with st.sidebar:
    with st.form("my_form"):
        st.info("**Yes Sirr! Let's do it ↓**", icon="👋🏾")
    with st.expander(":rainbow[**My project here**]"):
        st.markdown(
                """
                ---
                Follow me on:

                𝕏 → [@tonykipkemboi](https://twitter.com/tonykipkemboi)

                LinkedIn → [Tony Kipkemboi](https://www.linkedin.com/in/tonykipkemboi)

                """
            )
    