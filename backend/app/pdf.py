from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, ListFlowable, ListItem
from reportlab.lib.units import inch
import tempfile
import os


def generate_pdf(structured_blocks):
    """
    Generates a clean PDF from structured document blocks.
    Returns the file path.
    """
    tmp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".pdf")
    tmp_file.close()

    doc = SimpleDocTemplate(
        tmp_file.name,
        pagesize=A4,
        rightMargin=40,
        leftMargin=40,
        topMargin=40,
        bottomMargin=40
    )

    styles = getSampleStyleSheet()
    elements = []

    for block in structured_blocks:
        block_type = block["type"]
        content = block["content"]

        if not content:
            continue

        if block_type == "title":
            style = styles["Title"]
            elements.append(Paragraph(content, style))
            elements.append(Spacer(1, 0.3 * inch))

        elif block_type == "heading":
            style = styles["Heading2"]
            elements.append(Paragraph(content, style))
            elements.append(Spacer(1, 0.2 * inch))

        elif block_type == "bullet_list":
            bullets = content.split()
            bullet_items = [
                ListItem(Paragraph(b, styles["Normal"]))
                for b in bullets
            ]
            elements.append(ListFlowable(bullet_items, bulletType="bullet"))
            elements.append(Spacer(1, 0.2 * inch))

        else:  # paragraph
            style = styles["Normal"]
            elements.append(Paragraph(content, style))
            elements.append(Spacer(1, 0.15 * inch))

    doc.build(elements)
    return tmp_file.name
