from .nlp import correct_text


def classify_block(bbox, lines, page_height):
    _, y, _, h = bbox
    if y < page_height * 0.15 and len(lines) <= 1:
        return "title"
    if len(lines) <= 2:
        return "heading"
    return "paragraph"


def build_structure(blocks, page_height):
    structured = []

    for b in blocks:
        lines = b["lines"]
        raw = " ".join(l["text"] for l in lines)
        clean = correct_text(raw)

        if clean.strip():
            structured.append({
                "type": classify_block(b["bbox"], lines, page_height),
                "content": clean,
                "editable": True
            })

    return structured
