import torch
import cv2
import numpy as np
from transformers import TrOCRProcessor, VisionEncoderDecoderModel

# -----------------------------
# DEVICE
# -----------------------------

DEVICE = "cuda" if torch.cuda.is_available() else "cpu"

# -----------------------------
# LOAD MODEL ONCE (GLOBAL)
# -----------------------------

processor = TrOCRProcessor.from_pretrained(
    "microsoft/trocr-base-handwritten"
)

model = VisionEncoderDecoderModel.from_pretrained(
    "microsoft/trocr-base-handwritten"
).to(DEVICE)

model.eval()

# -----------------------------
# LINE NORMALIZATION (CRITICAL)
# -----------------------------

def normalize_line_for_trocr(line_img: np.ndarray):
    """
    Normalize a single line image to match TrOCR expectations.
    Input: BGR or grayscale numpy image
    Output: RGB image with height=32 or None if invalid
    """
    if line_img is None:
        return None

    if line_img.size == 0:
        return None

    # Convert to grayscale if needed
    if len(line_img.shape) == 3:
        line_img = cv2.cvtColor(line_img, cv2.COLOR_BGR2GRAY)

    h, w = line_img.shape

    # Hard reject tiny or empty crops
    if h < 10 or w < 40:
        return None

    # Resize by HEIGHT only (preserve aspect ratio)
    new_w = max(int(w * (32 / h)), 32)
    line_img = cv2.resize(line_img, (new_w, 32), interpolation=cv2.INTER_CUBIC)

    # Convert to RGB (TrOCR expects RGB)
    line_img = cv2.cvtColor(line_img, cv2.COLOR_GRAY2RGB)

    return line_img


# -----------------------------
# OCR FUNCTION (PUBLIC API)
# -----------------------------

def infer_line(line_img: np.ndarray) -> str:
    """
    OCR a single handwritten line image (numpy array).
    Returns recognized text or empty string.
    """
    norm = normalize_line_for_trocr(line_img)
    if norm is None:
        return ""

    inputs = processor(
        images=norm,
        return_tensors="pt"
    ).to(DEVICE)

    with torch.no_grad():
        generated_ids = model.generate(
            inputs.pixel_values,
            max_length=128,
            early_stopping=True
        )

    text = processor.batch_decode(
        generated_ids,
        skip_special_tokens=True
    )[0]

    return text.strip()
