import warnings
warnings.filterwarnings('ignore')
import os
os.environ["TF_CPP_MIN_LOG_LEVEL"] = "3"  # 0 = all logs, 1 = filter INFO, 2 = filter WARNING, 3 = filter ERROR
from transformers.utils import logging
logging.set_verbosity_error()

import re
import streamlit as st
import os
from pathlib import Path
from generate_wordclouds import generate_wordclouds  # your existing logic
from util_funcs.predict import counter

def extract_id(text):
    pattern = r"v=([a-zA-Z0-9_-]{11})"
    match =  re.search(pattern, text)
    if match:
        return match.group(1)
    return "invalid link"

# set output folder
OUTPUT_DIR = Path("wordclouds")


st.set_page_config(page_title="YouTube Comments Emotion Recognition System", 
                   page_icon="assets/youtube_logo.png",
                    layout="wide")

st.markdown(
    """
    <style>
    .block-container {
    max-width: 85%;
    }
    </style>
""", unsafe_allow_html=True
)

col1, col2 = st.columns([1, 10])
with col1:
    st.image("assets/youtube_logo.png", width=70)
with col2:
    st.title("YouTube Comments Emotion Recognition System")

# Input: YouTube video URL
youtube_link = st.text_input("Enter YouTube video link:")

youtube_link = extract_id(youtube_link)

if st.button("Generate WordClouds"):
    counter = 0

    if youtube_link.strip() == "invalid link":
        st.warning("Please enter a YouTube link.")
    else:
        # Clean output directory
        if OUTPUT_DIR.exists():
            for f in OUTPUT_DIR.glob("*.png"):
                try:
                    f.unlink()  # delete the file
                except Exception as e:
                    st.error(f"Could not delete {f}: {e}")
        else:
            OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

        with st.spinner(f"Fetching comments and generating wordclouds..."):
            progress_bar = st.progress(0, text="Starting...")
            # Call your function (it should save PNGs in output/)
            generate_wordclouds(youtube_link, progress_bar)
            progress_bar.empty()

        st.success("Wordclouds generated successfully!")

        col1, col2 = st.columns(2)
        num = 0
        # Display wordcloud images
        for img_file in sorted(OUTPUT_DIR.glob("*.png")):
            if num%2 == 0:
                with col1:
                    st.image(str(img_file), caption=img_file.stem.capitalize(), use_container_width=True)
            else:
                with col2:
                    st.image(str(img_file), caption=img_file.stem.capitalize(), use_container_width=True)
            num += 1


