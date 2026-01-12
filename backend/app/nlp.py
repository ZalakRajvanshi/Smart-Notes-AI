from symspellpy import SymSpell, Verbosity
from textblob import TextBlob
import os
import re

# ---------------------------
# SYMSPELL SETUP
# ---------------------------

MAX_EDIT_DISTANCE = 2
PREFIX_LENGTH = 7

symspell = SymSpell(
    max_dictionary_edit_distance=MAX_EDIT_DISTANCE,
    prefix_length=PREFIX_LENGTH
)

BASE_DIR = os.path.dirname(__file__)
DICT_PATH = os.path.join(
    BASE_DIR,
    "frequency_dictionary_en_82_765.txt"
)

if not symspell.word_count:
    symspell.load_dictionary(
        DICT_PATH,
        term_index=0,
        count_index=1
    )


# ---------------------------
# SAFE WORD CORRECTION
# ---------------------------

def _safe_symspell(word: str) -> str:
    if not word.isalpha():
        return word

    if len(word) >= 12:  # protect technical words
        return word

    suggestions = symspell.lookup(
        word,
        Verbosity.CLOSEST,
        max_edit_distance=MAX_EDIT_DISTANCE
    )

    if not suggestions:
        return word

    best = suggestions[0].term

    # prevent wild replacements
    if abs(len(best) - len(word)) > 2:
        return word

    return best


# ---------------------------
# TEXTBLOB (VERY LIMITED)
# ---------------------------

def _light_textblob(text: str) -> str:
    """
    Grammar smoothing ONLY.
    No aggressive correction.
    """
    try:
        blob = TextBlob(text)
        corrected = str(blob.correct())

        # Safety: reject if too different
        if abs(len(corrected) - len(text)) > len(text) * 0.3:
            return text

        return corrected
    except Exception:
        return text


# ---------------------------
# MAIN ENTRY
# ---------------------------

def correct_text(text: str) -> str:
    text = re.sub(r"\s+", " ", text).strip()
    if not text:
        return text

    # --- Step 1: SymSpell (token-level) ---
    words = text.split(" ")
    symspell_fixed = " ".join(
        [_safe_symspell(w) for w in words]
    )

    # --- Step 2: TextBlob (light polish) ---
    final_text = _light_textblob(symspell_fixed)

    # Capitalize sentence
    final_text = final_text[0].upper() + final_text[1:] if final_text else final_text

    return final_text
