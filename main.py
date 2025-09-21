"""
Main processing module for video and audio files.
This module contains the logic for processing uploaded files using analysis modules.
"""

from typing import Dict, Any
from analysis import VideoAnalyzer, AudioAnalyzer


def process_video(file_path: str, filename: str) -> Dict[str, Any]:
    """
    Process a video file and return analysis results.
    
    Args:
        file_path (str): Path to the uploaded video file
        filename (str): Original filename of the uploaded file
    
    Returns:
        Dict[str, Any]: Processing results as a dictionary
        
    Note:
        Uses VideoAnalyzer for actual video analysis with OpenCV and FFmpeg.
        AI model integration can be added here later.
    """
    # Use the VideoAnalyzer from the analysis module
    results = VideoAnalyzer.analyze_video(file_path, filename)
    
    # Add a note about future AI model integration
    if results.get("status") == "success":
        results["message"] += " AI model classification can be integrated here later."
    
    return results


def process_audio(file_path: str, filename: str) -> Dict[str, Any]:
    """
    Process an audio file and return analysis results.
    
    Args:
        file_path (str): Path to the uploaded audio file
        filename (str): Original filename of the uploaded file
    
    Returns:
        Dict[str, Any]: Processing results as a dictionary
        
    Note:
        Uses AudioAnalyzer for actual audio analysis with FFmpeg.
        AI model integration can be added here later.
    """
    # Use the AudioAnalyzer from the analysis module
    results = AudioAnalyzer.analyze_audio(file_path, filename)
    
    # Add a note about future AI model integration
    if results.get("status") == "success":
        results["message"] += " AI model classification can be integrated here later."
    
    return results