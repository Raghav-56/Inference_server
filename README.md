# Inference_server
Server for Inference script - A FastAPI server for processing audio and video files

## Features
- **Audio Processing**: Upload and process audio files (MP3, WAV, FLAC, AAC, OGG, M4A, WMA)
- **Video Processing**: Upload and process video files (MP4, AVI, MOV, WMV, FLV, WebM, MKV, M4V)
- **Health Check**: Simple endpoint to verify server status
- **JSON Responses**: All endpoints return structured JSON responses
- **File Validation**: Automatic file type and size validation
- **Web Interface**: User-friendly file upload interface at base route (/)
- **FFmpeg Analysis**: Real-time metadata extraction using FFmpeg
- **Custom Response Override**: Optional feature to return custom JSON responses
- **Extensible**: Ready for AI model integration

## Installation

1. Clone the repository:
```bash
git clone https://github.com/Raghav-56/Inference_server.git
cd Inference_server
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

### Start the server:
```bash
python3 app.py
```

The server will start on `http://localhost:8000`

### Web Interface
Visit `http://localhost:8000` for a user-friendly file upload interface with drag-and-drop functionality and real-time analysis results.

### API Documentation
Once the server is running, you can access:
- **Interactive API docs**: `http://localhost:8000/docs`
- **ReDoc documentation**: `http://localhost:8000/redoc`
- **OpenAPI JSON**: `http://localhost:8000/openapi.json`

## API Endpoints

### 1. Health Check
```http
GET /health
```
**Response:**
```json
{
  "status": "healthy",
  "message": "Inference server is running and ready to process files",
  "service": "inference-server"
}
```

### 2. Upload Audio File
```http
POST /upload-audio
```
**Request:** Multipart form data with audio file
**Supported formats:** MP3, WAV, FLAC, AAC, OGG, M4A, WMA
**Max file size:** 100MB

**Response:**
```json
{
  "status": "success",
  "filename": "audio.mp3",
  "file_size_bytes": 1024,
  "processing_status": "completed",
  "content_type": "audio",
  "analysis": {
    "duration": "placeholder - to be calculated",
    "sample_rate": "placeholder - to be detected",
    "format": "placeholder - to be identified"
  },
  "message": "Audio processed successfully."
}
```

### 3. Upload Video File
```http
POST /upload-video
```
**Request:** Multipart form data with video file
**Supported formats:** MP4, AVI, MOV, WMV, FLV, WebM, MKV, M4V
**Max file size:** 500MB

**Response:**
```json
{
  "status": "success",
  "filename": "video.mp4",
  "file_size_bytes": 2048,
  "processing_status": "completed",
  "content_type": "video",
  "analysis": {
    "duration": "placeholder - to be calculated",
    "resolution": "placeholder - to be detected",
    "classification": "placeholder - AI model will classify later"
  },
  "message": "Video processed successfully. AI classification pending implementation."
}
```

## Example Usage with curl

### Health Check:
```bash
curl -X GET "http://localhost:8000/health"
```

### Upload Audio:
```bash
curl -X POST "http://localhost:8000/upload-audio" \
  -H "Content-Type: multipart/form-data" \
  -F "file=@path/to/audio.mp3;type=audio/mp3"
```

### Upload Video:
```bash
curl -X POST "http://localhost:8000/upload-video" \
  -H "Content-Type: multipart/form-data" \
  -F "file=@path/to/video.mp4;type=video/mp4"
```

## File Structure

```
Inference_server/
├── app.py                    # Main FastAPI application
├── main.py                   # Processing logic for audio/video files
├── custom_response.json      # Custom JSON response template (editable)
├── analysis/                 # Analysis modules
│   ├── __init__.py          # Package initialization
│   ├── video_analyzer.py    # Video analysis using FFmpeg
│   └── audio_analyzer.py    # Audio analysis using FFmpeg
├── requirements.txt          # Python dependencies
├── run.sh                   # Convenience startup script
└── README.md                # This file
```

## Processing Logic

The server uses the `main.py` file for processing uploaded files. Currently, it includes:

### Real Analysis with FFmpeg
- **Video Analysis**: Extracts duration, resolution, FPS, codec, format, bitrate, and aspect ratio
- **Audio Analysis**: Extracts duration, sample rate, channels, codec, format, bitrate, and channel layout
- **Metadata Extraction**: Uses FFmpeg to analyze actual file properties
- **Error Handling**: Graceful handling of unsupported or corrupted files

### Custom Response Override
A special feature allows you to override the default analysis with custom JSON responses:

1. **Enable Override**: Set `ENABLE_CUSTOM_RESPONSE = True` in `main.py`
2. **Edit Response**: Modify `custom_response.json` with your desired response
3. **Dynamic Filename**: The filename will automatically update to match the uploaded file
4. **Use Cases**: Testing, demos, or returning predetermined responses

**Example custom response:**
```json
{
  "status": "success",
  "filename": "will_be_updated_automatically.mp4",
  "content_type": "custom",
  "analysis": {
    "your_custom_field": "your_custom_value"
  },
  "message": "Your custom message here"
}
```

This module is designed to be extended with:
- AI model integration for video classification
- Advanced audio analysis capabilities
- Machine learning inference pipelines

## Development

### Adding AI Models
To integrate AI models for classification:

1. Install additional dependencies (e.g., torch, tensorflow, opencv-python)
2. Update `main.py` with model loading and inference logic
3. Modify the response structure in `app.py` as needed

### Error Handling
The server includes comprehensive error handling for:
- Unsupported file types
- File size limits
- Processing errors
- Invalid requests

## Future Enhancements

- [ ] AI model integration for video classification
- [ ] Audio analysis and transcription
- [ ] Batch processing capabilities
- [ ] Database integration for storing results
- [ ] Authentication and authorization
- [ ] Rate limiting and caching
