from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from app.api.routes import router
import os

app = FastAPI(
    title="AI Career Coach API",
    version="1.0.0"
)

app.include_router(router)

# Get the absolute path to the frontend directory
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
FRONTEND_DIR = os.path.join(BASE_DIR, "frontend")

@app.get("/")
async def serve_frontend():
    return FileResponse(os.path.join(FRONTEND_DIR, "index.html"))

# Mount the frontend directory to serve other static files (CSS, JS) from the root
app.mount("/", StaticFiles(directory=FRONTEND_DIR), name="frontend")