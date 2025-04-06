import ffmpeg
from logger import logger
import os

class VideoProcessor:

    def __init__(self, file_path: str):
        self.file = file_path
        self.logger = logger

    def get_metadata(self):

        try:
            # Get video metadata using ffmpeg.probe()
            probe = ffmpeg.probe(self.file)
            
            # Extract specific metadata
            metadata = {
                "title": probe.get('format', {}).get('tags', {}).get('title', 'Unknown Title'),
                "filename": os.path.basename(self.file),
                "duration": float(probe['format']['duration']),
                "filesize_mb": round(float(probe['format']['size']) / (1024 * 1024), 2),
                "format": probe['format']['format_name'],
                "resolution": f"{probe['streams'][1]['width']}x{probe['streams'][1]['height']}"
            }
            
            return metadata
    
        except Exception as e:
            self.logger.info(f"Error: {e}")
            return None