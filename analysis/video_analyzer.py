"""
Video analysis module using FFmpeg.
Provides functionality to extract video metadata and analyze video files.
"""

import ffmpeg
import os
from typing import Dict, Any


class VideoAnalyzer:
    """Analyzer for video files using FFmpeg."""
    
    @staticmethod
    def analyze_video(file_path: str, filename: str) -> Dict[str, Any]:
        """
        Analyze a video file and extract metadata.
        
        Args:
            file_path (str): Path to the video file
            filename (str): Original filename
            
        Returns:
            Dict[str, Any]: Analysis results including metadata
        """
        try:
            # Basic file info
            file_size = os.path.getsize(file_path) if os.path.exists(file_path) else 0
            
            # Use FFmpeg to get detailed metadata
            ffmpeg_info = VideoAnalyzer._analyze_with_ffmpeg(file_path)
            
            # Build analysis result
            analysis_result = {
                "status": "success",
                "filename": filename,
                "file_size_bytes": file_size,
                "processing_status": "completed",
                "content_type": "video",
                "analysis": {
                    "duration_seconds": ffmpeg_info.get("duration", 0),
                    "resolution": f"{ffmpeg_info.get('width', 0)}x{ffmpeg_info.get('height', 0)}",
                    "fps": ffmpeg_info.get("fps", 0),
                    "codec": ffmpeg_info.get("codec", "unknown"),
                    "format": ffmpeg_info.get("format", "unknown"),
                    "bitrate": ffmpeg_info.get("bitrate", "unknown"),
                    "aspect_ratio": ffmpeg_info.get("aspect_ratio", "unknown")
                },
                "message": "Video analysis completed successfully using FFmpeg."
            }
            
            return analysis_result
            
        except Exception as e:
            return {
                "status": "error",
                "filename": filename,
                "file_size_bytes": file_size if 'file_size' in locals() else 0,
                "processing_status": "failed",
                "content_type": "video",
                "analysis": {},
                "message": f"Video analysis failed: {str(e)}"
            }
    
    @staticmethod
    def _analyze_with_ffmpeg(file_path: str) -> Dict[str, Any]:
        """Extract video metadata using FFmpeg."""
        try:
            # Get video information using ffmpeg-python
            probe = ffmpeg.probe(file_path)
            
            # Extract video stream information
            video_stream = next((stream for stream in probe['streams'] 
                               if stream['codec_type'] == 'video'), None)
            
            if not video_stream:
                return {"error": "No video stream found"}
            
            duration = float(probe.get('format', {}).get('duration', 0))
            bitrate = probe.get('format', {}).get('bit_rate', 'unknown')
            format_name = probe.get('format', {}).get('format_name', 'unknown')
            codec = video_stream.get('codec_name', 'unknown')
            
            # Extract width/height from video stream
            width = video_stream.get('width', 0)
            height = video_stream.get('height', 0)
            
            # Calculate FPS from r_frame_rate
            fps = 0
            try:
                frame_rate = video_stream.get('r_frame_rate', '0/1')
                if '/' in frame_rate:
                    num, den = frame_rate.split('/')
                    fps = float(num) / float(den) if float(den) != 0 else 0
                else:
                    fps = float(frame_rate)
            except:
                fps = 0
                
            # Calculate aspect ratio
            aspect_ratio = "unknown"
            if width and height:
                ratio = width / height
                aspect_ratio = f"{ratio:.2f}:1"
            
            return {
                "duration": duration,
                "bitrate": bitrate,
                "format": format_name,
                "codec": codec,
                "width": width,
                "height": height,
                "fps": fps,
                "aspect_ratio": aspect_ratio
            }
            
        except Exception as e:
            return {"error": f"FFmpeg analysis failed: {str(e)}"}