from config import get_envs, Settings
from logger import logger
import streamlit as st

from gemini import GeminiInference
from video_processor import VideoProcessor
from video_indexer import VideoIndexer
from video_retriever import VideoRetriever

from pathlib import Path

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


    page_setup()

    # Setting up Gemini
    try:
        logger.info("Setting up Gemini")
        st.session_state.gemini_inference = GeminiInference(st.session_state.gemini_api_key)
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

            #Get metadata
            logger.info("Fetching video Metadata")
            video_object = VideoProcessor(video_file, subtitle_file)
            video_metadata = video_object.get_metadata()
            status_log.markdown(video_metadata)
            progress_bar.progress(5)

            #Generate Frames
            logger.info("Extracting frames...")
            #session_frames_directory = video_object.extract_frames()
            session_frames_directory = output_dir = Path(env_vars.data_dir)
            progress_bar.progress(10)
            status_log.markdown(f"Extracted {len(list(session_frames_directory.glob('*.png')))} frames to {session_frames_directory}")
            logger.info(f"Extracted {len(list(session_frames_directory.glob('*.png')))} frames to {session_frames_directory}")

            #Read captions
            logger.info("Getting the subtitle file...")
            session_subtitle_file = video_object.save_captions()
            status_log.markdown(session_subtitle_file)
            progress_bar.progress(15)
            status_log.markdown(f"Fetched the subtitle file... {session_subtitle_file}")
            logger.info(f"Fetched the subtitle file... {session_subtitle_file}")

            #Create Index
            indexer = VideoIndexer(env_vars.embed_model, env_vars.indexing_path)
            index = indexer.get_multimodal_index(video_metadata["filename_without_extension"])
            if index is None:
                logger.info("Creating multimodal index...")
                index = indexer.create_multimodal_index(env_vars.qdrant_host, env_vars.qdrant_port,
                                                    video_metadata["filename_without_extension"],
                                                    session_frames_directory, session_subtitle_file)
                logger.info("Index Created !!!")
            else:
                logger.info("Index Loaded !!!")

            progress_bar.progress(90)

            st.session_state.index = index
            st.session_state.video_file = video_file
            st.session_state.subtitle_file = session_subtitle_file
            st.session_state.video_id = video_metadata["filename_without_extension"]
            st.session_state.retriever = VideoRetriever(index)
            status_log.markdown("Index creation complete")
            progress_bar.progress(100)
            st.success("✅ Index creatied successfully ✅")

        # Query Section
   
    if "index" in st.session_state and st.session_state.index is not None:
        st.header("Step 2: Query Video Content 🔍")
        if st.session_state.video_file:
            st.video(st.session_state.video_file)

        query = st.text_input("Enter your query:")
        if st.button("Enter you Query: "):
            logger.info(f"Processing query: {query}")
            try:
                processing_container = st.container()
                with processing_container:
                    st.markdown("Query Processing Logs: ")
                    query_status_log = st.empty()
                    query_progress = st.progress(0)

                with st.spinner("Analyzing query..."):
                    query_status_log.markdown("Starting query processing...")
                    query_progress.progress(20)

                    query_status_log.markdown("Searching for relevant content...")
                    retrieved_images, retrieved_texts = (st.session_state.retriever.retrieve(query))
                    query_progress.progress(40)

                    query_status_log.markdown(
                        f"Found {len(retrieved_images)} relevant frames and {len(retrieved_texts)} text segments"
                    )

                    query_status_log.markdown("Generating response with Gemini...")
                    response = st.session_state.gemini_inference.process_query(
                        retrieved_images, retrieved_texts, query
                    )
                    query_progress.progress(80)

                    st.subheader("Answer 💡")
                    st.markdown(f"**{response['answer']}**")

                    st.subheader("Retrieved Frames 🖼️")
                    num_cols = min(3, len(retrieved_images))
                    cols = st.columns(num_cols)
                    for idx, image_path in enumerate(retrieved_images):
                        with cols[idx % num_cols]:
                            st.image(str(image_path), use_container_width=True)
                            st.caption(f"Frame {idx + 1}")

                    query_progress.progress(100)
                    logger.info("Query processed !")
                    query_status_log.markdown("Query processed !")
                
            except Exception as e:
                logger.error(f"Error processing query: {str(e)}", exc_info=True)
                st.error(f"❌Error processing query❌: {str(e)}")

        else:
            logger.info("NONO")