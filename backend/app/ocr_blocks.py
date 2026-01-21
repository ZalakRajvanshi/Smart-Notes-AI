import cv2
from .layout import detect_blocks
from .ocr import infer_line


def segment_lines(block_img):
    gray = cv2.cvtColor(block_img, cv2.COLOR_BGR2GRAY)
    _, th = cv2.threshold(gray, 0, 255,
                          cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)

    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 9))
    dilated = cv2.dilate(th, kernel, iterations=1)

    cnts, _ = cv2.findContours(
        dilated, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE
    )

    lines = [cv2.boundingRect(c) for c in cnts]
    return sorted(lines, key=lambda b: b[1])


def ocr_page(image_path):
    img = cv2.imread(image_path)
    if img is None:
        return []

    blocks = detect_blocks(image_path)
    results = []

    for x, y, w, h in blocks:
        block_img = img[y:y+h, x:x+w]
        lines = segment_lines(block_img)

        ocr_lines = []
        gray = cv2.cvtColor(block_img, cv2.COLOR_BGR2GRAY)

        for lx, ly, lw, lh in lines:
            crop = gray[ly:ly+lh, lx:lx+lw]
            text = infer_line(crop)
            if text:
                ocr_lines.append({"text": text})

        if ocr_lines:
            results.append({
                "bbox": [x, y, w, h],
                "lines": ocr_lines
            })

    return results
