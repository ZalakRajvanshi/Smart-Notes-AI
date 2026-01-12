import cv2
import tempfile
import os
from fastapi import APIRouter, UploadFile, File

from .ocr_blocks import ocr_page
from .structure import build_structure
from .pdf import generate_pdf

router = APIRouter()


@router.post("/process")
async def process_image(file: UploadFile = File(...)):
    # ----------------------------------
    # SAVE UPLOADED IMAGE
    # ----------------------------------
    suffix = os.path.splitext(file.filename)[-1]

    with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
        tmp.write(await file.read())
        image_path = tmp.name

    # ----------------------------------
    # LOAD IMAGE
    # ----------------------------------
    img = cv2.imread(image_path)
    if img is None:
        os.unlink(image_path)
        return {
            "structure": [],
            "pdf_path": None
        }

    page_height = img.shape[0]

    # ----------------------------------
    # OCR PIPELINE (BLOCK → LINE → OCR)
    # ----------------------------------
    blocks_data = ocr_page(image_path)

    # ----------------------------------
    # STRUCTURE
    # ----------------------------------
    structured = build_structure(blocks_data, page_height)

    # ----------------------------------
    # PDF
    # ----------------------------------
    pdf_path = generate_pdf(structured)

    # ----------------------------------
    # CLEANUP
    # ----------------------------------
    os.unlink(image_path)

    return {
        "structure": structured,
        "pdf_path": pdf_path
    }
