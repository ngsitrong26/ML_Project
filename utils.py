import os
import cv2
import time
import streamlit as st

def get_data_base(folder_dir,model):
    list_image = os.listdir(folder_dir)
    face_database = []
    for image in list_image:
        image_path = os.path.join(folder_dir, image)
        face = model.get_embedding(cv2.imread(image_path))
        name, student_id = image.split('_')
        student_id = student_id.split('.')[0]
        face_database.append({"name": name, "student_id": student_id, "embedding": face, "time_in": None, "time_out": None})
    return face_database

def display_time(face_database):
    for face_data in face_database:
        st.write(f"Name: {face_data['name']}")
        if face_data['time_in'] is None:
            st.write("Time in: No attendance")
            st.write("Time out: No attendance")
            st.write("=====================================")
            continue
        st.write(f"Time in: {time.ctime(face_data['time_in'])}")
        st.write(f"Time out: {time.ctime(face_data['time_out'])}")
        st.write("=====================================")

@st.cache_data
def show_icon(emoji: str):
    """Shows an emoji as a Notion-style page icon.

    Args:
        emoji (str): name of the emoji, i.e. ":balloon:"
    """

    st.write(
        f'<span style="font-size: 78px; line-height: 1">{emoji}</span>',
        unsafe_allow_html=True,
    )