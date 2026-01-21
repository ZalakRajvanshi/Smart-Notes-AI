from symspellpy import SymSpell, Verbosity
from textblob import TextBlob
import pkg_resources

sym = SymSpell(max_dictionary_edit_distance=2, prefix_length=7)
dict_path = pkg_resources.resource_filename(
    "symspellpy", "frequency_dictionary_en_82_765.txt"
)
sym.load_dictionary(dict_path, 0, 1)


def correct_text(text: str) -> str:
    words = text.split()
    fixed = []

    for w in words:
        sug = sym.lookup(w, Verbosity.CLOSEST, max_edit_distance=2)
        fixed.append(sug[0].term if sug else w)

    blob = TextBlob(" ".join(fixed))
    return str(blob.correct())
