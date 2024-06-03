import streamlit as st
import time
import cv2
import numpy as np
from utils import get_data_base, display_time
from modules.facemodel import Attendance

st.set_page_config(page_title="Check Attendance", page_icon="🌍")

st.markdown("# Check Attendance")
st.sidebar.header("Check Attendance")
st.write(
    """This demo illustrates a combination of plotting and animation with
Streamlit. We're generating a bunch of random numbers in a loop for around
5 seconds. Enjoy!"""
)

folder = "./face_database"
model = Attendance()
face_database = get_data_base(folder, model)

image = st.camera_input("Take a portrait image")

if image is not None:
    bytes_data = image.getvalue()
    image = cv2.imdecode(np.frombuffer(bytes_data, np.uint8), cv2.IMREAD_COLOR)
    model.check_attendence(image, face_database)

