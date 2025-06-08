from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import JSONResponse
from routes import router as audio_router
import os

app = FastAPI()

# Allow CORS for local frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # В продакшене замените на конкретные домены
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Serve static files for Pages and CSS
pages_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "Pages"))
css_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "css"))
app.mount("/Pages", StaticFiles(directory=pages_dir), name="pages")
app.mount("/css", StaticFiles(directory=css_dir), name="css")

# API routes and page routes
app.include_router(audio_router)

@app.get("/api/ping")
def ping():
    return JSONResponse(content={"message": "pong"})
@app.get("/")
def read_root():
    return {"Hello": "World"}