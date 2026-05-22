import os
import fitz
from docx import Document


async def parse_document(file_path: str):

    extension = os.path.splitext(file_path)[1]

    if extension == ".pdf":
        return parse_pdf(file_path)

    elif extension == ".docx":
        return parse_docx(file_path)

    elif extension == ".txt":
        return parse_txt(file_path)

    else:
        raise ValueError("Unsupported file type")


def parse_pdf(file_path: str):

    document = fitz.open(file_path)

    pages = []

    full_text = ""

    for page_number, page in enumerate(document):

        text = page.get_text()

        pages.append({
            "page": page_number + 1,
            "text": text
        })

        full_text += text + "\n"

    return {
        "type": "pdf",
        "total_pages": len(pages),
        "content": full_text
    }


def parse_docx(file_path: str):

    document = Document(file_path)

    paragraphs = []

    full_text = ""

    for paragraph in document.paragraphs:

        text = paragraph.text.strip()

        if text:

            paragraphs.append(text)

            full_text += text + "\n"

    return {
        "type": "docx",
        "total_paragraphs": len(paragraphs),
        "content": full_text
    }


def parse_txt(file_path: str):

    with open(file_path, "r", encoding="utf-8") as file:

        content = file.read()

    return {
        "type": "txt",
        "content": content
    }