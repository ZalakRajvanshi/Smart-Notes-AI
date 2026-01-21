import torch
import cv2
import numpy as np
from transformers import TrOCRProcessor, VisionEncoderDecoderModel

DEVICE = "cuda" if torch.cuda.is_available() else "cpu"

processor = TrOCRProcessor.from_pretrained(
    "microsoft/trocr-base-handwritten"
)
model = VisionEncoderDecoderModel.from_pretrained(
    "microsoft/trocr-base-handwritten"
).to(DEVICE)
model.eval()


def normalize_line(line_img):
    if line_img is None:
        return None

    if len(line_img.shape) == 3:
        line_img = cv2.cvtColor(line_img, cv2.COLOR_BGR2GRAY)

    h, w = line_img.shape
    if h < 10 or w < 40:
        return None

    scale = 32 / h
    new_w = int(w * scale)
    line_img = cv2.resize(line_img, (new_w, 32))

    line_img = cv2.cvtColor(line_img, cv2.COLOR_GRAY2RGB)
    return line_img


def infer_line(line_img: np.ndarray) -> str:
    img = normalize_line(line_img)
    if img is None:
        return ""

    inputs = processor(images=img, return_tensors="pt").to(DEVICE)

    with torch.no_grad():
        ids = model.generate(inputs.pixel_values, max_length=128)

    text = processor.batch_decode(ids, skip_special_tokens=True)[0]
    return text.strip()
