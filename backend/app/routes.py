import cv2, tempfile, os
from fastapi import APIRouter, UploadFile, File, Body
from .ocr_blocks import ocr_page
from .structure import build_structure
from .pdf import generate_pdf

router = APIRouter()


@router.post("/process")
async def process_image(file: UploadFile = File(...)):
    with tempfile.NamedTemporaryFile(delete=False) as tmp:
        tmp.write(await file.read())
        path = tmp.name

    img = cv2.imread(path)
    h = img.shape[0]

    blocks = ocr_page(path)
    structured = build_structure(blocks, h)
    pdf = generate_pdf(structured)

    os.unlink(path)
    return {"structure": structured, "pdf_path": pdf}


@router.post("/export-pdf")
async def export_pdf(structure: list = Body(...)):
    pdf = generate_pdf(structure)
    return {"pdf_path": pdf}
