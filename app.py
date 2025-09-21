"""
FastAPI server for handling audio and video file uploads.
This server provides endpoints for processing media files and health checks.
"""

import os
import tempfile
from typing import Dict, Any
from fastapi import FastAPI, File, UploadFile, HTTPException, status, Request
from fastapi.responses import JSONResponse, HTMLResponse
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
    """Save uploaded file to the data folder and return the path."""
    try:
        # Create data/uploads directory if it doesn't exist
        data_dir = os.path.join("data", "uploads")
        os.makedirs(data_dir, exist_ok=True)
        
        # Generate a unique filename with timestamp to avoid conflicts
        import time
        timestamp = int(time.time() * 1000)  # milliseconds
        filename = f"{timestamp}_{file.filename}"
        file_path = os.path.join(data_dir, filename)
        
        # Save file to data folder
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
            
        return file_path
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error saving file: {str(e)}"
        )

@app.get("/", response_class=HTMLResponse)
async def upload_interface():
    """
    Serve a minimal HTML interface for file uploads at the base route.
    
    Returns:
        HTMLResponse: Simple HTML form for file uploads
    """
    html_content = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Inference Server - File Upload</title>
        <style>
            body { font-family: Arial, sans-serif; margin: 40px; background-color: #f5f5f5; }
            .container { max-width: 600px; margin: 0 auto; background: white; padding: 30px; border-radius: 8px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }
            h1 { color: #333; text-align: center; margin-bottom: 30px; }
            .upload-section { margin: 20px 0; padding: 20px; border: 2px dashed #ddd; border-radius: 8px; text-align: center; }
            .upload-section:hover { border-color: #007bff; background-color: #f8f9fa; }
            input[type="file"] { margin: 10px 0; padding: 10px; border: 1px solid #ddd; border-radius: 4px; width: 100%; }
            button { background-color: #007bff; color: white; padding: 12px 30px; border: none; border-radius: 4px; cursor: pointer; margin: 5px; }
            button:hover { background-color: #0056b3; }
            .info { margin-top: 20px; padding: 15px; background-color: #e9ecef; border-radius: 4px; }
            .result { margin-top: 20px; padding: 15px; border-radius: 4px; white-space: pre-wrap; }
            .success { background-color: #d4edda; border: 1px solid #c3e6cb; color: #155724; }
            .error { background-color: #f8d7da; border: 1px solid #f5c6cb; color: #721c24; }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🎬 Inference Server - File Analysis</h1>
            
            <div class="upload-section">
                <h3>📹 Upload Video File</h3>
                <form id="videoForm" enctype="multipart/form-data">
                    <input type="file" id="videoFile" name="file" accept="video/*" required>
                    <br>
                    <button type="submit">Analyze Video</button>
                </form>
            </div>
            
            <div class="upload-section">
                <h3>🎵 Upload Audio File</h3>
                <form id="audioForm" enctype="multipart/form-data">
                    <input type="file" id="audioFile" name="file" accept="audio/*" required>
                    <br>
                    <button type="submit">Analyze Audio</button>
                </form>
            </div>
            
            <div class="info">
                <strong>ℹ️ Information:</strong><br>
                • Supported video formats: MP4, AVI, MOV, WMV, FLV, WebM, MKV, M4V<br>
                • Supported audio formats: MP3, WAV, FLAC, AAC, OGG, M4A, WMA<br>
                • Max video size: 500MB | Max audio size: 100MB<br>
                • Files are analyzed using FFmpeg and OpenCV for metadata extraction
            </div>
            
            <div id="result"></div>
        </div>

        <script>
            async function uploadFile(formId, endpoint) {
                const form = document.getElementById(formId);
                const formData = new FormData(form);
                const resultDiv = document.getElementById('result');
                
                resultDiv.innerHTML = '<div class="result">⏳ Processing file...</div>';
                
                try {
                    const response = await fetch(endpoint, {
                        method: 'POST',
                        body: formData
                    });
                    
                    const result = await response.json();
                    
                    if (response.ok) {
                        resultDiv.innerHTML = `<div class="result success"><strong>✅ Analysis Complete!</strong><br><br>${JSON.stringify(result, null, 2)}</div>`;
                    } else {
                        resultDiv.innerHTML = `<div class="result error"><strong>❌ Error:</strong><br><br>${JSON.stringify(result, null, 2)}</div>`;
                    }
                } catch (error) {
                    resultDiv.innerHTML = `<div class="result error"><strong>❌ Network Error:</strong><br><br>${error.message}</div>`;
                }
            }
            
            document.getElementById('videoForm').addEventListener('submit', function(e) {
                e.preventDefault();
                uploadFile('videoForm', '/upload-video');
            });
            
            document.getElementById('audioForm').addEventListener('submit', function(e) {
                e.preventDefault();
                uploadFile('audioForm', '/upload-audio');
            });
        </script>
    </body>
    </html>
    """
    return HTMLResponse(content=html_content)

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
        # Save file to data folder
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
    # Note: Files are now saved persistently in data/uploads folder

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
        # Save file to data folder
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
    # Note: Files are now saved persistently in data/uploads folder

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