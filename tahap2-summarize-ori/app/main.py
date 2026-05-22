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

app.include_router(health_router)
app.include_router(documents_router)
app.include_router(summaries_router)


@app.get("/")
def root():
    return {"message": "Backend running"}