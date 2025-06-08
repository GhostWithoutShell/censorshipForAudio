from pydantic import BaseModel

class AudioProcessRequest(BaseModel):
    audio_base64: str
    language: str

class AudioProcessResponse(BaseModel):
    result_audio_base64: str
    message: str