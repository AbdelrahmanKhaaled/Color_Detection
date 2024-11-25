import numpy as np
import cv2
from PIL import Image


colors = ["Red", "Orange", "Green", "Blue", "Yellow", "Black", "White", "Gray", "Light Blue", "Violet", "Pink"]
colors_exist = []

def detect_color(hsvImage, lower, upper, i):
    mask1 = cv2.inRange(hsvImage, lower, upper)
    mask_1 = Image.fromarray(mask1)
    bbox1 = mask_1.getbbox()
    if bbox1 is not None:
        return colors[i]

list_lowers = [np.array([0, 130, 130]), np.array([9, 180, 220]), np.array([32, 170, 80]), np.array([100, 160, 105]), np.array([27, 180, 240]), np.array([0, 0, 0]), np.array([0, 0, 240]), np.array([0, 0, 45]), np.array([92, 140, 180]), np.array([128, 170, 60]), np.array([150, 160, 240])]

list_uppers = [np.array([9, 255, 255]), np.array([23, 255, 255]), np.array([78, 255, 255]), np.array([128, 255, 255]), np.array([32, 255, 255]), np.array([180, 255, 15]), np.array([180, 10, 255]), np.array([180, 10, 240]), np.array([100, 255, 255]), np.array([150, 255, 255]), np.array([170, 255, 255])]

import streamlit as st
from PIL import Image
import cv2
import numpy as np
import tempfile
import os

def process_image(image):

    colors = []
    np_image = np.array(image, dtype=np.uint8)
    np_image = cv2.cvtColor(np_image, cv2.COLOR_RGB2BGR)
    hsvImage = cv2.cvtColor(np_image, cv2.COLOR_BGR2HSV)

    for i in range(len(list_uppers)):
        color = detect_color(hsvImage, list_lowers[i], list_uppers[i], i)
        if (color not in colors and color != None):
            colors.append(color)
    return colors

def process_video(video_path):

    cap = cv2.VideoCapture(video_path)
    colors = []

    while True:
        _, frame = cap.read()

        hsvImage = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        for i in range(len(list_uppers)):
            color = detect_color(hsvImage, list_lowers[i], list_uppers[i], i)
            if (color not in colors and color != None):
                colors.append(color)
        return colors

st.title("Video/Image to Text Processor")

uploaded_file = st.file_uploader("Upload an Image or Video", type=["jpg", "jpeg", "png", "mp4", "avi", "mov"])

if uploaded_file:
    
    file_type = uploaded_file.name.split(".")[-1].lower()
    
    if file_type in ["jpg", "jpeg", "png"]:
        image = Image.open(uploaded_file)
        st.image(image, caption="Uploaded Image", use_container_width=True)
        text_output = process_image(image)
        st.write("**Colors:**")
        st.write(text_output)

    elif file_type in ["mp4", "avi", "mov"]:

        with tempfile.NamedTemporaryFile(delete=False, suffix=f".{file_type}") as tmp:
            tmp.write(uploaded_file.read())
            temp_video_path = tmp.name

        st.video(temp_video_path)
        text_output = process_video(temp_video_path)
        st.write("**Colors:**")
        st.write(text_output)

        os.remove(temp_video_path)

    else:
        st.warning("Unsupported file type!")