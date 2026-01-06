import cv2
import numpy as np


def detect_blocks(image_path):
    """
    Detects text blocks in a handwritten page using morphology.
    Returns list of bounding boxes.
    """

    img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    if img is None:
        raise ValueError("Image not found")

    # 1. Binarize
    _, thresh = cv2.threshold(
        img, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU
    )

    # 2. Dilate to merge text into blocks
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (25, 15))
    dilated = cv2.dilate(thresh, kernel, iterations=2)

    # 3. Find contours (blocks)
    contours, _ = cv2.findContours(
        dilated, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE
    )

    blocks = []
    for cnt in contours:
        x, y, w, h = cv2.boundingRect(cnt)
        if w > 100 and h > 50:  # filter noise
            blocks.append((x, y, w, h))

    # Sort top-to-bottom
    blocks = sorted(blocks, key=lambda b: b[1])
    return blocks


def segment_lines(block_image):
    
    """
    Segments lines within a text block using horizontal projection.
    """

    gray = cv2.cvtColor(block_image, cv2.COLOR_BGR2GRAY)
    _, thresh = cv2.threshold(
        gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU
    )

    # Horizontal projection
    horizontal_sum = np.sum(thresh, axis=1)

    lines = []
    start = None

    for i, val in enumerate(horizontal_sum):
        if val > 0 and start is None:
            start = i
        elif val == 0 and start is not None:
            end = i
            if end - start > 15:
                lines.append((start, end))
            start = None

    # Handle case where line goes till bottom
    if start is not None:
        lines.append((start, len(horizontal_sum)))

    return lines
