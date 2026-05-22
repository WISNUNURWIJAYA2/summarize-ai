from fastapi import APIRouter

router = APIRouter(
    prefix="/summaries",
    tags=["Summaries"]
)

@router.get("/")
def get_summaries():
    return {
        "message": "summaries endpoint"
    }