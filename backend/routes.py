from fastapi import APIRouter, HTTPException
from schemas import AudioProcessRequest, AudioProcessResponse
from fastapi.responses import FileResponse
from audio_processing import process_audio_with_censorship
import base64
import os

SUPPORTED_FORMATS = {"mp3", "wav"}

router = APIRouter()

@router.post("/api/process-audio", response_model=AudioProcessResponse)
def process_audio(data: AudioProcessRequest):
    if data.language not in ["Russian", "English"]:
        raise HTTPException(status_code=400, detail="Unsupported language")

    try:
        censored_base64 = process_audio_with_censorship(data.audio_base64, data.language)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Audio processing failed: {str(e)}")

    return AudioProcessResponse(
        result_audio_base64=censored_base64,
        message="Audio processed successfully."
    )


@router.get("/loading")
def loading_page():
    pages_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "Pages"))
    return FileResponse(os.path.join(pages_dir, "loading.html"))

@router.get("/result")
def result_page():
    pages_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "Pages"))
    return FileResponse(os.path.join(pages_dir, "result.html"))
