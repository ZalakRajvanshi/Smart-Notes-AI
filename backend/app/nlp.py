from symspellpy import SymSpell, Verbosity
import os
import re

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


# -------------------------
# TOKEN-LEVEL CORRECTION
# -------------------------

def _safe_correct_word(word: str) -> str:
    """
    Conservative correction for a single word.
    """

    # Skip numbers, symbols
    if not word.isalpha():
        return word

    # 🔒 Protect long / technical words
    if len(word) >= 12:
        return word

    suggestions = symspell.lookup(
        word,
        Verbosity.CLOSEST,
        max_edit_distance=MAX_EDIT_DISTANCE
    )

    if not suggestions:
        return word

    best = suggestions[0].term

    # Prevent drastic length changes
    if abs(len(best) - len(word)) > 2:
        return word

    return best


# -------------------------
# LINE-LEVEL CORRECTION
# -------------------------

def correct_text(text: str) -> str:
    """
    Safe OCR post-correction.
    """

    text = re.sub(r"\s+", " ", text).strip()
    if not text:
        return text

    words = text.split(" ")
    corrected_words = []

    for w in words:
        corrected_words.append(_safe_correct_word(w))

    corrected = " ".join(corrected_words)

    # Capitalize sentence start
    corrected = corrected[0].upper() + corrected[1:] if corrected else corrected

    return corrected
