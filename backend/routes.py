from fastapi import APIRouter, HTTPException
from .schemas import AudioProcessRequest, AudioProcessResponse
from fastapi.responses import FileResponse
import base64
import os

SUPPORTED_FORMATS = {"mp3", "wav"}

router = APIRouter()

@router.post("/api/process-audio", response_model=AudioProcessResponse)
def process_audio(data: AudioProcessRequest):
    # Validate language
    if data.language not in ["Russian", "English"]:
        raise HTTPException(status_code=400, detail="Unsupported language")
    # Validate audio format from base64 header
    header = data.audio_base64.split(",")[0] if "," in data.audio_base64 else ""
    if "mp3" in header:
        ext = "mp3"
    elif "wav" in header:
        ext = "wav"
    else:
        ext = None
    if ext not in SUPPORTED_FORMATS:
        raise HTTPException(status_code=400, detail="Unsupported audio format. Only mp3 and wav are allowed.")
    # Decode and process audio (placeholder logic)
    try:
        audio_bytes = base64.b64decode(data.audio_base64.split(",")[-1])
        # Here you would call your actual audio processing logic/script
        # For now, just return the same audio as a placeholder
        result_audio_base64 = data.audio_base64
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Audio processing failed: {str(e)}")
    return AudioProcessResponse(result_audio_base64=result_audio_base64, message="Audio processed successfully.")

@router.get("/loading")
def loading_page():
    pages_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "Pages"))
    return FileResponse(os.path.join(pages_dir, "loading.html"))

@router.get("/result")
def result_page():
    pages_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "Pages"))
    return FileResponse(os.path.join(pages_dir, "result.html"))
