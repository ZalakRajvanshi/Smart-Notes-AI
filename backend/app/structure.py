def classify_block(block_bbox, ocr_lines, page_height):
    """
    Classifies a block into semantic roles.
    """
    x, y, w, h = block_bbox
    num_lines = len(ocr_lines)

    # Title: top of page, single large line
    if y < page_height * 0.15 and num_lines == 1 and h > 60:
        return "title"

    # Heading: few lines, medium height
    if num_lines <= 2 and h < 120:
        return "heading"

    # Bullets: multiple short lines
    bullet_count = 0
    for line in ocr_lines:
        text = line["text"].strip()
        if text.startswith(("-", "•", "*")):
            bullet_count += 1

    if bullet_count >= 1:
        return "bullet_list"

    # Default
    return "paragraph"

def build_structure(blocks_data, page_height):
    """
    Converts blocks into structured document format.
    """
    structured = []

    for block in blocks_data:
        block_type = classify_block(
            block["bbox"],
            block["lines"],
            page_height
        )

        content = " ".join([l["text"] for l in block["lines"]])

        structured.append({
            "type": block_type,
            "content": content,
            "editable": True
        })

    return structured
