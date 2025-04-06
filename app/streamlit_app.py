from config import get_envs, Settings
from logger import logger
import streamlit as st

from gemini import GeminiInference

env_vars: Settings = get_envs()

def page_setup():
    st.set_page_config(page_title="NoBinge", layout="wide", page_icon="🐧")
    st.header("NoBinge")
    
    if env_vars.GEMINI_API_KEY=="GEMINI_API_KEY":
        st.sidebar.error("Gemini API Key needed in the env...", icon="ℹ️")
        st.stop()

    st.session_state.gemini_api_key = env_vars.GEMINI_API_KEY
    st.sidebar.header("Add the file paths to Video and Subtitle to analyse: ")
    video_file = st.sidebar.text_input("Add Path to Video File")
    subtitle_file = st.sidebar.text_input("Add Path to Subtitle File")


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

    