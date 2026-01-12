def classify_block(block_bbox, ocr_lines, page_height):
    """
    Classify a block based on position, size, and OCR content.
    """
    x, y, w, h = block_bbox
    num_lines = len(ocr_lines)

    # -------------------
    # TITLE
    # -------------------
    if y < page_height * 0.15 and num_lines <= 1 and h > 60:
        return "title"

    # -------------------
    # HEADING
    # -------------------
    if num_lines <= 2 and h < 120:
        return "heading"

    # -------------------
    # BULLET LIST
    # -------------------
    bullet_count = 0
    for line in ocr_lines:
        text = line.get("text", "").strip()
        if text.startswith(("-", "•", "*")):
            bullet_count += 1

    if bullet_count >= 1:
        return "bullet_list"

    # -------------------
    # DEFAULT
    # -------------------
    return "paragraph"


def build_structure(blocks_data, page_height):
    """
    Convert OCR blocks into structured, editable document format.
    """
    structured = []

    for block in blocks_data:
        bbox = block.get("bbox")

        if not bbox:
            continue

        # 🔑 Always expect line-based OCR now
        lines = block.get("lines", [])

        # Skip empty OCR blocks
        if not lines:
            continue

        block_type = classify_block(bbox, lines, page_height)

        # Merge line texts safely
        content = " ".join(
            l.get("text", "").strip()
            for l in lines
            if l.get("text", "").strip()
        ).strip()

        # Skip blocks with no readable content
        if content == "":
            continue

        structured.append({
            "type": block_type,
            "content": content,
            "editable": True
        })

    return structured
