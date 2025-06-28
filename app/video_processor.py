import ffmpeg
from logger import logger
import os
from config import get_envs, Settings
import shutil
from pathlib import Path
from moviepy.video.io.VideoFileClip import VideoFileClip

class VideoProcessor:

    def __init__(self, file_path: str, subtitle_path: str):
        self.file: str = file_path
        self.subtitle: str = subtitle_path
        self.logger = logger

    def get_metadata(self):

        try:
            # Get video metadata using ffmpeg.probe()
            probe = ffmpeg.probe(self.file)
            
            # Extract specific metadata
            metadata = {
                "title": probe.get('format', {}).get('tags', {}).get('title', 'Unknown Title'),
                "filename": os.path.basename(self.file),
                "filename_without_extension": os.path.splitext(os.path.basename(self.file))[0],
                "duration": float(probe['format']['duration']),
                "filesize_mb": round(float(probe['format']['size']) / (1024 * 1024), 2),
                "format": probe['format']['format_name'],
                "resolution": f"{probe['streams'][1]['width']}x{probe['streams'][1]['height']}"
            }
            
            return metadata
    
        except Exception as e:
            self.logger.info(f"Error while Fetching MetaData: {e}")
            return None
        

    def save_captions(self)->None:
        try:
            env_vars: Settings = get_envs()
            subtitle_filename = os.path.basename(self.subtitle)
            shutil.copy(self.subtitle, env_vars.data_dir)
            self.subtitle = env_vars.data_dir+"/"+subtitle_filename
            self.logger.info(f"New Subtitle Path: {self.subtitle}")
            return self.subtitle
        except Exception as e:
            self.logger.info(f"Error: {e}")
            return None

    

    def extract_frames(self) :
        env_vars: Settings = get_envs()
        output_dir = Path(env_vars.data_dir)
        output_dir.mkdir(parents=True, exist_ok=True)

        try:
            self.logger.info(f"Extracting frames from video: {self.file}")
            with VideoFileClip(str(self.file)) as clip:
                fps = 1 / env_vars.frame_interval
                clip.write_images_sequence(str(output_dir / "frame%04d.png"), fps=fps, logger="bar")
            self.logger.info(f"OUTPUT_DIR:{output_dir}")
            return output_dir
        except Exception as e:
            self.logger.error(f"Failed to extract frames: {str(e)}")
            raise