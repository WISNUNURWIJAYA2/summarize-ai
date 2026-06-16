import os
import shutil

from app.schemas.document_schema import UploadResponse
from app.services.file_service import save_uploaded_file


from fastapi import APIRouter, UploadFile, File, HTTPException, Form
from app.services.hf_model_service import summarize_text
from app.services.file_parser import read_pdf, read_docx, read_txt 
from app.services.export_service import (
    create_summary_pdf
)

from fastapi.responses import FileResponse
from datetime import datetime

router = APIRouter(
    prefix="/documents",
    tags=["Documents"]
)

@router.post("/summarize")
async def summarize_document(
    file: UploadFile = File(...),
    ratio: int = Form(30)
):

    try:

        if ratio not in [30, 50, 80]:
            raise HTTPException(
                status_code=400,
                detail="Ratio must be 30, 50, or 80"
            )

        if not file.filename:
            raise HTTPException(
                status_code=400,
                detail="No file uploaded"
            )

        upload_dir = "uploads"
        os.makedirs(upload_dir, exist_ok=True)

        generated_pdf_dir = "generated/pdf"

        os.makedirs(generated_pdf_dir, exist_ok=True)

        file_path = os.path.join(
            upload_dir,
            file.filename
        )

        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(
                file.file,
                buffer
            )

        filename = file.filename.lower()

        # PARSER
        if filename.endswith(".pdf"):
            parsed_text = read_pdf(file_path)

        elif filename.endswith(".docx"):
            parsed_text = read_docx(file_path)

        elif filename.endswith(".txt"):
            parsed_text = read_txt(file_path)

        else:
            raise HTTPException(
                status_code=400,
                detail="Only PDF, DOCX, TXT are supported"
            )

        if not parsed_text:
            raise HTTPException(
                status_code=400,
                detail="Document contains no text"
            )

        # SUMMARIZE
        summary = summarize_text(
            parsed_text,
            ratio
        )

        # GENERATE FILE NAME
        timestamp = datetime.now().strftime(
            "%Y%m%d_%H%M%S"
        )

        base_name = os.path.splitext(
            file.filename
        )[0]

        pdf_filename = (
            f"{base_name}_{ratio}_{timestamp}.pdf"
        )

        pdf_path = os.path.join(
            generated_pdf_dir,
            pdf_filename
        )
       
        # SAVE PDF
        pdf_buffer = create_summary_pdf(
            filename=file.filename,
            ratio=ratio,
            summary=summary
        )

        with open(
            pdf_path,
            "wb"
        ) as f:

            f.write(
                pdf_buffer.getvalue()
            )

        return {

            "status": "success",

            "filename": file.filename,

            "ratio": ratio,

            "original_words":
                len(parsed_text.split()),

            "summary_words":
                len(summary.split()),

            "summary": summary,

            "downloads": {

                "pdf": pdf_filename
            }
        }

    except HTTPException:
        raise

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )        
        
@router.get("/download/pdf/{filename}")
async def download_pdf(
    filename: str
):

    file_path = os.path.join(
        "generated/pdf",
        filename
    )

    if not os.path.exists(
        file_path
    ):
        raise HTTPException(
            status_code=404,
            detail="PDF file not found"
        )

    return FileResponse(
        path=file_path,
        filename=filename,
        media_type="application/pdf"
    )
    
             
# tes API
        
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
    
@router.post("/parser-test") #TES PARSER
async def parser_test(
    file: UploadFile = File(...)
):

    upload_dir = "uploads"
    os.makedirs(upload_dir, exist_ok=True)

    file_path = f"{upload_dir}/{file.filename}"

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    filename = file.filename.lower()

    if filename.endswith(".txt"):
        parsed_text = read_txt(file_path)

    elif filename.endswith(".pdf"):
        parsed_text = read_pdf(file_path)

    elif filename.endswith(".docx"):
        parsed_text = read_docx(file_path)

    else:
        raise HTTPException(
            status_code=400,
            detail="Unsupported file format"
        )

    return {
        "status": "success",
        "filename": file.filename,
        "characters": len(parsed_text),
        "words": len(parsed_text.split()),
        "preview": parsed_text[:1000]
    }
    
@router.get("/simple") # TES SUMMARIZATION SEDERHANA
def simple_test():

    text = """
    Indonesia is a country in Southeast Asia.
    It has more than 17,000 islands.
    Jakarta is the capital city.
    """

    summary = summarize_text(text, 30)

    return {
        "summary": summary
    }