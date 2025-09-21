"""
Audio analysis module using FFmpeg.
Provides functionality to extract audio metadata and analyze audio files.
"""

import ffmpeg
import os
from typing import Dict, Any


class AudioAnalyzer:
    """Analyzer for audio files using FFmpeg."""
    
    @staticmethod
    def analyze_audio(file_path: str, filename: str) -> Dict[str, Any]:
        """
        Analyze an audio file and extract metadata.
        
        Args:
            file_path (str): Path to the audio file
            filename (str): Original filename
            
        Returns:
            Dict[str, Any]: Analysis results including metadata
        """
        try:
            # Basic file info
            file_size = os.path.getsize(file_path) if os.path.exists(file_path) else 0
            
            # Use FFmpeg to get audio metadata
            ffmpeg_info = AudioAnalyzer._analyze_with_ffmpeg(file_path)
            
            # Build analysis result
            analysis_result = {
                "status": "success",
                "filename": filename,
                "file_size_bytes": file_size,
                "processing_status": "completed",
                "content_type": "audio",
                "analysis": {
                    "duration_seconds": ffmpeg_info.get("duration", 0),
                    "sample_rate": ffmpeg_info.get("sample_rate", "unknown"),
                    "channels": ffmpeg_info.get("channels", "unknown"),
                    "codec": ffmpeg_info.get("codec", "unknown"),
                    "format": ffmpeg_info.get("format", "unknown"),
                    "bitrate": ffmpeg_info.get("bitrate", "unknown"),
                    "channel_layout": ffmpeg_info.get("channel_layout", "unknown")
                },
                "message": "Audio analysis completed successfully using FFmpeg."
            }
            
            return analysis_result
            
        except Exception as e:
            return {
                "status": "error",
                "filename": filename,
                "file_size_bytes": file_size if 'file_size' in locals() else 0,
                "processing_status": "failed",
                "content_type": "audio",
                "analysis": {},
                "message": f"Audio analysis failed: {str(e)}"
            }
    
    @staticmethod
    def _analyze_with_ffmpeg(file_path: str) -> Dict[str, Any]:
        """Extract audio metadata using FFmpeg."""
        try:
            # Get audio information using ffmpeg-python
            probe = ffmpeg.probe(file_path)
            
            # Extract audio stream information
            audio_stream = next((stream for stream in probe['streams'] 
                               if stream['codec_type'] == 'audio'), None)
            
            if not audio_stream:
                return {"error": "No audio stream found"}
            
            # Extract format information
            format_info = probe.get('format', {})
            
            duration = float(format_info.get('duration', 0))
            bitrate = format_info.get('bit_rate', 'unknown')
            format_name = format_info.get('format_name', 'unknown')
            
            # Extract audio stream specific information
            codec = audio_stream.get('codec_name', 'unknown')
            sample_rate = audio_stream.get('sample_rate', 'unknown')
            channels = audio_stream.get('channels', 'unknown')
            channel_layout = audio_stream.get('channel_layout', 'unknown')
            
            return {
                "duration": duration,
                "bitrate": bitrate,
                "format": format_name,
                "codec": codec,
                "sample_rate": sample_rate,
                "channels": channels,
                "channel_layout": channel_layout
            }
            
        except Exception as e:
            return {"error": f"FFmpeg analysis failed: {str(e)}"}