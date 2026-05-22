from fastapi import APIRouter, UploadFile, File, HTTPException

from app.schemas.document_schema import UploadResponse
from app.schemas.parsing_schema import ParsingResponse

from app.services.file_service import save_uploaded_file
from app.services.parsing_service import parse_document

router = APIRouter(
    prefix="/documents",
    tags=["Documents"]
)


@router.post("/upload", response_model=UploadResponse)
async def upload_document(file: UploadFile = File(...)):

    try:
        result = await save_uploaded_file(file)
        return result

    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail=str(e)
        )


@router.post("/parse", response_model=ParsingResponse)
async def parse_uploaded_document(
    file: UploadFile = File(...)
):

    try:

        uploaded = await save_uploaded_file(file)

        parsed_result = await parse_document(
            uploaded["path"]
        )

        return {
            "filename": uploaded["filename"],
            "parsed_data": parsed_result
        }

    except ValueError as e:

        raise HTTPException(
            status_code=400,
            detail=str(e)
        )