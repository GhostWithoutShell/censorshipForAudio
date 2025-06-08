import base64
import io
import re
import tempfile
from typing import List
from faster_whisper import WhisperModel
from pydub import AudioSegment
from pydub.generators import Sine

BAD_WORDS = {
    "English": ["fuck", "shit", "bitch", "asshole"],
    "Russian": ["блять", "сука", "хуй", "пизда"]
}

model = WhisperModel("base", device="cpu", compute_type="int8")

def decode_audio(audio_base64: str) -> AudioSegment:
    audio_data = base64.b64decode(audio_base64.split(",")[-1])
    return AudioSegment.from_file(io.BytesIO(audio_data))

def encode_audio(audio: AudioSegment) -> str:
    buffer = io.BytesIO()
    audio.export(buffer, format="wav")
    return "data:audio/wav;base64," + base64.b64encode(buffer.getvalue()).decode("utf-8")

def generate_beep(duration_ms: int, sample_rate=16000) -> AudioSegment:
    return Sine(1000, sample_rate=sample_rate).to_audio_segment(duration=duration_ms).apply_gain(+5)

def match_bad_words(text: str, lang: str):
    words = BAD_WORDS.get(lang, [])
    if not words:
        return None
    pattern = r"\b(" + "|".join(map(re.escape, words)) + r")\b"
    return re.compile(pattern, re.IGNORECASE)

def censor_audio(audio: AudioSegment, segments, bad_word_regex) -> AudioSegment:
    censored = audio[:]
    for segment in segments:
        for match in bad_word_regex.finditer(segment.text):
            start_ms = int(segment.start * 1000)
            end_ms = int(segment.end * 1000)
            duration_ms = end_ms - start_ms
            beep = generate_beep(duration_ms)
            censored = censored.overlay(beep, position=start_ms)
    return censored

def process_audio_with_censorship(audio_base64: str, language: str) -> str:
    audio = decode_audio(audio_base64)
    audio = audio.set_frame_rate(16000).set_channels(1)

    with tempfile.NamedTemporaryFile(suffix=".wav", delete=True) as tmpfile:
        audio.export(tmpfile.name, format="wav")

        if audio.duration_seconds > 30:
            segments = []
            for segment in model.transcribe(tmpfile.name, language=language, vad_filter=True)[0]:
                segments.append(segment)
        else:
            segments, _ = model.transcribe(tmpfile.name, language=language)

    full_text = " ".join([seg.text for seg in segments])
    regex = match_bad_words(full_text, language)
    if not regex:
        return encode_audio(audio)

    censored = censor_audio(audio, segments, regex)
    return encode_audio(censored)