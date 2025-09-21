"""
Main processing module for video and audio files.
This module contains the logic for processing uploaded files using analysis modules.
"""

import json
import os
from typing import Dict, Any
from analysis import VideoAnalyzer, AudioAnalyzer

# Configuration for custom response override
# Set this to True to enable custom JSON response override
ENABLE_CUSTOM_RESPONSE = False

# Path to the custom response JSON file
CUSTOM_RESPONSE_FILE = "custom_response.json"


def load_custom_response(filename: str) -> Dict[str, Any]:
    """
    Load custom response from JSON file if override is enabled.
    
    Args:
        filename (str): Original filename to include in the response
        
    Returns:
        Dict[str, Any]: Custom response data with filename updated
    """
    try:
        if not ENABLE_CUSTOM_RESPONSE:
            return None
            
        if not os.path.exists(CUSTOM_RESPONSE_FILE):
            print(f"Warning: Custom response file '{CUSTOM_RESPONSE_FILE}' not found")
            return None
            
        with open(CUSTOM_RESPONSE_FILE, 'r') as f:
            custom_data = json.load(f)
            
        # Update the filename in the custom response
        custom_data["filename"] = filename
        
        return custom_data
        
    except Exception as e:
        print(f"Error loading custom response: {str(e)}")
        return None


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
        If ENABLE_CUSTOM_RESPONSE is True, returns custom JSON response instead.
    """
    # Check if custom response override is enabled
    custom_response = load_custom_response(filename)
    if custom_response is not None:
        return custom_response
    
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
        If ENABLE_CUSTOM_RESPONSE is True, returns custom JSON response instead.
    """
    # Check if custom response override is enabled
    custom_response = load_custom_response(filename)
    if custom_response is not None:
        return custom_response
    
    # Use the AudioAnalyzer from the analysis module
    results = AudioAnalyzer.analyze_audio(file_path, filename)
    
    # Add a note about future AI model integration
    if results.get("status") == "success":
        results["message"] += " AI model classification can be integrated here later."
    
    return results