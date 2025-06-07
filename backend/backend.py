from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, FileResponse
from fastapi import UploadFile, File, HTTPException
from pydantic import BaseModel
import base64
import os
from fastapi.staticfiles import StaticFiles

app = FastAPI()

# Allow CORS for local frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Serve static files for Pages
app.mount("/Pages", StaticFiles(directory="Pages"), name="pages")

@app.get("/api/ping")
def ping():
    return JSONResponse(content={"message": "pong"})

SUPPORTED_FORMATS = {"mp3", "wav"}

class AudioProcessRequest(BaseModel):
    language: str
    audio_base64: str

class AudioProcessResponse(BaseModel):
    result_audio_base64: str
    message: str

@app.post("/api/process-audio", response_model=AudioProcessResponse)
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

@app.get("/loading")
def loading_page():
    return FileResponse("Pages/loading.html")

@app.get("/result")
def result_page():
    return FileResponse("Pages/result.html")