# NoBinge

NoBinge is a Streamlit-based prototype application that utilizes multimodal indexing to query videos through transcripts. The application leverages advanced machine learning models to process, index, and retrieve video content efficiently.

## Features

- **Video Processing**: Extract metadata and process video files using `ffmpeg` and `moviepy`.
- **Multimodal Indexing**: Index video content using `llama_index` and `qdrant_client` for efficient querying.
- **Video Retrieval**: Retrieve video content based on transcript queries with high accuracy.
- **Streamlit Interface**: User-friendly interface for interacting with the application.

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/3l-d1abl0/NoBinge.git
   ```
2. Navigate to the project directory:
   ```bash
   cd NoBinge/app
   ```
3. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

To run the application, execute the following command in the terminal:
```bash
streamlit run app/streamlit_app.py --server.headless true
```

## Configuration

- Check envs/env.sample to be aware of the environment variables required.
- Ensure you have set the `GEMINI_API_KEY` in your environment variables. The application will not run without it.
- Modify the `config.py` file to adjust settings such as embedding models and indexing paths.

## File Structure

- `streamlit_app.py`: Main entry point for the Streamlit application.
- `video_indexer.py`: Handles the indexing of video content.
- `video_processor.py`: Processes video files and extracts metadata.
- `video_retriever.py`: Retrieves video content based on queries.
- `config.py`: Configuration settings for the application.
- `gemini.py`: Integrates Gemini inference for additional processing.

## Contributing

Contributions are welcome! Please fork the repository and submit a pull request for any improvements or bug fixes.

