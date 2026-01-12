import cv2
from .layout import detect_blocks
from .ocr import infer_line


# ===============================
# LINE SEGMENTATION
# ===============================

def segment_lines(block_img):
    """
    Detect line bounding boxes inside a block.
    Returns list of (x, y, w, h) sorted top-to-bottom.
    """
    gray = cv2.cvtColor(block_img, cv2.COLOR_BGR2GRAY)

    _, thresh = cv2.threshold(
        gray, 0, 255,
        cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU
    )

    # Merge characters into full text lines
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 9))
    dilated = cv2.dilate(thresh, kernel, iterations=1)

    contours, _ = cv2.findContours(
        dilated, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE
    )

    lines = []
    for cnt in contours:
        x, y, w, h = cv2.boundingRect(cnt)

        # Skip tiny noise
        if h < 8 or w < 40:
            continue

        lines.append((x, y, w, h))

    # Sort top → bottom
    lines = sorted(lines, key=lambda b: b[1])
    return lines


# ===============================
# OCR A SINGLE BLOCK
# ===============================

def ocr_block(block_img, line_boxes):
    """
    Runs OCR on each detected line inside a block.
    """
    results = []

    for (x, y, w, h) in line_boxes:
        line_img = block_img[y:y+h, x:x+w]

        if line_img is None or line_img.size == 0:
            continue

        # 🔑 IMPORTANT:
        # Pass RAW line image to TrOCR
        text = infer_line(line_img)

        if text.strip() == "":
            continue

        results.append({
            "text": text,
            "bbox": [x, y, w, h]
        })

    return results


# ===============================
# FULL PAGE OCR
# ===============================

def ocr_page(image_path):
    """
    Full OCR pipeline:
    page → blocks → lines → text
    """
    img = cv2.imread(image_path)
    if img is None:
        return []

    blocks = detect_blocks(image_path)
    page_results = []

    for (x, y, w, h) in blocks:
        block_img = img[y:y+h, x:x+w]

        if block_img is None or block_img.size == 0:
            continue

        line_boxes = segment_lines(block_img)
        ocr_lines = ocr_block(block_img, line_boxes)

        if not ocr_lines:
            continue

        page_results.append({
            "bbox": [x, y, w, h],
            "lines": ocr_lines
        })

    return page_results
