import os
from fastapi import UploadFile
from app.utils.file_utils import UPLOAD_DIR


ALLOWED_EXTENSIONS = [".pdf", ".docx", ".txt"]

async def save_uploaded_file(file: UploadFile):

    file_extension = os.path.splitext(file.filename)[1]

    if file_extension not in ALLOWED_EXTENSIONS:
        raise ValueError("File type not allowed")

    file_path = os.path.join(UPLOAD_DIR, file.filename)

    with open(file_path, "wb") as buffer:
        content = await file.read()
        buffer.write(content)

    return {
        "filename": file.filename,
        "content_type": file.content_type,
        "size": len(content),
        "path": file_path
    }