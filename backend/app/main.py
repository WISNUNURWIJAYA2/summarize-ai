from fastapi import FastAPI

from app.api.routes.health import router as health_router
from app.api.routes.documents import router as documents_router
from app.api.routes.summaries import router as summaries_router
from app.utils.file_utils import create_upload_dir

create_upload_dir()

app = FastAPI(
    title="AI Workflow API",
    version="1.0.0"
)

from fastapi.middleware.cors import CORSMiddleware
app = FastAPI()

# Izinkan origin dari Live Server frontend Anda
origins = [
    "http://127.0.0.1:5500",
    "http://localhost:5500",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health_router)
app.include_router(documents_router)
app.include_router(summaries_router)


@app.get("/")
def root():
    return {"message": "Backend running"}