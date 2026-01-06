from fastapi import APIRouter, UploadFile, File
import cv2
import numpy as np
import tempfile
from pathlib import Path
from backend.app.pdf import generate_pdf
import tempfile

from backend.app.layout import detect_blocks, segment_lines
from backend.app.ocr import OCRModel, ocr_block
from backend.app.structure import build_structure

router = APIRouter()


@router.get("/health")
def health_check():
    return {"status": "ok", "version": "v3"}


@router.post("/process")
async def process_document(image: UploadFile = File(...)):
    # Save uploaded image temporarily
    suffix = Path(image.filename).suffix
    with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
        tmp.write(await image.read())
        image_path = tmp.name

    # Load image
    img = cv2.imread(image_path)
    if img is None:
        return {"error": "Invalid image"}

    page_height, page_width, _ = img.shape

    # Initialize OCR (placeholder)
    ocr = OCRModel()

    blocks = detect_blocks(image_path)
    blocks_data = []

    for (x, y, w, h) in blocks:
        block_img = img[y:y+h, x:x+w]
        lines = segment_lines(block_img)
        ocr_lines = ocr_block(block_img, lines, ocr)

        blocks_data.append({
            "bbox": (x, y, w, h),
            "lines": ocr_lines
        })

    structured = build_structure(blocks_data, page_height)

    return {
        "blocks": structured
    }

@router.post("/export/pdf")
async def export_pdf(image: UploadFile = File(...)):
    suffix = Path(image.filename).suffix
    with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
        tmp.write(await image.read())
        image_path = tmp.name

    img = cv2.imread(image_path)
    page_height, _, _ = img.shape

    ocr = OCRModel()
    blocks = detect_blocks(image_path)

    blocks_data = []

    for (x, y, w, h) in blocks:
        block_img = img[y:y+h, x:x+w]
        lines = segment_lines(block_img)
        ocr_lines = ocr_block(block_img, lines, ocr)

        blocks_data.append({
            "bbox": (x, y, w, h),
            "lines": ocr_lines
        })

    structured = build_structure(blocks_data, page_height)

    pdf_file = tempfile.NamedTemporaryFile(delete=False, suffix=".pdf")
    generate_pdf(structured, pdf_file.name)

    return {
        "message": "PDF generated",
        "pdf_path": pdf_file.name
    }

