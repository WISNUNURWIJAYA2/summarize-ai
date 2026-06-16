from io import BytesIO

from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer
)

from reportlab.lib.styles import getSampleStyleSheet


def create_summary_pdf(
    filename: str,
    ratio: int,
    summary: str
):

    buffer = BytesIO()

    doc = SimpleDocTemplate(buffer)

    styles = getSampleStyleSheet()

    content = []

    content.append(
        Paragraph(
            "Document Summary",
            styles["Title"]
        )
    )

    content.append(
        Spacer(1, 12)
    )

    content.append(
        Paragraph(
            f"Source File: {filename}",
            styles["Normal"]
        )
    )

    content.append(
        Paragraph(
            f"Ratio: {ratio}%",
            styles["Normal"]
        )
    )

    content.append(
        Spacer(1, 12)
    )

    content.append(
        Paragraph(
            summary,
            styles["BodyText"]
        )
    )

    doc.build(content)

    buffer.seek(0)

    return buffer