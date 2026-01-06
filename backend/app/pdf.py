from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch


def generate_pdf(structured_blocks, output_path):
    c = canvas.Canvas(output_path, pagesize=A4)
    width, height = A4

    x_margin = 1 * inch
    y = height - 1 * inch

    for block in structured_blocks:
        block_type = block["type"]
        text = block["content"]

        if block_type == "title":
            c.setFont("Helvetica-Bold", 20)
            c.drawString(x_margin, y, text)
            y -= 40

        elif block_type == "heading":
            c.setFont("Helvetica-Bold", 14)
            c.drawString(x_margin, y, text)
            y -= 30

        elif block_type == "bullet_list":
            c.setFont("Helvetica", 11)
            for line in text.split("•"):
                c.drawString(x_margin + 15, y, "• " + line.strip())
                y -= 18

        else:  # paragraph
            c.setFont("Helvetica", 11)
            for line in text.split():
                if y < 1 * inch:
                    c.showPage()
                    y = height - 1 * inch
                    c.setFont("Helvetica", 11)
                c.drawString(x_margin, y, line)
                y -= 14

        y -= 10

        if y < 1 * inch:
            c.showPage()
            y = height - 1 * inch

    c.save()
