import streamlit as st
import os
from modules.facemodel import Attendance
from utils import get_data_base

database_path = "C:\Users\AU LAC COMPUTER\OneDrive - Hanoi University of Science and Technology\Năm 3\Học kỳ 20232\ML_ITTN\face_database"
name_image = st.text_input("Input name image here")
image = st.camera_input("Take a portrait image")
submit = st.button("Submit")

folder = "./face_database"
model = Attendance()
face_database = get_data_base(folder, model)

def check_existed(model, image):
    face = model.get(image)
    if len(face) == 0:
        st.error("No face found in image.")
    elif len(face) >= 2:
        st.error("Many faces have been detected in the image. Only one")
    else:
        face_embedding = face['embedding']
        for face_data in face_database:
            if model.is_face(face_data['embedding'],face_embedding):
                st.write("Already exits.")
                return True
        return False

if submit:
    if name_image and image:
        if check_existed(model, image):
            with open(os.path.join(database_path, f"{name_image}.png"), "wb") as file:
                file.write(image.getbuffer())

            st.success(f"Image saved as {name_image}.png in face_database folder")
    else:
        st.error("Please provide both a name and take a picture.")