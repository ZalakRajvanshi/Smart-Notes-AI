import re
from symspellpy import SymSpell, Verbosity
from textblob import TextBlob

# ===============================
# SYMSPELL SETUP (CONSERVATIVE)
# ===============================

symspell = SymSpell(max_dictionary_edit_distance=2, prefix_length=7)

# Load frequency dictionary (small + safe)
symspell.load_dictionary(
    "backend/app/frequency_dictionary_en_82_765.txt",
    term_index=0,
    count_index=1
)

# ===============================
# PROTECTED WORDS (CRITICAL)
# ===============================

PROTECTED_WORDS = {
    # technical / domain
    "methamphetamine",
    "ethamphetamine",
    "robotic",
    "robotics",
    "metallification",
    "technology",
    "technologies",
    "machine",
    "machines",

    # common OCR-safe words
    "wilson",
    "dean",
    "root"
}

# ===============================
# SAFE TOKEN CORRECTION
# ===============================

def _safe_symspell(word: str) -> str:
    clean = word.lower().strip(".,;:!?")

    # 1️⃣ protect names / capitalized words
    if word[0].isupper():
        return word

    # 2️⃣ protect domain words
    if clean in PROTECTED_WORDS:
        return word

    # 3️⃣ protect numbers
    if any(char.isdigit() for char in word):
        return word

    # 4️⃣ protect long words (likely technical)
    if len(clean) >= 12:
        return word

    # 5️⃣ non alphabetic → skip
    if not clean.isalpha():
        return word

    # 6️⃣ symspell lookup (TOP suggestion only)
    suggestions = symspell.lookup(
        clean,
        Verbosity.TOP,
        max_edit_distance=1
    )

    if suggestions:
        return suggestions[0].term

    return word


# ===============================
# MAIN NLP PIPELINE
# ===============================

def correct_text(text: str) -> str:
    if not text.strip():
        return text

    # ---------------------------
    # TOKEN LEVEL CORRECTION
    # ---------------------------
    tokens = re.findall(r"\w+|[^\w\s]", text)
    corrected_tokens = [_safe_symspell(t) for t in tokens]
    corrected = " ".join(corrected_tokens)

    # ---------------------------
    # LIGHT GRAMMAR SMOOTHING
    # ---------------------------
    try:
        blob = TextBlob(corrected)
        corrected = str(blob.correct())
    except Exception:
        pass  # never crash pipeline

    # ---------------------------
    # CLEANUP (IMPORTANT)
    # ---------------------------
    corrected = re.sub(r"\s+([.,!?])", r"\1", corrected)
    corrected = re.sub(r"\.\s*\.", ".", corrected)
    corrected = re.sub(r"\s{2,}", " ", corrected)

    return corrected.strip()
