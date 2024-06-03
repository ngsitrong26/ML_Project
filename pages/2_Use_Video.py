import streamlit as st
import time
import cv2
import numpy as np
from utils import get_data_base, display_time
from modules.facemodel import Attendance
from io import BytesIO

st.set_page_config(page_title="Use Video", page_icon="📈")

st.markdown("# Use Video")
st.sidebar.header("Use Video")
st.write(
    """This demo illustrates a combination of plotting and animation with
Streamlit. We're generating a bunch of random numbers in a loop for around
5 seconds. Enjoy!"""
)

folder = "./face_database"
model = Attendance()
face_database = get_data_base(folder, model)

video = st.file_uploader("Upload video", type=["mp4"])
run = st.checkbox('Run')
show_case = st.checkbox('Show Attendance')
FRAME_WINDOW = st.image([])

if 'notified_checkin' not in st.session_state:
    st.session_state.notified_checkin = set()
if 'face_database' not in st.session_state:
    st.session_state.face_database = face_database

if video is not None:
    vid = video.name
    with open(vid, mode='wb') as f:
        f.write(video.read())
    cap = cv2.VideoCapture(vid)
else:
    st.warning("Vui lòng tải lên video trước.")

while run:
    ret, frame = cap.read()
    if not ret:
        break
    for face_data in st.session_state.face_database:
        frame = model.use_web_cam(frame, face_data)
        if face_data['time_in'] is not None:
            if face_data['name'] not in st.session_state.notified_checkin:
                st.write(f"{face_data['name']} check in successfully")
                st.session_state.notified_checkin.add(face_data['name'])
                    
    FRAME_WINDOW.image(frame)
else:
    st.write('Stopped')

if show_case:
    display_time(st.session_state.face_database)
    # for face_data in st.session_state.face_database:
    #     st.write(f"Name: {face_data['name']}")
    #     if face_data['time_in'] is None:
    #         st.write("Time in: No attendance")
    #         st.write("Time out: No attendance")
    #         st.write("=====================================")
    #         continue
    #     st.write(f"Time in: {time.ctime(face_data['time_in'])}")
    #     st.write(f"Time out: {time.ctime(face_data['time_out'])}")
    #     st.write("=====================================")

