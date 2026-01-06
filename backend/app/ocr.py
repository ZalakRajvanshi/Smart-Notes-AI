import cv2
import numpy as np


class OCRModel:
    """
    Placeholder OCR model.
    Will be replaced with trained CRNN weights.
    """

    def __init__(self, model_path=None):
        self.model_path = model_path
        self.model = None  # loaded later

    def preprocess(self, line_image):
        """
        Resize, normalize, prepare image for model.
        """
        gray = cv2.cvtColor(line_image, cv2.COLOR_BGR2GRAY)
        resized = cv2.resize(gray, (200, 32))
        normalized = resized / 255.0
        return normalized

    def predict(self, line_image):
        """
        OCR inference on a single line image.
        """
        _ = self.preprocess(line_image)

        # TEMPORARY PLACEHOLDER
        # Real decoding will come after training
        return "[TEXT]"


def ocr_block(block_image, line_segments, ocr_model):
    """
    Runs OCR on each line segment inside a block.
    """
    results = []

    for (start, end) in line_segments:
        line_img = block_image[start:end, :]
        text = ocr_model.predict(line_img)

        results.append({
            "text": text,
            "line_bbox": [0, start, block_image.shape[1], end - start]
        })

    return results
