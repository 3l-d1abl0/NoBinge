from config import get_envs, Settings
#from config import Envs

from logger import logger
import streamlit as st


#env_vars: Envs = Envs.get_envs()
env_vars: Settings = get_envs()

def page_setup():
    st.set_page_config(page_title="NoBinge", layout="wide", page_icon="🐧")
    st.header("NoBinge")
    
    if env_vars.GEMINI_API_KEY=="GEMINI_API_KEY":
        st.sidebar.error("Gemini API Key needed in the env...", icon="ℹ️")
        st.stop()


if __name__ == "__main__":
    logger.info('############NoBinge#############')
    logger.info(env_vars)


    #page_setup()
    