from config import get_envs, Settings
from logger import logger
import streamlit as st

from gemini import GeminiInference
from video_processor import VideoProcessor

env_vars: Settings = get_envs()

def page_setup():
    st.set_page_config(page_title="NoBinge", layout="wide", page_icon="🐧")
    st.header("NoBinge")
    
    if env_vars.GEMINI_API_KEY=="GEMINI_API_KEY":
        st.sidebar.error("Gemini API Key needed in the env...", icon="ℹ️")
        st.stop()

    st.session_state.gemini_api_key = env_vars.GEMINI_API_KEY


if __name__ == "__main__":
    logger.info('############NoBinge#############')
    logger.info(env_vars)


    page_setup()

    # Setting up Gemini
    try:
        logger.info("Setting up Gemini")
        gemini_inference = GeminiInference(st.session_state.gemini_api_key)
    except Exception as e:
        logger.error(f"Failed to Set up Gemini: {str(e)}")
        st.error(f"Failed to Set up Gemini: {str(e)}")
        del st.session_state.gemini_api_key
        st.rerun()

    st.sidebar.header("Add the file paths to Video and Subtitle to analyse: ")
    video_file = st.sidebar.text_input("Add Path to Video File")
    subtitle_file = st.sidebar.text_input("Add Path to Subtitle File")
    process_button = st.sidebar.button("🚀 Process Video")

    # Processing the video and subs
    if process_button and video_file and subtitle_file:


        logger.info(f"Processing (video file): {video_file}")
        logger.info(f"Processing (subtitle file): {subtitle_file}")

        status_container = st.container()
        with status_container:
            st.markdown(f"<b>Processing (video file): {video_file}</b>",  unsafe_allow_html=True)
            st.markdown(f"<b>Processing (subtitle file): {subtitle_file}</b>",  unsafe_allow_html=True)
            status_log = st.container()
            progress_bar = st.progress(0)
            

        with st.spinner("Processing video..."):
            a=0
            for num in range(10000000):
                a=a+num

            video_object = VideoProcessor(video_file)
            video_metadata = video_object.get_metadata()
            #with status_log:
            status_log.markdown(video_metadata)
            progress_bar.progress(5)