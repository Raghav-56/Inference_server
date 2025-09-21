"""
FastAPI server for handling audio and video file uploads.
This server provides endpoints for processing media files and health checks.
"""

import os
import tempfile
from typing import Dict, Any
from fastapi import FastAPI, File, UploadFile, HTTPException, status
from fastapi.responses import JSONResponse
from pydantic import BaseModel
import shutil

# Import processing functions from main.py
from main import process_video, process_audio

# Create FastAPI app instance
app = FastAPI(
    title="Inference Server",
    description="A server for processing audio and video files with AI inference capabilities",
    version="1.0.0"
)

# Response models
class HealthResponse(BaseModel):
    status: str
    message: str
    service: str

class ProcessingResponse(BaseModel):
    status: str
    filename: str
    file_size_bytes: int
    processing_status: str
    content_type: str
    analysis: Dict[str, Any]
    message: str

# Supported file types
SUPPORTED_VIDEO_TYPES = {
    "video/mp4", "video/avi", "video/mov", "video/wmv", "video/flv", 
    "video/webm", "video/mkv", "video/m4v"
}

SUPPORTED_AUDIO_TYPES = {
    "audio/mp3", "audio/wav", "audio/flac", "audio/aac", "audio/ogg", 
    "audio/m4a", "audio/wma", "audio/mpeg"
}

def validate_file_type(file: UploadFile, supported_types: set) -> bool:
    """Validate if the uploaded file type is supported."""
    return file.content_type in supported_types

def save_uploaded_file(file: UploadFile) -> str:
    """Save uploaded file to a temporary location and return the path."""
    try:
        # Create a temporary file
        with tempfile.NamedTemporaryFile(delete=False, suffix=f"_{file.filename}") as temp_file:
            # Copy file content to temporary file
            shutil.copyfileobj(file.file, temp_file)
            return temp_file.name
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error saving file: {str(e)}"
        )

@app.get("/health", response_model=HealthResponse)
async def health_check() -> HealthResponse:
    """
    Health check endpoint to verify server is running.
    
    Returns:
        HealthResponse: Status information about the server
    """
    return HealthResponse(
        status="healthy",
        message="Inference server is running and ready to process files",
        service="inference-server"
    )

@app.post("/upload-audio", response_model=ProcessingResponse)
async def upload_audio(file: UploadFile = File(...)) -> ProcessingResponse:
    """
    Upload and process an audio file.
    
    Args:
        file (UploadFile): The audio file to process
        
    Returns:
        ProcessingResponse: Processing results and analysis
        
    Raises:
        HTTPException: If file type is not supported or processing fails
    """
    # Validate file type
    if not validate_file_type(file, SUPPORTED_AUDIO_TYPES):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Unsupported audio file type: {file.content_type}. "
                   f"Supported types: {', '.join(SUPPORTED_AUDIO_TYPES)}"
        )
    
    # Validate file size (limit to 100MB for audio)
    file.file.seek(0, 2)  # Seek to end
    file_size = file.file.tell()
    file.file.seek(0)  # Seek back to beginning
    
    if file_size > 100 * 1024 * 1024:  # 100MB limit
        raise HTTPException(
            status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
            detail="Audio file too large. Maximum size is 100MB."
        )
    
    temp_file_path = None
    try:
        # Save file temporarily
        temp_file_path = save_uploaded_file(file)
        
        # Process the audio file
        results = process_audio(temp_file_path, file.filename)
        
        return ProcessingResponse(**results)
        
    except HTTPException:
        # Re-raise HTTP exceptions
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error processing audio file: {str(e)}"
        )
    finally:
        # Clean up temporary file
        if temp_file_path and os.path.exists(temp_file_path):
            try:
                os.unlink(temp_file_path)
            except Exception:
                pass  # Ignore cleanup errors

@app.post("/upload-video", response_model=ProcessingResponse)
async def upload_video(file: UploadFile = File(...)) -> ProcessingResponse:
    """
    Upload and process a video file.
    
    Args:
        file (UploadFile): The video file to process
        
    Returns:
        ProcessingResponse: Processing results and analysis
        
    Raises:
        HTTPException: If file type is not supported or processing fails
    """
    # Validate file type
    if not validate_file_type(file, SUPPORTED_VIDEO_TYPES):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Unsupported video file type: {file.content_type}. "
                   f"Supported types: {', '.join(SUPPORTED_VIDEO_TYPES)}"
        )
    
    # Validate file size (limit to 500MB for video)
    file.file.seek(0, 2)  # Seek to end
    file_size = file.file.tell()
    file.file.seek(0)  # Seek back to beginning
    
    if file_size > 500 * 1024 * 1024:  # 500MB limit
        raise HTTPException(
            status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
            detail="Video file too large. Maximum size is 500MB."
        )
    
    temp_file_path = None
    try:
        # Save file temporarily
        temp_file_path = save_uploaded_file(file)
        
        # Process the video file using main.py
        results = process_video(temp_file_path, file.filename)
        
        return ProcessingResponse(**results)
        
    except HTTPException:
        # Re-raise HTTP exceptions
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error processing video file: {str(e)}"
        )
    finally:
        # Clean up temporary file
        if temp_file_path and os.path.exists(temp_file_path):
            try:
                os.unlink(temp_file_path)
            except Exception:
                pass  # Ignore cleanup errors

# Error handler for large files
@app.exception_handler(413)
async def request_entity_too_large_handler(request, exc):
    return JSONResponse(
        status_code=413,
        content={"detail": "File too large"}
    )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)