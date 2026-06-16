from fastapi import APIRouter
from app.services.hf_model_service import summarize_text

router = APIRouter()


@router.get("/")
def get_summaries():

    text = """
    Artificial intelligence is transforming healthcare,
    education, and software development.
    Companies use AI to automate tasks and improve productivity.
    """

    summary = summarize_text(text)

    return {
        "summary": summary
    }