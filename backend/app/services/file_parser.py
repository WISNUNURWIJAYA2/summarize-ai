from docx import Document
import fitz


def read_txt(file_path):

    with open(file_path, "r", encoding="utf-8") as f:
        return f.read()


def read_docx(file_path):

    doc = Document(file_path)

    text = []

    for para in doc.paragraphs:
        text.append(para.text)

    return "\n".join(text)


def read_pdf(file_path):

    text = ""

    pdf = fitz.open(file_path)

    for page in pdf:
        text += page.get_text()

    return text